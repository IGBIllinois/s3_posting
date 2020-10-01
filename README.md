# S3 Posting

[![Build Status](https://www.travis-ci.com/IGBIllinois/s3_posting.svg?branch=master)](https://www.travis-ci.com/IGBIllinois/s3_posting)

- Posts data to S3 buckets through linux command line
- Works with AWS, [https://aws.amazon.com/](https://aws.amazon.com/) and Minio, [https://min.io/](https://min.io/)
- Supports standard S3, Glacier, and Deep Glacier
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

## Configuration
How to configure the profiles is explained at [docs/config.md](docs/config.md)

## Usage
How to use the program is explained at [docs/usage.md](docs/usage.md)
