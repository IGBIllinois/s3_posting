import os.path
import validators
import yaml

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
	__valid_storage_classes = {'STANDARD',
			'REDUCED_REDUNDANCY',
			'STANDARD_IA',
			'ONEZONE_IA',
			'INTELLIGENT_TIERING',
			'GLACIER',
			'DEEP_ARCHIVE'
			}
	__email_enable = True
	__smtp_server = ""
	__email_from = ""
	__cc_emails = ""
	__reply_to = ""
	__subject = ""
	__seperate_emails = False	

##########Public Functions#########

	def __init__(self,profile_file):
		if os.path.isfile(profile_file) == False:
			print ("Error opening " + profile_file + "\n");
			return False
		with open(profile_file,'r') as ymlfile:
			try:
				self.__cfg = yaml.load(ymlfile,Loader=yaml.FullLoader)
			except yaml.YAMLError as exc:
				print ("Error Parsing " + profile_file + "\n");
				return false
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
		return False
	def __validate_config(in_cfg):
		success = True
		if (('region' not in in_cfg['aws']) or (in_cfg['aws']['region'] == None)):
			success = False

		return success

	def __validate_email(email):
		if not validators.email(email):
			return False
		return True

