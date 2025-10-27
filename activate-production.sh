#!/bin/bash

# Activate IntelliNemo Agent for Production
set -e

echo "🚀 Activating IntelliNemo Agent for Production..."

# Switch to ACTIVE mode
echo "⚡ Switching to ACTIVE mode..."
aws lambda update-function-configuration \
    --function-name intellinemo-agent \
    --environment Variables='{"MODE":"ACTIVE","S3_BUCKET":"intellinemo-agent-442042519962-us-east-1","SECRETS_ARN":"arn:aws:secretsmanager:us-east-1:442042519962:secret:intellinemo-agent-secrets-3qfYNM"}'

# Create test alarm that will trigger automatically
echo "🚨 Creating production test alarm..."
aws cloudwatch put-metric-alarm \
    --alarm-name "intellinemo-production-test" \
    --alarm-description "Production test for IntelliNemo Agent" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 75 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1

echo "✅ Production activation complete!"
echo ""
echo "🎯 IntelliNemo Agent is now in ACTIVE mode"
echo "📊 Monitoring CloudWatch alarms for automatic remediation"
echo "📋 All actions will be logged to S3 for audit"
echo ""
echo "🧪 Trigger test:"
echo "aws cloudwatch set-alarm-state --alarm-name intellinemo-production-test --state-value ALARM --state-reason 'Production test'"
echo ""
echo "📈 Monitor logs:"
echo "aws logs tail /aws/lambda/intellinemo-agent --follow"