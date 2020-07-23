import sys
import os.path
import threading
import subprocess
import boto3
import botocore
from botocore.client import Config
from urllib.parse import urlencode

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
	
	signature_version = "s3v4"

	def __init__(self,region,access_key_id,secret_access_key,bucket,endpoint_url):
		self._region = region
		self._access_key_id = access_key_id
		self._secret_access_key = secret_access_key
		self._bucket = bucket
		self._endpoint_url = endpoint_url
		self.connect()

	def bucket_exists(self):
        	response = self._connection.list_buckets()
	        buckets = [bucket['Name'] for bucket in response['Buckets']]
        	if self._bucket in buckets:
	                return True
        	return False

	def upload_file(self,file_path,directory):
		basename = os.path.basename(file_path);
		if (directory != None):
			full_path = directory + "/" + basename
		else:
			full_path = basename
		try:
        	        response = self._connection.upload_file(file_path,self._bucket,full_path,Callback=ProgressPercentage(file_path))
		except botocore.exceptions.ClientError as e:
        	        error_code = int(e.response['Error']['Code'])
                	functions.log("Error uploading file " + file_path + ", Error Code: " + str(error_code))
	                return error_code
		print (response)
		return True

	def get_url(self,filename,url_expires=0,custom_param=''):
		if (url_expires != 0):
	                seconds = url_expires * 24 * 60 * 60
        	        url = self._connection.generate_presigned_url('get_object',Params = {
                	        'Bucket': self._bucket,
                        	'Key': filename,
				'x-custom': custom_param},
	                        ExpiresIn = seconds)
		else:
                	url = self._connection.generate_presigned_url('get_object',Params = {
                        	'Bucket': self._bucket,
	                        'Key': filename,
				'x-custom': custom_param})

		return url

	def connect(self):
               	try:
                    self._connection = boto3.client('s3',endpoint_url=self._endpoint_url,region_name=self._region,aws_access_key_id=self._access_key_id,
                        aws_secret_access_key=self._secret_access_key,config=Config(signature_version=self.signature_version))
                    self._connection.meta.events.register("provide-client-params.s3.GetObject", self.client_param_handler)
                    self._connection.meta.events.register("before-sign.s3.GetObject", self.request_param_injector)
                except botocore.exceptions.ClientError as e:
                    error_code = int(e.response['Error']['Code'])
                    functions.log("Unable to connect to AWS S3, Error Code: " .  str(error_code))
                    return error_code
                return True

	def create_directory(self,directory):
		if (directory != None):
	        	try:
		                response = self._connection.put_object(Bucket=self._bucket,Key=directory + "/")
        		except botocore.exceptions.ClientError as e:
                		error_code = int(e.response['Error']['Code'])
		                functions.log("Error Creating Directory " + directory + ", Error Code: " + str(error_code))
        		        return error_code
	        	return True
		

	def directory_exists(self,directory):
		if (directory != None):
	        	try:
        	        	response = self._connection.list_objects_v2(Bucket=self._bucket,Prefix=directory + "/")
	        	except botocore.exceptions.ClientError as e:
        	        	error_code = int(e.response['Error']['Code'])
	                	functions.log("Error Checking Directory " + directory + ", Error Code: " + str(error_code))

		        return 'Contents' in response
		else:
			return True	


	# To add custom parameters to presigned url
	# https://stackoverflow.com/questions/59056522/create-a-presigned-s3-url-for-get-object-with-custom-logging-information-using-b
	def is_custom(self,k):
		return k.lower().startswith("x-")

	def client_param_handler(self, *, params, context, **_kw):
		# Store custom parameters in context for later event handlers
		context["custom_params"] = {k: v for k, v in params.items() if self.is_custom(k)}
		# Remove custom parameters from client parameters,
		# because validation would fail on them
		return {k: v for k, v in params.items() if not self.is_custom(k)}

	def request_param_injector(self, *, request, **_kw):
		if request.context["custom_params"]:
			request.url += "&" if "?" in request.url else "?"
			request.url += urlencode(request.context["custom_params"])

