import json
import boto3
import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    AutoCloudOps Agent Lambda Handler
    Processes CloudWatch alarms and executes AI-driven remediation
    """
    
    # Initialize AWS clients
    secrets_client = boto3.client('secretsmanager')
    s3_client = boto3.client('s3')
    ssm_client = boto3.client('ssm')
    
    # Get environment variables
    secrets_arn = os.environ['SECRETS_ARN']
    s3_bucket = os.environ['S3_BUCKET']
    mode = os.environ.get('MODE', 'DRY_RUN')
    
    try:
        # Extract alarm details from EventBridge event
        alarm_data = extract_alarm_data(event)
        
        # Get NVIDIA NIM credentials
        nim_config = get_nim_credentials(secrets_client, secrets_arn)
        
        # Process alarm with NIM reasoning
        reasoning_result = process_with_nim(alarm_data, nim_config)
        
        # Generate remediation action
        action = generate_action(reasoning_result, alarm_data)
        
        # Log results to S3
        log_to_s3(s3_client, s3_bucket, alarm_data, reasoning_result, action)
        
        # Execute action based on mode
        if mode == 'ACTIVE':
            execute_action(ssm_client, action)
        else:
            print(f"DRY_RUN MODE: Would execute action: {action}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'AutoCloudOps Agent processed alarm successfully',
                'alarm': alarm_data['alarm_name'],
                'action': action['type'],
                'mode': mode
            })
        }
        
    except Exception as e:
        print(f"Error processing alarm: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def extract_alarm_data(event):
    """Extract relevant alarm information from EventBridge event"""
    detail = event.get('detail', {})
    return {
        'alarm_name': detail.get('alarmName', 'Unknown'),
        'state': detail.get('state', {}).get('value', 'Unknown'),
        'reason': detail.get('state', {}).get('reason', 'No reason provided'),
        'metric_name': detail.get('configuration', {}).get('metricName', 'Unknown'),
        'namespace': detail.get('configuration', {}).get('namespace', 'Unknown'),
        'timestamp': detail.get('state', {}).get('timestamp', datetime.utcnow().isoformat())
    }

def get_nim_credentials(secrets_client, secrets_arn):
    """Retrieve NVIDIA NIM credentials from Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=secrets_arn)
        secrets = json.loads(response['SecretString'])
        return {
            'api_key': secrets['nvidia_api_key'],
            'llama_endpoint': 'https://integrate-api.nvidia.com/v1/chat/completions',
            'embedding_endpoint': 'https://integrate-api.nvidia.com/v1/embeddings'
        }
    except Exception as e:
        print(f"Error retrieving NIM credentials: {str(e)}")
        return None

def process_with_nim(alarm_data, nim_config):
    """Process alarm data using NVIDIA NIM reasoning"""
    if not nim_config:
        return {'reasoning': 'Unable to access NIM services', 'confidence': 0}
    
    # Prepare context for reasoning
    context_prompt = f"""
    You are an expert SRE analyzing a CloudWatch alarm. Provide concise root cause analysis and recommended action.
    
    Alarm Details:
    - Name: {alarm_data['alarm_name']}
    - State: {alarm_data['state']}
    - Reason: {alarm_data['reason']}
    - Metric: {alarm_data['metric_name']}
    - Namespace: {alarm_data['namespace']}
    
    Provide:
    1. Root cause analysis (2-3 sentences)
    2. Recommended action (specific and actionable)
    3. Confidence level (1-10)
    """
    
    try:
        headers = {
            'Authorization': f'Bearer {nim_config["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'meta/llama-3.1-nemotron-70b-instruct',
            'messages': [{'role': 'user', 'content': context_prompt}],
            'max_tokens': 500,
            'temperature': 0.1
        }
        
        response = requests.post(nim_config['llama_endpoint'], 
                               headers=headers, 
                               json=payload, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            reasoning_text = result['choices'][0]['message']['content']
            return {
                'reasoning': reasoning_text,
                'confidence': 8,  # Default confidence
                'model_used': 'llama-3.1-nemotron-70b'
            }
        else:
            print(f"NIM API error: {response.status_code} - {response.text}")
            return {'reasoning': 'NIM API unavailable', 'confidence': 0}
            
    except Exception as e:
        print(f"Error calling NIM API: {str(e)}")
        return {'reasoning': f'NIM processing failed: {str(e)}', 'confidence': 0}

def generate_action(reasoning_result, alarm_data):
    """Generate remediation action based on reasoning and alarm type"""
    
    # Simple action mapping based on alarm characteristics
    action_map = {
        'CPUUtilization': {
            'type': 'scale_instance',
            'command': 'aws autoscaling set-desired-capacity',
            'description': 'Scale up EC2 instances'
        },
        'DatabaseConnections': {
            'type': 'restart_service',
            'command': 'systemctl restart database',
            'description': 'Restart database service'
        },
        'DiskSpaceUtilization': {
            'type': 'cleanup_logs',
            'command': 'find /var/log -name "*.log" -mtime +7 -delete',
            'description': 'Clean up old log files'
        }
    }
    
    metric_name = alarm_data.get('metric_name', 'Unknown')
    default_action = {
        'type': 'investigate',
        'command': 'echo "Manual investigation required"',
        'description': 'Manual investigation required'
    }
    
    action = action_map.get(metric_name, default_action)
    action['reasoning'] = reasoning_result.get('reasoning', 'No reasoning available')
    action['confidence'] = reasoning_result.get('confidence', 0)
    
    return action

def log_to_s3(s3_client, bucket, alarm_data, reasoning_result, action):
    """Log processing results to S3 for audit and analysis"""
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'alarm': alarm_data,
        'reasoning': reasoning_result,
        'action': action
    }
    
    key = f"logs/{datetime.utcnow().strftime('%Y/%m/%d')}/{alarm_data['alarm_name']}-{int(datetime.utcnow().timestamp())}.json"
    
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(log_data, indent=2),
            ContentType='application/json'
        )
        print(f"Logged results to S3: s3://{bucket}/{key}")
    except Exception as e:
        print(f"Error logging to S3: {str(e)}")

def execute_action(ssm_client, action):
    """Execute remediation action using Systems Manager"""
    if action['confidence'] < 7:
        print(f"Action confidence too low ({action['confidence']}), skipping execution")
        return
    
    try:
        # Execute command via Systems Manager
        response = ssm_client.send_command(
            DocumentName='AWS-RunShellScript',
            Parameters={'commands': [action['command']]},
            Comment=f"AutoCloudOps remediation: {action['description']}"
        )
        
        command_id = response['Command']['CommandId']
        print(f"Executed remediation command: {command_id}")
        
    except Exception as e:
        print(f"Error executing action: {str(e)}")