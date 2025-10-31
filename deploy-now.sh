#!/bin/bash
set -e

echo "Deploying IntelliNemo Agent..."

# Deploy simple stack
aws cloudformation create-stack \
    --stack-name intellinemo-agent \
    --template-body file://infrastructure/cloudformation/simple-stack.json \
    --capabilities CAPABILITY_IAM

echo "Stack deploying... Check AWS Console"