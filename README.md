# AutoCloudOps Agent

Intelligent SRE Co-Pilot powered by NVIDIA NIM and AWS services.

## Quick Start

### 1. Get NVIDIA NIM Access
1. Visit [developer.nvidia.com](https://developer.nvidia.com)
2. Sign up and navigate to NGC (NVIDIA GPU Cloud)
3. Generate API key at [ngc.nvidia.com](https://ngc.nvidia.com) → Setup → Generate API Key
4. Export your key: `export NVIDIA_API_KEY=your_nvidia_api_key`

### 2. Setup AWS
```bash
aws configure
# Enter your AWS credentials and region
```

### 3. Deploy
```bash
chmod +x deploy.sh
./deploy.sh
```

### 4. Test
```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
python tests/test_agent.py

# Check Lambda logs
aws logs tail /aws/lambda/autocloudops-agent-dev-agent --follow
```

## Architecture

```
CloudWatch Alarm → EventBridge → Lambda → NVIDIA NIM → Systems Manager
```

## Features

- **AI-Powered Analysis**: Uses Llama-3.1 Nemotron for intelligent alarm analysis
- **Safe Remediation**: Dry-run mode with confidence-based execution
- **Full Audit Trail**: All actions logged to S3
- **Event-Driven**: Automatic trigger on CloudWatch alarms

## Configuration

Environment variables in Lambda:
- `MODE`: `DRY_RUN` (safe) or `ACTIVE` (auto-remediation)
- `S3_BUCKET`: Data storage bucket
- `SECRETS_ARN`: NVIDIA API key storage

## Testing

Create test alarm:
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name test-cpu-alarm \
  --alarm-description "Test alarm" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1
```

Trigger alarm:
```bash
aws cloudwatch set-alarm-state \
  --alarm-name test-cpu-alarm \
  --state-value ALARM \
  --state-reason "Testing AutoCloudOps Agent"
```