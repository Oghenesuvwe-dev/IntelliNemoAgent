#!/bin/bash

# IntelliNemo Agent - Complete Deployment
set -e

PROJECT_NAME="intellinemo-agent"
REGION="us-east-1"

echo "🧠 Deploying Complete IntelliNemo Agent Infrastructure"

# Check NVIDIA API key
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ Error: NVIDIA_API_KEY required"
    echo "Set with: export NVIDIA_API_KEY=your_key"
    exit 1
fi

# Deploy complete stack
echo "☁️ Deploying complete infrastructure..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/complete-intellinemo-stack.json \
    --stack-name ${PROJECT_NAME}-complete \
    --parameter-overrides \
        NvidiaApiKey=${NVIDIA_API_KEY} \
        ProjectName=${PROJECT_NAME} \
    --capabilities CAPABILITY_NAMED_IAM \
    --region ${REGION}

# Get outputs
echo "📋 Getting deployment outputs..."
aws cloudformation describe-stacks \
    --stack-name ${PROJECT_NAME}-complete \
    --query 'Stacks[0].Outputs' \
    --region ${REGION}

echo "✅ Complete IntelliNemo Agent deployed!"
echo "💰 Monthly cost: ~$512.94 (SageMaker endpoints)"
echo "🎯 Features: Nano-8B + Nemo Retriever + Full automation"