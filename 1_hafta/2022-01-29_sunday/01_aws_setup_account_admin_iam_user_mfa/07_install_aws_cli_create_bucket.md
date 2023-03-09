# Install AWS CLI on CentOS7

## 1. Install 
```
cd ~
sudo yum -y install unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## 2. Check version
```
(base) [train@localhost ~]$ aws --version
```
- Expected output

` aws-cli/2.4.19 Python/3.8.8 Linux/3.10.0-1160.53.1.el7.x86_64 exe/x86_64.centos.7 prompt/off `

## 3. Learn Region
![ Learn Region](images/aws_regions.png 'Learn Region')

-----------------------------------------------

## 4. Configure
### 4.1. default profile
```
aws configure
AWS Access Key ID [None]: <your key here>
AWS Secret Access Key [None]: <your secret key here>
Default region name [None]: eu-central-1
Default output format [None]: json
```

### 4.2. named profile
```commandline
[train@trainvm ~]$ aws configure --profile minio
AWS Access Key ID [None]: root
AWS Secret Access Key [None]: root12345
Default region name [None]: 
Default output format [None]: json
```
- Check
```commandline
train@trainvm ~]$ cat /home/train/.aws/credentials
[default]
aws_access_key_id = <your key>
aws_secret_access_key = <your secret key>
[minio]
aws_access_key_id = root
aws_secret_access_key = root12345
```

## 5. Create a bucket
- You must specify unique bucket name. For example `<yourname>-vbo-de-bootcamp`
```
aws s3api create-bucket \
--bucket vbo-de-bootcamp \
--create-bucket-configuration LocationConstraint=eu-central-1
```

## 6. Check bucket from AWS Web Console
![Check bucket from AWS Web Console](../../02_collection/01_kinesis/images/54_bucket_on_web_console.png 'Check bucket from AWS Web Console')

-----------------------------------------------

## 7. Upload a file from local
```
echo "AWS S3 bucket test" > test.txt
aws s3 cp test.txt s3://vbo-de-bootcamp/s3-tests/test.txt
```

## 8. Check uploaded file
![Check uploaded file](images/bucket_file_copy_test.png 'Check uploaded file')

-----------------------------------------------