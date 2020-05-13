import os.path
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

class email:

	subject = "Sequence files from University of Illinois DNA Sequencing Lab"
	template_dir = "templates"

	def __init__(self,email,cc,url,md5sum,sha256sum,cfg):
		file_loader = FileSystemLoader(template_dir)
		self.template_env = Environment(loader=file_loader)
		self.email = email
		self.cc = cc
		self.url = url
		self.md5sum = md5sum
		self.sha256sum = sha256sum
		self.cfg = cfg

	def html_email(url,md5sum,sha256sum,expire_date):
        	html = "<html><head></head><body>"
        html += "<p>Hi,</p>"
        html += "<p>Your sequencing results from the DNA Sequencing lab at UIUC are available for download.</p>"
        html += "<p>Below is the list of files and the link to download them.</p>"
        html += "<p>The links (URLs) will expire on " + expire_date + "</p>"
        html += "<br>"
        for file_name,url_link in url.items():
                html += "<p>File: " + os.path.basename(file_name) + "</p>"
                html += "<p>URL: <a href='" + url_link + "'>" + url_link + "</a></p>"
                if len(md5sum):
                        html += "<p>md5sum: " + str(md5sum[file_name].decode("utf-8")) + "</p>"
        html += "<p>For questions about this posting, you may reply to this email and must cc: aghernan@illinois.edu and clwright@illinois.edu</p>"
        html += "<p>Sincerely,</p>"
        html += "<p>The DNA Sequencing Lab, University of Illinois at Urbana-Champaign</p>"
        html += "</body></html>"
        return html

	def text_email(url,md5sum,sha256sum,expire_date):
        text = "Hi,\n\n"
        text += "Your sequencing results from the DNA Sequencing lab at UIUC are available for download.\n\n"
        text += "Below is the list of files and the link to download them.\n\n"
        text += "The links (URLs) will expire on " + expire_date + "\n\n" 
        for file_name, url_link in url.items():
                text += "File: " + os.path.basename(file_name) + "\n\n"
                text += "URL: " + url_link + "\n\n"
                if len(md5sum):
                        text += "md5sum: " + str(md5sum[file_name].decode("utf-8")) + "\n\n"

        text += "For questions about this posting, you may reply to this email and must cc: aghernan@illinois.edu and clwright@illinois.edu\n\n"
        text += "Sincerely,\n\n";
        text += "The DNA Sequencing Lab, University of Illinois at Urbana-Champaign\n\n"

        return text

	def send_email():
        	print ("cc" + ", ".join(self.cc) + "\n")
	        expire_date = datetime.date.today() + datetime.timedelta(+self.cfg['aws']['url_expires'])
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

