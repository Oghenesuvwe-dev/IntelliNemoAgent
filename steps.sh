#!/bin/bash

echo "Step 1: Start Lab"
echo "- Click 'Start lab' button"
echo "- Wait for green dot"
echo ""

echo "Step 2: Get AWS Credentials"
echo "- Click 'AWS CLI' text area"
echo "- Copy all 4 lines"
echo "- Paste in terminal:"
echo ""
echo "export AWS_ACCESS_KEY_ID=AKIA..."
echo "export AWS_SECRET_ACCESS_KEY=..."
echo "export AWS_SESSION_TOKEN=..."
echo "export AWS_DEFAULT_REGION=us-east-1"
echo ""

echo "Step 3: Test Connection"
echo "aws sts get-caller-identity"
echo ""

echo "Step 4: Check IntelliNemo Deployment"
echo "aws cloudformation describe-stacks --stack-name intellinemo-eks-hackathon"
echo ""

echo "Step 5: Get Lambda Function Details"
echo "aws lambda list-functions --query 'Functions[?contains(FunctionName, \`intellinemo\`)].{Name:FunctionName,Runtime:Runtime}' --output table"
echo ""

echo "Step 6: Check CloudWatch Alarms"
echo "aws cloudwatch describe-alarms --query 'MetricAlarms[?contains(AlarmName, \`intellinemo\`)].AlarmName'"