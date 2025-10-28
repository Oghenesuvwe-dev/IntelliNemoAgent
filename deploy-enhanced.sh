#!/bin/bash

# Enhanced IntelliNemo Agent Deployment
set -e

PROJECT_NAME="intellinemo-agent"
REGION="us-east-1"

echo "🚀 Deploying Enhanced IntelliNemo Agent..."

# Get Lambda function ARN
LAMBDA_ARN=$(aws lambda get-function --function-name intellinemo-agent --query 'Configuration.FunctionArn' --output text)
echo "📋 Lambda ARN: $LAMBDA_ARN"

# Deploy SSM runbooks
echo "📚 Deploying Systems Manager runbooks..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/ssm-runbooks.json \
    --stack-name ${PROJECT_NAME}-ssm-runbooks \
    --region ${REGION}

# Deploy EventBridge integration
echo "⚡ Deploying EventBridge integration..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/eventbridge-stack.json \
    --stack-name ${PROJECT_NAME}-eventbridge \
    --parameter-overrides LambdaFunctionArn=${LAMBDA_ARN} \
    --region ${REGION}

# Update Lambda with enhanced code
echo "🔄 Updating Lambda function..."
cd lambda-package && rm -f lambda_function.py && cp ../src/lambda/lambda_function.py . && zip -r ../lambda-enhanced.zip . && cd ..
aws lambda update-function-code \
    --function-name intellinemo-agent \
    --zip-file fileb://lambda-enhanced.zip \
    --region ${REGION}

# Update Lambda permissions for SSM
echo "🔐 Updating Lambda permissions..."
aws iam attach-role-policy \
    --role-name $(aws lambda get-function --function-name intellinemo-agent --query 'Configuration.Role' --output text | cut -d'/' -f2) \
    --policy-arn arn:aws:iam::aws:policy/AmazonSSMFullAccess

echo "✅ Enhanced deployment completed!"
echo ""
echo "🧪 Test with real CloudWatch alarm:"
echo "aws cloudwatch put-metric-alarm --alarm-name intellinemo-test --alarm-description 'Test' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 1 --alarm-actions arn:aws:sns:${REGION}:$(aws sts get-caller-identity --query Account --output text):intellinemo-notifications"
echo ""
echo "aws cloudwatch set-alarm-state --alarm-name intellinemo-test --state-value ALARM --state-reason 'Testing enhanced IntelliNemo'"

rm -f lambda-enhanced.zip