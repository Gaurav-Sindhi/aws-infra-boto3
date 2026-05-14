import boto3
from config import *

ec2 = boto3.client('ec2', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)
iam = boto3.client('iam')

# ---------------- EC2 ----------------
def create_ec2():
    response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        MinCount=1,
        MaxCount=1
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 Created: {instance_id}")

# ---------------- S3 ----------------
def create_s3():
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': REGION
        }
    )
    print(f"S3 Bucket Created: {BUCKET_NAME}")

# ---------------- IAM ----------------
def create_iam():
    role_name = "boto3-demo-role"
    
    assume_role_policy = """{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }]
    }"""
    
    iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=assume_role_policy
    )
    
    print(f"IAM Role Created: {role_name}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("Creating AWS Infrastructure...\n")
    
    create_ec2()
    create_s3()
    create_iam()
    
    print("\nSetup Complete 🚀")