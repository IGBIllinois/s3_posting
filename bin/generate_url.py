#!/usr/bin/env python

import sys
import os.path
import glob
from optparse import OptionParser

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir + "/lib")
config_file = root_dir + "/config/config.yaml"
import s3_posting
from s3_posting import functions
from s3_posting import s3_posting
from s3_posting import s3_mail
from s3_posting import config

settings = {}
settings['bucket'] = ""
settings['region'] = ""
settings['access_key_id'] = None
settings['secret_access_key'] = None
settings['url_expires'] = 0
settings['subfolder'] = None

posting_files = []
url = {}

def main():
	
	global settings
	global posting_files
	global file_checksums
	global url

	description = "Posts data to S3 buckets through linux command line\n"
	description += functions.get_website()
	parser = OptionParser(description=description,version=functions.get_version())
	parser.add_option("-p","--profile",type="string",help="Profile to use");
	parser.add_option("-f","--file",action='append', type="string",help="Filename to upload");
	parser.add_option("-d","--dir",action='append',type="string",help="Directory to upload");
	parser.add_option("-e","--email",action='append',type='string', help="Email to send to");
	parser.add_option("-b","--bucket",type='string',help="Bucket to upload to");
	parser.add_option("-s","--subfolder",type='string',help="Folder to place object in");	
	parser.add_option("--dry-run",action='store_true',help="Dry Run. Disable uploads and emails");
	(options,args) = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		quit(1)

	#Load config file and verify it
	cfg = config.load_config(config_file)
	if (not config.validate_config(cfg)):
		print ("Invalid config.yaml\n")
		quit()

	if (("access_key_id" in cfg['aws']) and ("secret_access_key" in cfg['aws'])):	
		settings['access_key_id'] = cfg['aws']['access_key_id']
		settings['secret_access_key'] = cfg['aws']['secret_access_key']

	if ("url_expires" in cfg['aws']):
		settings['url_expires'] = cfg['aws']['url_expires']
	if ("region" in cfg['aws']):
		settings['region'] = cfg['aws']['region']

	if ("endpoint_url" in cfg['aws']):
		settings['endpoint_url'] = cfg['aws']['endpoint_url']

	#Verify -f/--files files and -d/--dir 
	if ((options.file != None) and (options.dir != None)):
		parser.error("--file and --dir are mutually exclusive")
		quit(1)
	elif ((options.file == None) and (options.dir == None)):
		parser.error("Must specify a file with --file or a dir with --dir")
		quit(1)
	elif ((options.file != None) and (options.dir == None)):
		success = True
		for i in options.file:
			if (os.path.isfile(i) == False):
				parser.error("File " + i + " does not exist")
				success = False
			posting_files = options.file
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
					posting_files.extend(result)
	
	if (options.subfolder != None):
		cfg['subfolder'] = options.subfolder
		
	#Verify -email
	if (options.email == None):
		parser.error("Must specifiy an email address with --email")
		quit(1)
	else:
		for i in options.email:
			if (not config.validate_email(i)):
				parser.error("Invalid email " + i)
				quit(1)

	#Verify cc emails
	if (cfg['email']['cc_emails'] != None):
		for i in cfg['email']['cc_emails']:
			if (not config.validate_email(i)):
				parser.error("Invalid cc email " + i)
				quit(1)
		settings['cc'] = cfg['email']['cc_emails']

	#Verify -b/--bucket
	if ((options.bucket == None) and cfg['aws']['default_bucket'] == None):
		parser.error("Must specify a bucket")
		quit()
	elif ((options.bucket == None) and cfg['aws']['default_bucket'] != None):
		settings['bucket'] = cfg['aws']['default_bucket']
	else:
		settings['bucket'] = options.bucket

	functions.log("Bucket: " + settings['bucket'])
	
	


	#If Dry Run is disabled, generate url and send email
	if (options.dry_run == None):
		s3_connection = s3_posting.s3_posting(settings['region'],settings['access_key_id'],settings['secret_access_key'],settings['bucket'],settings['endpoint_url'])
	
		if (s3_connection.bucket_exists() != True):
                	functions.log("Bucket " + settings['bucket'] + " does not exist")
	                quit()

		if not s3_connection.directory_exists(settings['subfolder']):
			functions.log("Directory " + options.email + " does not exist.  Creating Directory")



		#Generate URL
		for i in posting_files:
			basename = os.path.basename(i)
			if (settings['subfolder'] != None):
				full_path = settings['subfolder'] + "/" + basename
			else:
				full_path = basename
			url[i] = s3_connection.get_url(basename,settings['url_expires'],'test1');
			functions.log("File: " + i + ", URL: " + url[i])
		#Send Email
		mail = s3_mail.s3_mail(options.email,url,file_md5_checksums,file_sha256_checksums,cfg)
		mail.send_email()
	elif (options.dry_run):
		functions.log("Dry Run Enabled - Disabling uploads and email")

if __name__ == '__main__':
	main()
