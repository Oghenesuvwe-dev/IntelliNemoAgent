#!/bin/bash
set -e

echo "Deploying IntelliNemo Agent to hackathon account..."

# Configure AWS CLI for this account
export AWS_DEFAULT_REGION=us-east-1

# Deploy the hackathon stack with dummy NVIDIA API key
aws cloudformation create-stack \
    --stack-name intellinemo-hackathon-demo \
    --template-body file://infrastructure/cloudformation/simple-stack.json \
    --capabilities CAPABILITY_IAM \
    --region us-east-1 \
    --parameters ParameterKey=NvidiaApiKey,ParameterValue=dummy-key-for-demo

echo "Stack created! Check CloudFormation console for progress."