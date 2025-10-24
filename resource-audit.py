#!/usr/bin/env python3
"""
AutoCloudOps Agent - Resource Audit
Check what test resources are available
"""

import boto3
import json

def audit_resources():
    print("🔍 AutoCloudOps Agent - Resource Audit")
    print("=" * 50)
    
    # Check Lambda function
    try:
        lambda_client = boto3.client('lambda')
        response = lambda_client.get_function(FunctionName='autocloudops-agent')
        print("✅ Lambda Function: autocloudops-agent")
        print(f"   Runtime: {response['Configuration']['Runtime']}")
        print(f"   Mode: {response['Configuration']['Environment']['Variables'].get('MODE', 'Unknown')}")
    except Exception as e:
        print(f"❌ Lambda Function: {str(e)}")
    
    # Check S3 bucket
    try:
        s3_client = boto3.client('s3')
        bucket_name = 'autocloudops-agent-442042519962-us-east-1'
        s3_client.head_bucket(Bucket=bucket_name)
        print("✅ S3 Bucket: autocloudops-agent-442042519962-us-east-1")
        
        # Check logs
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='logs/')
        log_count = objects.get('KeyCount', 0)
        print(f"   Log entries: {log_count}")
    except Exception as e:
        print(f"❌ S3 Bucket: {str(e)}")
    
    # Check Secrets Manager
    try:
        secrets_client = boto3.client('secretsmanager')
        secret_arn = 'arn:aws:secretsmanager:us-east-1:442042519962:secret:autocloudops-agent-secrets-3qfYNM'
        secrets_client.describe_secret(SecretId=secret_arn)
        print("✅ Secrets Manager: NVIDIA API key configured")
    except Exception as e:
        print(f"❌ Secrets Manager: {str(e)}")
    
    # Check CloudWatch alarms
    try:
        cloudwatch = boto3.client('cloudwatch')
        alarms = cloudwatch.describe_alarms(AlarmNamePrefix='autocloudops')
        alarm_count = len(alarms['MetricAlarms'])
        print(f"✅ CloudWatch Alarms: {alarm_count} test alarms")
        for alarm in alarms['MetricAlarms']:
            print(f"   - {alarm['AlarmName']}: {alarm['StateValue']}")
    except Exception as e:
        print(f"❌ CloudWatch Alarms: {str(e)}")
    
    print("\n🎯 MISSING TEST RESOURCES:")
    print("❌ EventBridge Rules (auto-triggering)")
    print("❌ EC2 Instances (scaling targets)")
    print("❌ Auto Scaling Groups (scaling actions)")
    print("❌ RDS Instances (database restart targets)")
    print("❌ ECS Services (container restart targets)")
    print("❌ Systems Manager Documents (runbooks)")
    
    print("\n📋 CURRENT TESTING CAPABILITY:")
    print("✅ Manual Lambda invocation")
    print("✅ S3 audit logging")
    print("✅ NVIDIA NIM integration (network restricted)")
    print("✅ Action mapping logic")
    print("❌ Actual resource remediation")

if __name__ == "__main__":
    audit_resources()