# S3 Posting

[![Build Status](https://www.travis-ci.com/IGBIllinois/s3_posting.svg?branch=master)](https://www.travis-ci.com/IGBIllinois/s3_posting)

- Posts data to S3 buckets through linux command line
- Works with AWS, [https://aws.amazon.com/](https://aws.amazon.com/) and Minio, [https://min.io/](https://min.io/)
- Emails user with the location of the data
- Generates md5sum and/or sha256 checksums of the file
## Installation
- Install using virtualenv
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```
- Or Install directly into python
```
pip install -r requirements.txt
```
- Download Code using a tag release or git clone
```
git clone https://github.com/IGBIllinois/s3_posting.git
```
- Copy config/config.yaml.dist to config/config.yaml
- Edit config/config.yaml to have defaults for AWS bucket and email server
```
aws:
	endpoint_url:
        region: us-east-1
        url_expires: 30
        access_key_id: 
        secret_access_key: 
        default_bucket: 

email:
        smtp_server: 
        from: 
        cc_emails: 
        reply_to: 
```

## Usage
```
[root@localhost bin]# ./upload.py
Usage: upload.py [options]

Posts data to S3 buckets through linux command line
https://github.com/IGBIllinois/s3_posting

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Filename to upload
  -d DIR, --dir=DIR     Directory to upload
  --email=EMAIL         Email to send to
  --cc=CC               Email address to cc
  -b BUCKET, --bucket=BUCKET
                        Bucket to upload to
  --md5                 Create md5 checksums
  --sha256              Create sha256 checksums
  --dry-run             Dry Run. Disable uploads and emails
```
