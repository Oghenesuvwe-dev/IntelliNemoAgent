#!/bin/bash

# IntelliNemo Agent - Hackathon Deployment
# Meets AWS x NVIDIA Hackathon Requirements

set -e

echo "🏆 IntelliNemo Agent - Hackathon Deployment"
echo "Requirements: Llama-3.1-Nemotron-nano-8B-v1 + Retrieval NIM on SageMaker"

# Set NVIDIA API key
NVIDIA_API_KEY="MmxtdHJyaTNpN2JnZTVuaTNuNThqbzVuOHY6ZTUyNjBhNGYtOGY1MC00ZTc2LWFjMzktNzUxODliYTM5ZTNh"

if [ -z "$NVIDIA_API_KEY" ] || [ "$NVIDIA_API_KEY" = "your_nvidia_api_key_here" ]; then
    echo "❌ Error: Update NVIDIA_API_KEY in deploy-hackathon.sh"
    echo "Edit line 12 with your actual NVIDIA API key"
    exit 1
fi

REGION=${AWS_DEFAULT_REGION:-us-east-1}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "Deploying to Account: $ACCOUNT_ID, Region: $REGION"

# Step 1: Deploy SageMaker NIMs
echo "Step 1: Deploying SageMaker NIMs..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/sagemaker-nim-stack.json \
    --stack-name intellinemo-hackathon-nims \
    --parameter-overrides \
        NvidiaApiKey=$NVIDIA_API_KEY \
        ModelName=intellinemo-hackathon \
    --capabilities CAPABILITY_IAM \
    --region $REGION

# Step 2: Wait for endpoints
echo "Step 2: Waiting for SageMaker endpoints..."
aws sagemaker wait endpoint-in-service \
    --endpoint-name intellinemo-hackathon-endpoint \
    --region $REGION

aws sagemaker wait endpoint-in-service \
    --endpoint-name intellinemo-hackathon-retrieval-endpoint \
    --region $REGION

# Step 3: Package Lambda with SageMaker integration
echo "Step 3: Packaging Lambda function..."
cd lambda-package
cp ../src/lambda/sagemaker_lambda_function.py lambda_function.py
zip -r ../hackathon-lambda.zip . -x "*.pyc" "__pycache__/*"
cd ..

# Step 4: Deploy/Update Lambda
echo "Step 4: Deploying Lambda function..."
aws lambda create-function \
    --function-name intellinemo-agent-hackathon \
    --runtime python3.11 \
    --role arn:aws:iam::$ACCOUNT_ID:role/IntelliNemoLambdaRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://hackathon-lambda.zip \
    --timeout 300 \
    --environment Variables="{
        LLAMA_ENDPOINT=intellinemo-hackathon-endpoint,
        RETRIEVAL_ENDPOINT=intellinemo-hackathon-retrieval-endpoint,
        S3_BUCKET=intellinemo-agent-$ACCOUNT_ID-$REGION,
        MODE=DRY_RUN,
        HACKATHON_COMPLIANT=true
    }" \
    --region $REGION 2>/dev/null || \

aws lambda update-function-code \
    --function-name intellinemo-agent-hackathon \
    --zip-file fileb://hackathon-lambda.zip \
    --region $REGION

aws lambda update-function-configuration \
    --function-name intellinemo-agent-hackathon \
    --environment Variables="{
        LLAMA_ENDPOINT=intellinemo-hackathon-endpoint,
        RETRIEVAL_ENDPOINT=intellinemo-hackathon-retrieval-endpoint,
        S3_BUCKET=intellinemo-agent-$ACCOUNT_ID-$REGION,
        MODE=DRY_RUN,
        HACKATHON_COMPLIANT=true
    }" \
    --region $REGION

# Cleanup
rm -f hackathon-lambda.zip

echo ""
echo "✅ HACKATHON DEPLOYMENT COMPLETE!"
echo "Requirements Met:"
echo "  ✅ Agentic Application: IntelliNemo Agent"
echo "  ✅ Llama-3.1-Nemotron-nano-8B-v1: SageMaker endpoint"
echo "  ✅ Retrieval NIM: nv-embedqa-e5-v5 on SageMaker"
echo "  ✅ SageMaker Deployment: Both NIMs running"
echo ""
echo "Test: aws lambda invoke --function-name intellinemo-agent-hackathon --payload '{}' response.json"
echo "Cost: ~$13/day (within $100 hackathon budget)"