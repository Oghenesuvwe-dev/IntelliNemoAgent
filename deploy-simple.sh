#!/bin/bash

# Simple IntelliNemo Agent Deployment
set -e

echo "🧠 Deploying Simple IntelliNemo Agent"

# Check NVIDIA API key
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ Error: NVIDIA_API_KEY required"
    exit 1
fi

# Create S3 bucket
BUCKET_NAME="intellinemo-data-$(date +%s)"
echo "📦 Creating S3 bucket: $BUCKET_NAME"
aws s3 mb s3://$BUCKET_NAME --profile intellinemo

# Create Secrets Manager secret
echo "🔐 Creating secrets..."
SECRET_ARN=$(aws secretsmanager create-secret \
    --name "intellinemo-secrets" \
    --secret-string "{\"nvidia_api_key\":\"$NVIDIA_API_KEY\"}" \
    --profile intellinemo \
    --query 'ARN' --output text)

# Package Lambda function
echo "📦 Packaging Lambda function..."
cd src/lambda
zip -r ../../intellinemo-lambda.zip .
cd ../..

# Create Lambda function directly
echo "⚡ Creating Lambda function..."
aws lambda create-function \
    --function-name intellinemo-agent \
    --runtime python3.11 \
    --role arn:aws:iam::442042519962:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://intellinemo-lambda.zip \
    --timeout 300 \
    --memory-size 512 \
    --environment Variables="{S3_BUCKET=$BUCKET_NAME,SECRETS_ARN=$SECRET_ARN,MODE=DRY_RUN}" \
    --profile intellinemo || echo "Function may already exist"

echo "✅ Simple IntelliNemo Agent deployed!"
echo "📦 S3 Bucket: $BUCKET_NAME"
echo "🔐 Secrets ARN: $SECRET_ARN"
echo "⚡ Lambda: intellinemo-agent"

# Cleanup
rm -f intellinemo-lambda.zip