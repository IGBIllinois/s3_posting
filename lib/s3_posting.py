import sys
import os.path
import threading
import subprocess
import boto3
import botocore
from botocore.client import Config


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

class s3_posting:
	
	signature_version = "s3"

	def __init__(self,region,access_key_id,secret_access_key,bucket):
		self._region = region
		self._access_key_id = access_key_id
		self._secret_access_key = secret_access_key
		self._bucket = bucket
		self.connect()

	def bucket_exists(self):
        	response = self._connection.list_buckets()
	        buckets = [bucket['Name'] for bucket in response['Buckets']]
        	if self._bucket in buckets:
	                return True
        	return False

	def upload_file(self,file_path,directory):
        	basename = os.path.basename(file_path);
	        try:
        	        response = self._connection.upload_file(file_path,self._bucket,directory + "/" + basename,Callback=ProgressPercentage(file_path))
	        except botocore.exceptions.ClientError as e:
        	        error_code = int(e.response['Error']['Code'])
                	functions.log("Error uploading file " + file_path + ", Error Code: " + str(error_code))
	                return error_code
        	print response
	        return True

	def get_url(self,filename,url_expires=0):
        	if (url_expires != 0):
	                seconds = url_expires * 24 * 60 * 60
        	        url = self._connection.generate_presigned_url('get_object',Params = {
                	        'Bucket': self._bucket,
                        	'Key': filename},
	                        ExpiresIn = seconds)
        	else:
                	url = self._connection.generate_presigned_url('get_object',Params = {
                        	'Bucket': self._bucket,
	                        'Key': filename})
        	return url

	def connect(self):
               	try:
			self._connection = boto3.client('s3',self._region,
				aws_access_key_id=self._access_key_id,
				aws_secret_access_key=self._secret_access_key,
				config=Config(signature_version=self.signature_version))
		except botocore.exceptions.ClientError as e:
			error_code = int(e.response['Error']['Code'])
			functions.log("Unable to connect to AWS S3, Error Code: " .  str(error_code))
			return error_code
	        return True

	def create_directory(self,directory):
        	try:
	                response = self._connection.put_object(Bucket=self._bucket,Key=directory + "/")
        	except botocore.exceptions.ClientError as e:
                	error_code = int(e.response['Error']['Code'])
	                functions.log("Error Creating Directory " + directory + ", Error Code: " + str(error_code))
        	        return error_code
	        return True

	def directory_exists(self,directory):
        	try:
                	response = self._connection.list_objects(Bucket=self._bucket,Prefix=directory + "/")
	        except botocore.exceptions.ClientError as e:
        	        error_code = int(e.response['Error']['Code'])
                	functions.log("Error Checking Directory " + directory + ", Error Code: " + str(error_code))

	        return 'Contents' in response


