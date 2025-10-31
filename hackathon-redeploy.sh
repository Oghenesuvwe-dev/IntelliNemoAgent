#!/bin/bash
set -e

echo "Deploying IntelliNemo to hackathon account 8833-2360-5108..."

# Check current account
ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text 2>/dev/null || echo "Not configured")
echo "Current account: $ACCOUNT"

if [ "$ACCOUNT" != "883323605108" ]; then
    echo "ERROR: Configure AWS CLI for hackathon account first"
    echo "Get credentials from AWS lab and run:"
    echo "export AWS_ACCESS_KEY_ID=..."
    echo "export AWS_SECRET_ACCESS_KEY=..."
    echo "export AWS_SESSION_TOKEN=..."
    echo "export AWS_DEFAULT_REGION=us-east-1"
    exit 1
fi

# Deploy to hackathon account
aws cloudformation create-stack \
    --stack-name intellinemo-hackathon-team94 \
    --template-body file://infrastructure/cloudformation/simple-stack.json \
    --capabilities CAPABILITY_IAM \
    --region us-east-1 \
    --parameters ParameterKey=NvidiaApiKey,ParameterValue=demo-key-team94

echo "IntelliNemo deployed to hackathon account!"