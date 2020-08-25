import os.path
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

class s3_mail:

	__template_dir = 'templates'
	__template_txt = 'email.txt'
	__template_html = 'email.html'
	__emails = []
	__files = []
	
	def __init__(self,in_profile,in_emails,in_files):
		path = os.path.abspath(__file__)
		dir_path = os.path.dirname(path)
		file_loader = FileSystemLoader(dir_path + "/../../" + self.__template_dir)
		self.template_env = Environment(loader=file_loader)
		self.__profile = in_profile
		self.__emails = in_emails
		self.__files = in_files

	def html_email(self):
		template = self.template_env.get_template('default/' + self.__template_html)
		if (os.path.exists("../../templates/custom/" + self.__template_html)):
			template = self.template_env.get_template('custom/' + self.__template_html)
		try:
			output = template.render(files=self.__files)
		except TemplateError as e:
			sys.exit('Syntax Error in email template ' + self.__template_html)

		return output

	def text_email(self):
		template = self.template_env.get_template('default/' + self.__template_txt)
		if (os.path.exists("../../templates/custom/" + self.__template_txt)):
			template = self.template_env.get_template('custom/' + self.__template_txt)

		try:
			output = template.render(files=self.__files)
		except TemplateError as e:
			sys.exit('Syntax Error in email template ' + self.__template_txt)

		return output

	def send_email(self):
		if (self.__profile.get_cc_emails() != None):
			print ("cc: " + self.__profile.get_cc_emails() + "\n")
		self.expire_date = datetime.date.today() + datetime.timedelta(+self.__profile.get_url_expires())
		formatted_expire_date = self.expire_date.strftime('%Y-%m-%d')
		msg = MIMEMultipart('alternative')
		msg['Subject'] = self.__profile.get_subject()
		msg['From'] = self.__profile.get_from_email()
		msg['To'] = ''.join(self.__emails)
		if (self.cfg['email']['cc_emails'] != None):
			msg['Cc'] = self.cfg['email']['cc_emails']
		if (self.__profile.get_reply_to() != None):
			msg['Reply-to'] = self.__profile.get_reply_to()
		part1 = MIMEText(self.text_email(),'text')
		part2 = MIMEText(self.html_email(),'html')
		msg.attach(part1)
		msg.attach(part2)
		s = smtplib.SMTP(self.__profile.get_smtp_server())
		envelop = [self.__emails]
		if (self.__profile.get_cc_emails() != None):
			envelop += self.cfg['email']['cc_emails'].split(",")
		result = s.sendmail(self.__profile.get_from_email(),envelop,msg.as_string())
		s.quit

