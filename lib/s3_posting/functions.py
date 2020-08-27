import sys
import os.path
import datetime
import subprocess
import validators

from s3_posting import __version__
from s3_posting import __website__

def get_version():
	return __version__

def get_website():
	return __website__

def create_md5_checksum(file_path):
	cmd = "md5sum " + file_path + " | awk '{print $1}'"
	p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	stdout,stderr = p.communicate()
	if (p.returncode):
		return False
	else:
		return stdout.strip().rstrip() 
	
def create_sha256sum_checksum(file_path):
        cmd = "sha256sum " + file_path + " | awk '{print $1}'"
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        stdout,stderr = p.communicate()
        if (p.returncode):
                return False
        else:
                return stdout.strip().rstrip()

def log(msg):
	now = datetime.datetime.now()
	formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
	print (formatted_time + ": " + msg)

		
def get_files_in_dir(path):
	file_paths = []

	for folder, subs, files in os.walk(path):
		for filename in files:
			file_paths.append(os.path.abspath(os.path.join(folder, filename)))
	if len(file_paths) > 0:
		return file_paths
	else:
		return False

def validate_email(email):
        if not validators.email(email):
                return False
        return True
