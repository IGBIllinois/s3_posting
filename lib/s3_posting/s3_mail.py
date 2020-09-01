import os.path
import datetime
import smtplib
import sys
import s3_posting
from s3_posting import functions
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

class s3_mail:

	__template_dir = 'templates'
	__template_txt = 'email.txt'
	__template_html = 'email.html'
	__email = {}
	
	def __init__(self,in_profile,in_email):
		path = os.path.abspath(__file__)
		dir_path = os.path.dirname(path)
		file_loader = FileSystemLoader(dir_path + "/../../" + self.__template_dir)
		self.template_env = Environment(loader=file_loader)
		self.__profile = in_profile
		self.__email = in_email

	def html_email(self):
		template = self.template_env.get_template('default/' + self.__template_html)
		if (os.path.exists("../../templates/custom/" + self.__template_html)):
			template = self.template_env.get_template('custom/' + self.__template_html)
		try:
			output = template.render(files=self.__email['files'])
		except TemplateError as e:
			sys.exit('Syntax Error in email template ' + self.__template_html)

		return output

	def text_email(self):
		template = self.template_env.get_template('default/' + self.__template_txt)
		if (os.path.exists("../../templates/custom/" + self.__template_txt)):
			template = self.template_env.get_template('custom/' + self.__template_txt)

		try:
			output = template.render(files=self.__email['files'])
		except TemplateError as e:
			sys.exit('Syntax Error in email template ' + self.__template_txt)

		return output

	def send_email(self):
		self.expire_date = datetime.date.today() + datetime.timedelta(+self.__profile.get_url_expires())
		formatted_expire_date = self.expire_date.strftime('%Y-%m-%d')
		msg = MIMEMultipart('alternative')
		msg['Subject'] = self.__profile.get_subject()
		msg['From'] = self.__profile.get_from_email()
		msg['To'] = ''.join(self.__email['to'])
		if (self.__profile.get_cc_emails() != None):
			msg['Cc'] = ', ' .join(self.__profile.get_cc_emails())
		if (self.__profile.get_reply_to() != None):
			msg['Reply-to'] = self.__profile.get_reply_to()
		part1 = MIMEText(self.text_email(),'text')
		part2 = MIMEText(self.html_email(),'html')
		msg.attach(part1)
		msg.attach(part2)

		try:
			s = smtplib.SMTP(self.__profile.get_smtp_server())
			envelop = [self.__email['to']]
			if (self.__profile.get_cc_emails() != None):
				envelop += ', ' .join(self.__profile.get_cc_emails())
			result = s.sendmail(self.__profile.get_from_email(),envelop,msg.as_string())
			s.quit
		except (OSError,smtplib.SMTPException) as e:
			functions.log('Error sending email')
			sys.exit()
