# S3 Posting

[![Build Status](https://www.travis-ci.com/IGBIllinois/s3_posting.svg?branch=master)](https://www.travis-ci.com/IGBIllinois/s3_posting)

- Posts data to S3 buckets through linux command line
- Works with AWS, [https://aws.amazon.com/](https://aws.amazon.com/) and Minio, [https://min.io/](https://min.io/)
- Emails user with the location of the data
- Generates md5sum and/or sha256 checksums of the file
## Installation
- Download Code using a tag release or git clone
```
git clone https://github.com/IGBIllinois/s3_posting.git
```
- Install using virtualenv
```
virtualenv .env && source .env/bin/activate && pip install -r requirements.txt
```
- Or Install directly into python
```
pip install -r requirements.txt
```

- Copy config/config.yaml.dist to config/config.yaml for the default profile
- Create other profiles by copying config/config.yaml.dist to config/<PROFILE_NAME>.yaml
- Edit config/config.yaml to have defaults for AWS bucket and email server
```
aws:
        endpoint_url:
        region: us-east-1
        #URL expiration. Maximum 7 days for signature version s3v4, set 0 to disable
        url_expires: 7
        access_key_id:
        secret_access_key:
        default_bucket:
        #STANDARD,REDUCED_REDUNDANCY,STANDARD_IA,ONEZONE_IA,INTELLIGENT_TIERING,GLACIER,DEEP_ARCHIVE Default: STANDARD
        storage_class: STANDARD

email:
        #Enable emails Default: true
        enable: true
        smtp_server:
        from:
        cc_emails:
        reply_to:
        subject:
        #Send seperate emails with unique presigned url for each email address Default: false
        seperate_emails: false
```

## Usage
```
Usage: upload.py [options]

Posts data to S3 buckets through linux command line
https://github.com/IGBIllinois/s3_posting

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROFILE, --profile=PROFILE
                        Profile to use
  -f FILE, --file=FILE  Filename to upload
  -d DIR, --dir=DIR     Directory to upload
  -e EMAIL, --email=EMAIL
                        Email to send to
  -b BUCKET, --bucket=BUCKET
                        Bucket to upload to
  -s SUBFOLDER, --subfolder=SUBFOLDER
                        Folder to place object in
  --md5                 Create md5 checksums
  --sha256              Create sha256 checksums
  -m METADATA, --metadata=METADATA
                        Key/values metadata to add to object
  --dry-run             Dry Run. Disable uploads and emails
```
