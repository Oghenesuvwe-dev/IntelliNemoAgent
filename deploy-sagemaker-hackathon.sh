#!/bin/bash

# IntelliNemo Agent - Hackathon Compliant SageMaker Deployment
# Uses Llama-3.1-Nemotron-nano-8B-v1 + Retrieval NIM

set -e

echo "🏆 Deploying IntelliNemo Agent - Hackathon Compliant Version"
echo "📋 Requirements: Llama-3.1-Nemotron-nano-8B-v1 + Retrieval NIM on SageMaker"
echo "=" * 60

# Check prerequisites
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ Error: NVIDIA_API_KEY environment variable not set"
    echo "Please set: export NVIDIA_API_KEY=your_nvidia_api_key"
    exit 1
fi

# Configuration
STACK_NAME="intellinemo-agent-hackathon"
REGION=${AWS_DEFAULT_REGION:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "🔧 Configuration:"
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"
echo "   Account: $ACCOUNT_ID"

# Deploy SageMaker NIM stack
echo ""
echo "🚀 Deploying SageMaker NIMs..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/sagemaker-nim-stack.json \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        NvidiaApiKey=$NVIDIA_API_KEY \
        ModelName=intellinemo-hackathon \
    --capabilities CAPABILITY_IAM \
    --region $REGION

# Wait for endpoints to be ready
echo ""
echo "⏳ Waiting for SageMaker endpoints to be ready..."
aws sagemaker wait endpoint-in-service \
    --endpoint-name intellinemo-hackathon-endpoint \
    --region $REGION

aws sagemaker wait endpoint-in-service \
    --endpoint-name intellinemo-hackathon-retrieval-endpoint \
    --region $REGION

# Package and deploy Lambda with SageMaker integration
echo ""
echo "📦 Packaging Lambda function..."
cd lambda-package
cp ../src/lambda/sagemaker_lambda_function.py lambda_function.py

# Create deployment package
zip -r ../intellinemo-hackathon-lambda.zip . -x "*.pyc" "__pycache__/*"
cd ..

# Deploy Lambda
echo ""
echo "🔧 Deploying Lambda function..."
aws lambda create-function \
    --function-name intellinemo-agent-hackathon \
    --runtime python3.11 \
    --role arn:aws:iam::$ACCOUNT_ID:role/IntelliNemoLambdaRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://intellinemo-hackathon-lambda.zip \
    --timeout 300 \
    --environment Variables="{
        LLAMA_ENDPOINT=intellinemo-hackathon-endpoint,
        RETRIEVAL_ENDPOINT=intellinemo-hackathon-retrieval-endpoint,
        S3_BUCKET=intellinemo-agent-$ACCOUNT_ID-$REGION,
        MODE=DRY_RUN
    }" \
    --region $REGION || \

# Update if exists
aws lambda update-function-code \
    --function-name intellinemo-agent-hackathon \
    --zip-file fileb://intellinemo-hackathon-lambda.zip \
    --region $REGION

# Clean up
rm -f intellinemo-hackathon-lambda.zip

echo ""
echo "✅ HACKATHON DEPLOYMENT COMPLETE!"
echo "=" * 60
echo "🎯 Compliance Status:"
echo "   ✅ Agentic Application: IntelliNemo Agent"
echo "   ✅ Llama-3.1-Nemotron-nano-8B-v1: Deployed on SageMaker"
echo "   ✅ Retrieval NIM: nv-embedqa-e5-v5 on SageMaker"
echo "   ✅ SageMaker Deployment: Both NIMs running"
echo ""
echo "📊 Endpoints:"
echo "   Llama NIM: intellinemo-hackathon-endpoint"
echo "   Retrieval NIM: intellinemo-hackathon-retrieval-endpoint"
echo ""
echo "💰 Estimated Cost: ~$13/day (within $100 hackathon budget)"
echo ""
echo "🧪 Test the deployment:"
echo "   aws lambda invoke --function-name intellinemo-agent-hackathon --payload '{}' response.json"
echo ""
echo "🏆 Ready for hackathon submission!"