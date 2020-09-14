# Configuration

## S3 User
- You need to create a S3 user with read/write permissions to the bucket.
- For Amazon, a user can be created in IAM.  Then a bucket policy can be applied in S3
- An example for AWS policy is below.  Replace \<ORGID\>, \<USERNAME\>, \<BUCKETNAME\> with your organziation ID, username, and name of bucket
```
{
    "Statement": [
        {
	    "Sid": "ListObjectsInBucket",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<ORGID>:user/<USERNAME>"
            },
            "Action": ["s3:ListBucket"],
            "Resource": "arn:aws:s3:::<BUCKETNAME>"
        },
	{
	    "Sid": "AllObjectActions",
	    "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<ORGID>:user/<USERNAME>"
            },
            "Action": "s3:*Object",
            "Resource": "arn:aws:s3:::<BUCKETNAME>"
    ]
}
```
- For Minio, the policy is simplified as it doesn't have the Principal setting.  In Minio, you specify which user/group the policy should apply to using the mc admin console
```
{
    "Statement": [
        {
            "Sid": "ListObjectsInBucket",
            "Effect": "Allow",
            "Action": ["s3:ListBucket", "s3:*Object"],
            "Resource": "arn:aws:s3:::<BUCKETNAME>"
        }
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
    cc_emails: []
    reply_to:
    subject:
    #Send seperate emails with unique presigned url for each email address Default: false
    seperate_emails: false
```
* aws
   * endpoint_url - URL to send the data.  For Amazon, it will be in the form of https://s3.us-east-1.amazonaws.com
   * region - S3 Region - List of Amazon regions is at https://docs.aws.amazon.com/general/latest/gr/rande.html
   * url_expires - Days - Maximum of 7 days.  Set to 0 to disable url generation
   * access_key_id - User Access Key.  For Amazon, this is set in IAM
   * secret_access_key - User Secret Key.  Form Amazon, this is set in IAM 
   * default_bucket - Default bucket name to use
   * storage_class - S3 Storage class to use.  STANDARD,REDUCED_REDUNDANCY,STANDARD_IA,ONEZONE_IA,INTELLIGENT_TIERING,GLACIER,DEEP_ARCHIVE
* email
   * enable - enable sending of emails with the unique url to download file
   * smtp_server - hostname of the mail server to use
   * from - email address for the FROM field
   * cc_emails - list of emails to CC
   * reply_to - email address for the reply to field
   * subject - Subject of the email
   * seperate_emails - Send one email to all the specified to: emails or send seperate emails to each to: with unique URLS for each one


