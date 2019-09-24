# S3 Posting
- Posts data to AWS S3 bucket through linux command line
- Emails user with the location of the data
- Generates md5sum of the file
## Installation
- Install boto3 and validators
```
pip install boto3 validators
```
- Copy config/config-default.yaml to config/config.yaml
- Edit config/config.yaml to have defaults for AWS bucket and email server
```
aws:
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
[root@compute-0 bin]# ./upload.py
Usage: upload.py [options] arg

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Filename to upload
  -d DIR, --dir=DIR     Directory to upload
  --email=EMAIL         Email to send to
  --cc=CC               Email address to cc
  -b BUCKET, --bucket=BUCKET
                        Bucket to upload to
  --checksum            Create file checksums
  --dry-run             Dry Run.  Disable uploads and emails
```
