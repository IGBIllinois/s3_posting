# Configuration

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

