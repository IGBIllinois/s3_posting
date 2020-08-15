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
from s3_posting import profile

settings = {}
settings['bucket'] = ""
settings['region'] = ""
settings['access_key_id'] = None
settings['secret_access_key'] = None
settings['overwrite'] = False
settings['md5sum'] = False
settings['sha256sum'] = False
settings['url_expires'] = 0
settings['subfolder'] = None

posting_files = []
file_md5_checksums = {}
file_sha256_checksums = {}
url = {}

def main():
	
	global settings
	global posting_files
	global file_checksums
	global url

	my_profile = profile.profile(config_file)
	

if __name__ == '__main__':
	main()
