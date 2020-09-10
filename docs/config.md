# Configuration

## S3 User
- You need to create a S3 user with read/write permissions to the bucket.
- For Amazon, a user can be created in IAM.  Then a bucket policy can be applied in S3
- An example policy is below.  Replace <ORGID> and <BUCKETNAME> with your organization id and name of the bucket
```
{
    "Statement": [
        {
	    "Sid": "ListObjectsInBucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<ORGID>:user/upload_user"
            },
            "Action": ["s3:ListBucket"],
            "Resource": "arn:aws:s3:::<BUCKETNAME>"
        },
	{
	    "Sid": "AllObjectActions",
	    "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<ORGID>:user/upload_user"
            },
            "Action": "s3:*Object",
            "Resource": "arn:aws:s3:::<BUCKETNAME>"
    ]
}
```

## Profiles
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


