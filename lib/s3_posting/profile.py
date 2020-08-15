import os.path
import validators
import yaml
import json
import jsonschema

class profile:

########Class Variables#########
	__profile_file = ""
	__cfg = ""
	__endpoint_url = ""
	__region = ""
	__enable_url = True
	__url_expires = 7
	__access_key_id = ""
	__secret_access_key = ""
	__bucket = ""
	__storage_class = "STANDARD"
	__email_enable = True
	__smtp_server = ""
	__email_from = ""
	__cc_emails = ""
	__reply_to = ""
	__subject = ""
	__seperate_emails = False	
	__profile_schema = os.path.dirname(__file__) + "/profile_schema.json"

##########Public Functions#########

	def __init__(self,profile_file):
		if os.path.isfile(profile_file) == False:
			print ("Error " + profile_file + " does not exist");
			exit(1)
		with open(profile_file,'r') as ymlfile:
			try:
				self.__cfg = yaml.load(ymlfile,Loader=yaml.FullLoader)
			except yaml.YAMLError as exc:
				print ("Error Parsing " + profile_file)
				exit(1)

			try:
				with open(self.__profile_schema,'r') as f:
					schema = json.load(f)
					jsonschema.validate(self.__cfg,schema)

			except jsonschema.exceptions.ValidationError as exc:
				print ("Error Validating " + profile_file)
				print(exc.message)
				exit(1)

			self.__profile_file = profile_file

	def get_endpoint_url(self):
		return self.__endpoint_url

	def get_region(self):
		return self.__region

	def get_enable_url(self):
		return self.__enable_url

	def get_url_expires(self):
		return self.__url_expires

	def get_access_key_id(self):
		return self.__access_key_id

	def get_secret_access_key(self):
		return self.__secret_access_key

	def get_bucket(self):
		return self.__bucket

	def get_storage_class(self):
		return self.__storage_class

	def get_email_enabled(self):
		return self.__email_enable

	def get_smtp_server(self):
		return self.__smtp_server

	def get_email_from(self):
		return self.__email_from

	def get_cc_emails(self):
		return self.__cc_emails

	def get_reply_to(self):
		return self.__reply_to

	def get_subject(self):
		return self.__subject

	def get_seperate_emails(self):
		return self.__seperate_emails

##########Private Functions###########
	def __load_profile(self):
		if ("endpoint_url" in __cfg['aws']):
			__endpoint_url = __cfg['aws']['endpoint_url']
		if ("region" in __cfg['aws']):
			__region = __cfg['aws']['region']
		if ("url_expires" in __cfg['aws']):
			__url_expires = __cfg['aws']['url_expires']
		if ("access_key_id" in __cfg['aws']):
			__access_key_id = __cfg['aws']['access_key_id']
		if ("secret_access_key" in __cfg['aws']):
			__secret_access_key = __cfg['aws']['secret_access_key']
		if ("default_bucket" in __cfg['aws']):
			___bucket = __cfg['aws']['default_bucket']
		if ("enable_url" in __cfg['aws']):
			__enable_url = __cfg['aws']['enable_url']
		if ("storage_class" in __cfg['aws']):
			__storage_class = __cfg['aws']['storage_class']
		if ("enable" in __cfg['email']):
			__enable_email = __cfg['email']['enable']
		if ("smtp_server" in __cfg['email']):
			__smtp_server = __cfg['email']['smtp_server']
		if ("from" in __cfg['email']):
			__email_from = __cfg['email']['from']
		if ("cc_emails" in __cfg['email']):
			__cc_emails = __cfg['email']['cc_emails']
		if ("reply_to" in __cfg['email']):
			__reply_to = __cfg['email']['reply_to']
		if ("subject" in __cfg['subject']):
			__subject = __cfg['email']['subject']
		if ("seperate_emails" in __cfg['email']):
			__seperate_emails = __cfg['email']['seperate_emails']

	def __validate_config(in_cfg):
		success = True
		if (('region' not in in_cfg['aws']) or (in_cfg['aws']['region'] == None)):
			success = False

		return success

	def __validate_email(email):
		if not validators.email(email):
			return False
		return True

