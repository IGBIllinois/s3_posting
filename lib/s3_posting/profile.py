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
	__url_expires = 7
	__access_key_id = ""
	__secret_access_key = ""
	__bucket = ""
	__storage_class = "STANDARD"
	__email_enable = False
	__smtp_server = ""
	__email_from = ""
	__cc_emails = []
	__bcc_emails = []
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
				print(exc.message)
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
			self.__load_profile()

	def get_endpoint_url(self):
		return self.__endpoint_url

	def get_region(self):
		return self.__region

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

	def get_from_email(self):
		return self.__email_from

	def get_cc_emails(self):
		return self.__cc_emails
	def get_bcc_emails(self):
		return self.__bcc_emails

	def get_reply_to(self):
		return self.__reply_to

	def get_subject(self):
		return self.__subject

	def get_seperate_emails(self):
		return self.__seperate_emails

	def print_profile(self):
		print(yaml.dump(self.__cfg))
	
##########Private Functions###########
	def __load_profile(self):
		if ("endpoint_url" in self.__cfg['aws']):
			self.__endpoint_url = self.__cfg['aws']['endpoint_url']
		if ("region" in self.__cfg['aws']):
			self.__region = self. __cfg['aws']['region']
		if ("url_expires" in self.__cfg['aws']):
			self.__url_expires =self. __cfg['aws']['url_expires']
		if ("access_key_id" in self.__cfg['aws']):
			self.__access_key_id = self.__cfg['aws']['access_key_id']
		if ("secret_access_key" in self.__cfg['aws']):
			self.__secret_access_key = self.__cfg['aws']['secret_access_key']
		if ("default_bucket" in self.__cfg['aws']):
			self.__bucket = self.__cfg['aws']['default_bucket']
		if ("storage_class" in self.__cfg['aws']):
			self.__storage_class = self.__cfg['aws']['storage_class']
		if ("enable" in self.__cfg['email']):
			self.__email_enable = self.__cfg['email']['enable']
		if ("smtp_server" in self.__cfg['email']):
			self.__smtp_server = self.__cfg['email']['smtp_server']
		if ("from" in self.__cfg['email']):
			self.__email_from = self.__cfg['email']['from']
		if ("cc_emails" in self.__cfg['email']):
			self.__cc_emails = self.__cfg['email']['cc_emails']
		if ("bcc_emails" in self.__cfg['email']):
			self.__bcc_emails = self.__cfg['email']['bcc_emails']
		if ("reply_to" in self.__cfg['email']):
			self.__reply_to = self.__cfg['email']['reply_to']
		if ("subject" in self.__cfg['email']):
			self.__subject = self.__cfg['email']['subject']
		if ("seperate_emails" in self.__cfg['email']):
			self.__seperate_emails = self.__cfg['email']['seperate_emails']

	def __validate_config(in_cfg):
		success = True
		if (('region' not in in_cfg['aws']) or (in_cfg['aws']['region'] == None)):
			success = False

		return success

	def __validate_email(email):
		if not validators.email(email):
			return False
		return True

