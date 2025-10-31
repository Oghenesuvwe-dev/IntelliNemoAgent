#!/bin/bash

# Quick deployment script for AWS lab environment
set -e

echo "Starting IntelliNemo Agent deployment..."

# Check if lab is started
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "Please start the AWS lab and configure credentials first"
    exit 1
fi

# Deploy basic infrastructure
echo "Deploying CloudFormation stack..."
aws cloudformation create-stack \
    --stack-name intellinemo-agent \
    --template-body file://infrastructure/cloudformation/simple-stack.json \
    --capabilities CAPABILITY_IAM

# Wait for stack creation
echo "Waiting for stack creation..."
aws cloudformation wait stack-create-complete --stack-name intellinemo-agent

echo "Deployment complete! Check CloudWatch for alarms and Lambda logs."