#!/usr/bin/env python

import sys
import os.path, time
import socket
import getpass
import glob
from optparse import OptionParser

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir + "/lib")

import s3_posting
from s3_posting import functions
from s3_posting import s3_posting
from s3_posting import s3_mail
from s3_posting import profile

parameters = {}
parameters['bucket'] = ""
parameters['overwrite'] = False
parameters['no-progressbar'] = False
parameters['md5sum'] = False
parameters['sha256sum'] = False
parameters['subfolder'] = None

posting_files = {}
emails = {}
reserved_metadata = ['original_location','hostname','creation_date','emails','username','md5sum','sha256sum']
global_metadata = {}

def main():
	
    global parameters
    global posting_files
    global emails

    description = "Posts data to S3 buckets through linux command line\n"
    description += functions.get_website()
    profile_list = functions.get_profiles(root_dir +"/config/")
    parser = OptionParser(description=description,version=functions.get_version())
    parser.add_option("-p","--profile",type="string",help="Profile to use ("+profile_list+")");
    parser.add_option("-f","--file",action='append', type="string",help="Filename to upload");
    parser.add_option("-d","--dir",action='append', type="string",help="Directory to upload");
    parser.add_option("-e","--email",action='append',type='string', help="Email to send to");
    parser.add_option("-b","--bucket",action='append', type='string',help="Bucket to upload to");
    parser.add_option("-s","--subfolder",type='string',help="Folder to place object in");	
    parser.add_option("--md5",action='store_true',help="Create md5 checksums");
    parser.add_option("--sha256",action='store_true',help="Create sha256 checksums");
    parser.add_option("-m","--metadata",action='append',type='string',help="Key/values metadata to add to object",metavar="KEY:VALUE");
    parser.add_option("--overwrite",action='store_true',help="Force overwrite of existing object");
    parser.add_option("--no-progressbar",action='store_true',help="Disable upload progress bar");
    parser.add_option("--dry-run",action='store_true',help="Dry Run. Disable uploads and emails");
    (options,args) = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        quit(1)

	#Load config file and verify it
    if (options.profile != None):
        profile_file = root_dir + "/config/" + options.profile + ".yaml"
    else:
        profile_file = root_dir + "/config/config.yaml"

    my_profile = profile.profile(profile_file)

	#Verify -f/--files files and -d/--dir
    if ((options.dir != None) and (len(options.dir) > 1)): 
        parser.error("-d/--dir can only be specified once")
    if ((options.file != None) and (options.dir != None)):
        parser.error("--file and --dir are mutually exclusive")
        quit(1)
    elif ((options.file == None) and (options.dir == None)):
        parser.error("Must specify a file with --file or a dir with --dir")
        quit(1)
    elif ((options.file != None) and (options.dir == None)):
        success = True
        k = 0
        for i in options.file:
            if (os.path.isfile(i) == False):
                parser.error("File " + i + " does not exist")
                success = False
            posting_files[k] = {}
            posting_files[k]['file'] = os.path.basename(i)
            posting_files[k]['full_path'] = i
            k += 1
        if not success:
            quit(1)
    elif ((options.file == None) and (options.dir != None)):
        for i in options.dir:
            if (os.path.isdir(i) == False):
                parser.error("Directory " + i + " is not a directory")
                quit(1)
            else:
                result = functions.get_files_in_dir(i)
                if (result == False):
                    parser.error("No files in " + i)
                    quit(1)
                else:
                    k = 0;
                    for file_result in result:
                        posting_files[k] = {}
                        posting_files[k]['file'] = os.path.basename(file_result)
                        posting_files[k]['full_path'] = file_result
                        k += 1

    if (options.subfolder != None):
        parameters['subfolder'] = options.subfolder
        functions.log("Subfolder: " + parameters['subfolder'])
	
    if (options.no_progressbar != None):
        parameters['no-progressbar'] = True
        functions.log("Disabling Progress Bar")

	#Verify -email
    if ((options.email == None) and my_profile.get_email_enabled()):
        parser.error("Must specifiy an email address with --email")
        quit(1)
    elif ((options.email != None) and my_profile.get_email_enabled()):
        k = 0
        for i in options.email:
            if (not functions.validate_email(i)):
                parser.error("Invalid email " + i)
                quit(1)
	#Verify cc emails
    if (my_profile.get_cc_emails() != None):
        for i in my_profile.get_cc_emails():
            if (not functions.validate_email(i)):
                parser.error("Invalid cc email " + i)
                quit(1)

	#Verify -b/--bucket
    if ((options.bucket != None) and (len(options.bucket) > 1)):
        parser.error("Can only specifiy a single bucket with -b/--bucket")
        quit(1)
    elif ((options.bucket == None) and my_profile.get_bucket() == None):
        parser.error("Must specify a bucket")
        quit()
    elif ((options.bucket == None) and my_profile.get_bucket() != None):
        parameters['bucket'] = my_profile.get_bucket()
    else:
        parameters['bucket'] = " " . join(options.bucket)

    functions.log("Bucket: " + parameters['bucket'])
	
    if (options.md5):
        parameters['md5sum'] = True
        functions.log("md5 checksum enabled")
    if (options.sha256):
        parameters['sha256sum'] = True
        functions.log("sha256 checksum enabled")

	#Verify Metadata -m/--meta	
    if (options.metadata != None):
        for in_metadata in options.metadata:
            if ":" not in in_metadata:
                parser.error("Invalid metadata format for '" + in_metadata + "'.  Must be KEY:VALUE")
                quit(1)
            key,value = in_metadata.split(":")
            if key in reserved_metadata:
                parser.error("Can not specify '" + key + "' with -m/--meta.  This is a reserved metadata key")
                quit(1)
            if key in global_metadata:
                parser.error("Duplicate metadata for key '" + key + "'")
            else:	
                global_metadata[key] = value

	#Calculate md5 checksums
    if (parameters['md5sum']):
        functions.log("Calculating md5 checksums")
        for i in posting_files:
            checksum = functions.create_md5_checksum(posting_files[i]['full_path'])
            posting_files[i]['md5sum'] = str(checksum.decode("utf-8"))
            functions.log("File: " + posting_files[i]['full_path'] + ", MD5 checksum: " + str(checksum.decode("utf-8")))

    #Calculate sha256 checksums
    if (parameters['sha256sum']):
        functions.log("Calculating sha256 checksums")
        for i in posting_files:
            checksum = functions.create_sha256sum_checksum(posting_files[i]['full_path'])
            posting_files[i]['sha256sum'] = str(checksum.decode("utf-8"))
            functions.log("File: " + posting_files[i]['full_path'] + ", SHA256 checksum: " + str(checksum.decode("utf-8")))

	#If Dry Run is disabled, upload files and send email
    if (options.dry_run == None):
        s3_connection = s3_posting.s3_posting(my_profile,parameters)

        if (s3_connection.bucket_exists() != True):
            functions.log("Bucket " + parameters['bucket'] + " does not exist")
            quit()
	
        if (parameters['subfolder'] != None):
            if not s3_connection.directory_exists(parameters['subfolder']):
                functions.log("Directory " + parameters['subfolder'] + " does not exist.  Creating Directory")
                s3_connection.create_directory(parameters['subfolder'])

		#Upload Files
        for i in posting_files:
            creation_date = time.ctime(os.path.getctime(posting_files[i]['full_path']))

            file_metadata = {
			   "original_location" : posting_files[i]['full_path'],
			   "hostname" : socket.gethostname(),
			   "creation_date" : creation_date,
			   "username" : getpass.getuser(),
 
            }
            if ('md5sum' in posting_files[i]):
                file_metadata['md5sum'] = posting_files[i]['md5sum']
            if ('sha256sum' in posting_files[i]):
                file_metadata['sha256sum'] = posting_files[i]['sha256sum']

            if (my_profile.get_email_enabled()):
                file_metadata['emails'] = ",".join(options.email)

            file_metadata.update(global_metadata)
			
			#Get file size
            file_size = str(functions.get_filesize(posting_files[i]['full_path']))

            if (float(file_size) > functions.get_maxfilesize()):
                functions.log("File: " + posting_files[i]['full_path'] + " greater than maximum filesize of " + str(functions.get_maxfilesize()) + "GB")
                quit(1)
            elif (file_size == "0.0"):
                posting_files[i]['size'] = "<1"
                functions.log("File: " + posting_files[i]['full_path'] + " Size: <1 GB")
            else:
                posting_files[i]['size'] = file_size
                functions.log("File: " + posting_files[i]['full_path'] + " Size: " + file_size + " GB")

			#Upload file
            functions.log("File: " + posting_files[i]['full_path'] + " Uploading")
            s3_connection.upload_file(posting_files[i]['full_path'],file_metadata)
            functions.log("File: " + posting_files[i]['full_path'] + " Finish Uploading")
            print();
            basename = os.path.basename(posting_files[i]['file'])
            if (parameters['subfolder'] != None):
                full_path = parameters['subfolder'] + "/" + basename
            else:
                full_path = basename
		
		
        if (my_profile.get_email_enabled() and my_profile.get_seperate_emails()):
            k = 0
            for i in options.email:
                emails[k] = {}
                emails[k]['to'] = []
                emails[k]['to'].append(i)
                emails[k]['files'] = posting_files
                if (my_profile.get_url_expires() > 0):
                    for uploaded_files in emails[k]['files']:
                        s3_path = emails[k]['files'][uploaded_files]['file']
                        if (parameters['subfolder']):
                            s3_path = parameters['subfolder'] + "/" + s3_path
                        emails[k]['files'][uploaded_files]['url'] = s3_connection.get_url(s3_path,i)
                        functions.log("URL: " + emails[k]['files'][uploaded_files]['url'])
                k += 1
        elif (my_profile.get_email_enabled() and not my_profile.get_seperate_emails()):
            emails[0] = {}
            emails[0]['to'] = options.email
            emails[0]['files'] = posting_files
            if (my_profile.get_url_expires() > 0):
                for k in emails[0]['files']:
                    s3_path = emails[0]['files'][k]['file']
                    if (parameters['subfolder']):
                        s3_path = parameters['subfolder'] + "/" + s3_path
                    emails[0]['files'][k]['url'] = s3_connection.get_url(s3_path)
                    functions.log("URL:" + emails[0]['files'][k]['url'])
			
		#Send Email
        if (my_profile.get_email_enabled()):
            for email in emails:
                mail = s3_mail.s3_mail(my_profile,emails[email])
                mail.send_email()

    elif (options.dry_run):
        functions.log("Dry Run Enabled - Disabling uploads and email")

if __name__ == '__main__':
    main()

