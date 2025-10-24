#!/bin/bash

# AutoCloudOps Agent - SageMaker + NVIDIA NIM Deployment
set -e

PROJECT_NAME="autocloudops-agent"
REGION="us-east-1"

echo "🚀 Deploying AutoCloudOps Agent with SageMaker + NVIDIA NIM"
echo "💰 Estimated cost: $392.46/month"
echo ""

# Check prerequisites
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ Error: NVIDIA_API_KEY environment variable required"
    exit 1
fi

# Deploy SageMaker stack
echo "🤖 Deploying SageMaker + NIM stack..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/sagemaker-nim-stack.json \
    --stack-name ${PROJECT_NAME}-sagemaker \
    --parameter-overrides \
        NvidiaApiKey=${NVIDIA_API_KEY} \
        ModelName=autocloudops-llama3-nim \
    --capabilities CAPABILITY_IAM \
    --region ${REGION}

# Get endpoint names
echo "📋 Getting SageMaker endpoint information..."
LLAMA_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name ${PROJECT_NAME}-sagemaker \
    --query 'Stacks[0].Outputs[?OutputKey==`LlamaNIMEndpoint`].OutputValue' \
    --output text \
    --region ${REGION})

RETRIEVAL_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name ${PROJECT_NAME}-sagemaker \
    --query 'Stacks[0].Outputs[?OutputKey==`RetrievalNIMEndpoint`].OutputValue' \
    --output text \
    --region ${REGION})

# Create SageMaker-integrated Lambda function
echo "🔄 Creating SageMaker-integrated Lambda function..."
cat > src/lambda/sagemaker_lambda_function.py << EOF
import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    AutoCloudOps Agent - SageMaker Integration Handler
    """
    
    # SageMaker endpoints
    LLAMA_ENDPOINT = "${LLAMA_ENDPOINT}"
    RETRIEVAL_ENDPOINT = "${RETRIEVAL_ENDPOINT}"
    
    # Initialize clients
    sagemaker_runtime = boto3.client('sagemaker-runtime')
    s3_client = boto3.client('s3')
    
    # Get environment variables
    s3_bucket = os.environ['S3_BUCKET']
    mode = os.environ.get('MODE', 'DRY_RUN')
    
    try:
        # Extract alarm details
        alarm_data = extract_alarm_data(event)
        
        # Get context using Retrieval NIM
        context = get_context_from_sagemaker(alarm_data, RETRIEVAL_ENDPOINT, sagemaker_runtime)
        
        # Process with Llama-3 NIM
        reasoning_result = process_with_sagemaker(alarm_data, context, LLAMA_ENDPOINT, sagemaker_runtime)
        
        # Generate action
        action = generate_action(reasoning_result, alarm_data)
        
        # Log to S3
        log_to_s3(s3_client, s3_bucket, alarm_data, reasoning_result, action)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'AutoCloudOps Agent processed alarm successfully',
                'alarm': alarm_data['alarm_name'],
                'action': action['type'],
                'confidence': action['confidence'],
                'mode': mode,
                'deployment': 'SageMaker'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def extract_alarm_data(event):
    detail = event.get('detail', {})
    return {
        'alarm_name': detail.get('alarmName', 'Unknown'),
        'state': detail.get('state', {}).get('value', 'Unknown'),
        'reason': detail.get('state', {}).get('reason', 'No reason provided'),
        'metric_name': detail.get('configuration', {}).get('metricName', 'Unknown'),
        'namespace': detail.get('configuration', {}).get('namespace', 'Unknown'),
        'timestamp': detail.get('state', {}).get('timestamp', datetime.utcnow().isoformat())
    }

def get_context_from_sagemaker(alarm_data, endpoint_name, sagemaker_runtime):
    try:
        query = f"CloudWatch alarm: {alarm_data['alarm_name']} - {alarm_data['reason']}"
        
        payload = {
            "input": [query],
            "model": "nvidia/nv-embedqa-e5-v5"
        }
        
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        result = json.loads(response['Body'].read().decode())
        return result.get('data', [{}])[0].get('embedding', [])
        
    except Exception as e:
        print(f"Error calling Retrieval SageMaker endpoint: {str(e)}")
        return []

def process_with_sagemaker(alarm_data, context, endpoint_name, sagemaker_runtime):
    try:
        context_summary = "Retrieved context available" if context else "No context retrieved"
        
        prompt = f"""
        You are an expert SRE analyzing a CloudWatch alarm. Provide concise analysis.
        
        Alarm: {alarm_data['alarm_name']}
        State: {alarm_data['state']}
        Reason: {alarm_data['reason']}
        Metric: {alarm_data['metric_name']}
        Context: {context_summary}
        
        Provide:
        1. Root cause (1-2 sentences)
        2. Recommended action (specific)
        3. Confidence (1-10)
        """
        
        payload = {
            "model": "meta/llama-3.1-nemotron-70b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.1
        }
        
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        result = json.loads(response['Body'].read().decode())
        reasoning_text = result['choices'][0]['message']['content']
        
        # Extract confidence
        import re
        confidence_match = re.search(r'confidence[:\s]*(\d+)', reasoning_text.lower())
        confidence = int(confidence_match.group(1)) if confidence_match else 5
        
        return {
            'reasoning': reasoning_text,
            'confidence': confidence,
            'model_used': 'sagemaker-llama-3.1-nemotron',
            'context_available': len(context) > 0
        }
        
    except Exception as e:
        print(f"Error calling Llama SageMaker endpoint: {str(e)}")
        return {'reasoning': f'SageMaker error: {str(e)}', 'confidence': 0}

def generate_action(reasoning_result, alarm_data):
    action_map = {
        'CPUUtilization': {
            'type': 'scale_instance',
            'description': 'Scale EC2 Auto Scaling Group',
            'parameters': {'AutoScalingGroupName': 'default-asg', 'DesiredCapacity': '3'}
        },
        'DatabaseConnections': {
            'type': 'restart_service',
            'description': 'Restart database service',
            'parameters': {'ServiceName': 'mysql'}
        },
        'DiskSpaceUtilization': {
            'type': 'cleanup_logs',
            'description': 'Clean up old log files',
            'parameters': {'LogPath': '/var/log', 'DaysOld': '7'}
        }
    }
    
    metric_name = alarm_data.get('metric_name', 'Unknown')
    action = action_map.get(metric_name, {
        'type': 'investigate',
        'description': 'Manual investigation required',
        'parameters': {}
    })
    
    action['reasoning'] = reasoning_result.get('reasoning', 'No reasoning available')
    action['confidence'] = reasoning_result.get('confidence', 0)
    
    return action

def log_to_s3(s3_client, bucket, alarm_data, reasoning_result, action):
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'alarm': alarm_data,
        'reasoning': reasoning_result,
        'action': action,
        'deployment': 'SageMaker-NIM'
    }
    
    key = f"logs/{datetime.utcnow().strftime('%Y/%m/%d')}/{alarm_data['alarm_name']}-{int(datetime.utcnow().timestamp())}.json"
    
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(log_data, indent=2),
            ContentType='application/json'
        )
        print(f"Logged to S3: s3://{bucket}/{key}")
    except Exception as e:
        print(f"Error logging to S3: {str(e)}")
EOF

# Package and update Lambda
echo "📦 Updating Lambda function for SageMaker integration..."
cd src/lambda
zip -r ../../lambda-sagemaker.zip sagemaker_lambda_function.py
cd ../..

aws lambda update-function-code \
    --function-name autocloudops-agent \
    --zip-file fileb://lambda-sagemaker.zip \
    --region ${REGION}

aws lambda update-function-configuration \
    --function-name autocloudops-agent \
    --handler sagemaker_lambda_function.lambda_handler \
    --region ${REGION}

# Add SageMaker permissions to Lambda role
echo "🔐 Adding SageMaker permissions..."
LAMBDA_ROLE=$(aws lambda get-function --function-name autocloudops-agent --query 'Configuration.Role' --output text | cut -d'/' -f2)

aws iam attach-role-policy \
    --role-name ${LAMBDA_ROLE} \
    --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerReadOnly

echo ""
echo "✅ SageMaker + NVIDIA NIM deployment completed!"
echo ""
echo "📊 Deployed Resources:"
echo "   • SageMaker Llama-3 Endpoint: ${LLAMA_ENDPOINT}"
echo "   • SageMaker Retrieval Endpoint: ${RETRIEVAL_ENDPOINT}"
echo "   • Lambda: SageMaker-integrated handler"
echo ""
echo "💰 Monthly Cost: ~$392.46"
echo "🎯 Status: Managed ML deployment ready"

# Cleanup
rm -f lambda-sagemaker.zip