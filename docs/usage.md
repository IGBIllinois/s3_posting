# Usage

## upload.py

```
Usage: upload.py [options]

Posts data to S3 buckets through linux command line
https://github.com/IGBIllinois/s3_posting

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROFILE, --profile=PROFILE
                        Profile to use (posting, deepglacier, s3)
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

## generate_url.py
```
Usage: generate_url.py [options]

Regenerates unique URL for existing S3 file
https://github.com/IGBIllinois/s3_posting

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROFILE, --profile=PROFILE
                        Profile to use (posting, deepglacier, s3)
  -f FILE, --file=FILE  Filename to generate URL
  -d DIR, --dir=DIR     Directory to generate URL
  -e EMAIL, --email=EMAIL
                        Email to send to
  -b BUCKET, --bucket=BUCKET
                        Bucket to upload to
  -s SUBFOLDER, --subfolder=SUBFOLDER
                        Folder to place object in
  --dry-run             Dry Run. Disable generate URL and emails
```

## test_profile.py
```
Usage: test_profile.py [options]

Tests Profile for proper formatting https://github.com/IGBIllinois/s3_posting

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROFILE, --profile=PROFILE
                        Profile to use (posting, deepglacier, s3)
```
