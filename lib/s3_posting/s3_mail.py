import os.path
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

class s3_mail:

	subject = "Sequence files from University of Illinois DNA Sequencing Lab"
	template_dir = 'templates'
	template_txt = 'email.txt'
	template_html = 'email.html'

	def __init__(self,email,cc,url,md5sum,sha256sum,cfg):
		file_loader = FileSystemLoader(template_dir)
		self.template_env = Environment(loader=file_loader)
		self.email = email
		self.cc = cc
		self.url = url
		self.md5sum = md5sum
		self.sha256sum = sha256sum
		self.cfg = cfg

	def html_email():
		template = self.template_env.get_template('default/' + self.template_html)
		if (os.path.exists("../../templates/custom/" + self.template_html):
			template = self.template_env.get_template('custom/' + self.template_html)
		output = template.render(expire_date=self.expire_date,self.url)
		return output

	def text_email(url,md5sum,sha256sum,expire_date):
                template = self.template_env.get_template('default/' + self.template_txt)
                if (os.path.exists("../../templates/custom/" + self.template_txt):
                        template = self.template_env.get_template('custom/' + self.template_txt)
                output = template.render(expire_date=self.expire_date,self.url)
                return output

	def send_email():
        	print ("cc" + ", ".join(self.cc) + "\n")
	        self.expire_date = datetime.date.today() + datetime.timedelta(+self.cfg['aws']['url_expires'])
        	formatted_expire_date = expire_date.strftime('%Y-%m-%d')
	        email_from = self.cfg['email']['from']
        	msg = MIMEMultipart('alternative')
	        msg['Subject'] = self.subject
        	msg['From'] = email_from
	        msg['To'] = self.email
        	msg['Cc'] = ", ".join(self.cc)
	        msg['Reply-to'] = self.cfg['email']['reply_to']
        	part1 = MIMEText(self.text_email(),'text')
	        part2 = MIMEText(self.html_email(),'html')
        	msg.attach(part1)
	        msg.attach(part2)
        	s = smtplib.SMTP(self.cfg['email']['smtp_server'])
	        envelop = [email] + self.cc
        	result = s.sendmail(email_from,envelop,msg.as_string())
	        s.quit

