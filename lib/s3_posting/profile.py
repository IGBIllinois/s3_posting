
import os.path

class profile:

	profile_file = ""
	endpoint_url = ""
	region = ""
	enable_url = True
	url_expires = 7
	access_key_id = ""
	secret_access_key = ""
	bucket = ""
	storage_class = "STANDARD"
	email_enable = True
	smtp_server = ""
	email_from = ""
	cc_emails = ""
	reply_to = ""
	subject = ""
	seperate_emails = False	


	def __init__(self,profile_file):
		self.profile_file = profile_file

	def get_endpoint_url(self):
		return self.endpoint_url

	def get_region(self):
		return self.region

	def get_enable_url(self):
		return self.enable_url

	def get_url_expires(self):
		return self.url_expires

	def get_access_key_id(self):
		return self.access_key_id

	def get_secret_access_key(self):
		return self.secret_access_key

	def get_bucket(self):
		return self.bucket

	def get_storage_class(self):
		return self.storage_class

	def get_email_enabled(self):
		return self.email_enable

	def get_smtp_server(self):
		return self.smtp_server

	def get_email_from(self):
		return self.email_from

	def get_cc_emails(self):
		return self.cc_emails

	def get_reply_to(self):
		return self.reply_to

	def get_subject(self):
		return self.subject

	def get_seperate_emails(self):
		return self.seperate_emails


