#!/usr/bin/env python

import sys
import os.path
import glob
from optparse import OptionParser

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir + "/lib")

import s3_posting
from s3_posting import profile
from s3_posting import functions

def main():
	
	global settings
	global posting_files
	global file_checksums
	global url

	description = "Tests Profile for proper formatting\n"
	description += functions.get_website()
	parser = OptionParser(description=description,version=functions.get_version())
	parser.add_option("-p","--profile",type="string",help="Profile to use");
	(options,args) = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()
		quit(1)

	profile_file = root_dir + "/config/" + options.profile + ".yaml"	
	my_profile = profile.profile(profile_file)
	my_profile.print_profile()
	

if __name__ == '__main__':
	main()
