#!/bin/bash
set -e

echo "Deploying IntelliNemo Agent with unique names..."

# Generate unique suffix
SUFFIX=$(date +%s)

# Deploy with unique names
aws cloudformation create-stack \
    --stack-name intellinemo-hackathon-${SUFFIX} \
    --template-body file://infrastructure/cloudformation/simple-stack.json \
    --capabilities CAPABILITY_IAM \
    --region us-east-1 \
    --parameters ParameterKey=NvidiaApiKey,ParameterValue=dummy-key-for-demo

echo "Stack intellinemo-hackathon-${SUFFIX} created!"