#!/usr/bin/env python

import sys
import os.path
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
parameters['md5sum'] = False
parameters['sha256sum'] = False
parameters['subfolder'] = None

posting_files = {}
emails = {}

def main():
	
	global parameters
	global posting_files
	global emails

	description = "Regenerates unique URL for existing S3 file\n"
	description += functions.get_website()
	profile_list = functions.get_profiles(root_dir +"/config/")
	parser = OptionParser(description=description,version=functions.get_version())
	parser.add_option("-p","--profile",type="string",help="Profile to use ("+profile_list+")");
	parser.add_option("-f","--file",action='append', type="string",help="Filename to generate URL");
	parser.add_option("-e","--email",action='append',type='string', help="Email to send to");
	parser.add_option("-b","--bucket",type='string',help="Bucket to upload to");
	parser.add_option("-s","--subfolder",type='string',help="Folder to place object in");	
	parser.add_option("--dry-run",action='store_true',help="Dry Run. Disable generate URL and emails");
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
	if (options.file == None):
		parser.error("Must specify a file with -f/--file")
		quit(1)
	elif (options.file != None):
		k = 0
		for i in options.file:
			posting_files[k] = {}
			posting_files[k]['file'] = i
			k += 1
	
	if (options.subfolder != None):
		parameters['subfolder'] = options.subfolder
		
	#Verify -email
	if ((options.email == None) and my_profile.get_email_enabled()):
		parser.error("Must specifiy an email address with --email")
		quit(1)
	else:
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
		quit(1)
	elif ((options.bucket == None) and my_profile.get_bucket() != None):
		parameters['bucket'] = my_profile.get_bucket()
	else:
		parameters['bucket'] = options.bucket

	functions.log("Bucket: " + parameters['bucket'])
	
	#If Dry Run is disabled, generate urls and send email
	if (options.dry_run == None):
		s3_connection = s3_posting.s3_posting(my_profile,parameters)

	
		if (s3_connection.bucket_exists() != True):
			functions.log("Bucket " + parameters['bucket'] + " does not exist")
			sys.exit('Aborting')

		#if not s3_connection.object_exists(parameters['subfolder']):
		#	functions.log("Subfolder " + parameters['subfolder'] + " does not exist.")
		#	sys.exit('Aborting')
		
		for i in posting_files:
			
			if (parameters['subfolder']):
				full_path = parameters['subfolder'] + "/" + posting_files[i]['file']
			else:
				full_path = posting_files[i]['file']

			if not (s3_connection.object_exists(full_path)):
					functions.log("File " + full_path + " does not exist.");
					sys.exit('Aborting')

		if (my_profile.get_seperate_emails()):
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
		else:
			emails[0] = {}
			emails[0]['to'] = options.email
			emails[0]['files'] = posting_files
			if (my_profile.get_url_expires() > 0):
				for k in emails[0]['files']:
					s3_path = emails[k]['files'][uploaded_files]['file']
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
