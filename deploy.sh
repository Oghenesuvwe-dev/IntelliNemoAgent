#!/bin/bash

# AutoCloudOps Agent Deployment Script
set -e

PROJECT_NAME="autocloudops-agent"
ENVIRONMENT="dev"
REGION="us-east-1"

echo "🚀 Deploying AutoCloudOps Agent..."

# Check if NVIDIA API key is provided
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ Error: NVIDIA_API_KEY environment variable is required"
    echo "Please set it with: export NVIDIA_API_KEY=your_nvidia_api_key"
    exit 1
fi

# Check AWS CLI configuration
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ Error: AWS CLI not configured or no valid credentials"
    echo "Please run: aws configure"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Package Lambda function
echo "📦 Packaging Lambda function..."
cd src/lambda
zip -r ../../lambda-deployment.zip .
cd ../..

# Deploy CloudFormation stack
echo "☁️ Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/main-stack.json \
    --stack-name ${PROJECT_NAME}-${ENVIRONMENT} \
    --parameter-overrides \
        ProjectName=${PROJECT_NAME} \
        Environment=${ENVIRONMENT} \
        NvidiaApiKey=${NVIDIA_API_KEY} \
    --capabilities CAPABILITY_NAMED_IAM \
    --region ${REGION}

# Update Lambda function code
echo "🔄 Updating Lambda function code..."
FUNCTION_NAME="${PROJECT_NAME}-${ENVIRONMENT}-agent"
aws lambda update-function-code \
    --function-name ${FUNCTION_NAME} \
    --zip-file fileb://lambda-deployment.zip \
    --region ${REGION}

# Get stack outputs
echo "📋 Getting deployment information..."
aws cloudformation describe-stacks \
    --stack-name ${PROJECT_NAME}-${ENVIRONMENT} \
    --query 'Stacks[0].Outputs' \
    --region ${REGION}

echo "✅ Deployment completed successfully!"
echo ""
echo "🧪 To test the deployment:"
echo "1. Create a test CloudWatch alarm:"
echo "   aws cloudwatch put-metric-alarm --alarm-name test-cpu-alarm --alarm-description 'Test alarm' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 1"
echo ""
echo "2. Trigger the alarm:"
echo "   aws cloudwatch set-alarm-state --alarm-name test-cpu-alarm --state-value ALARM --state-reason 'Testing AutoCloudOps Agent'"
echo ""
echo "3. Check Lambda logs:"
echo "   aws logs tail /aws/lambda/${FUNCTION_NAME} --follow"

# Cleanup
rm -f lambda-deployment.zip