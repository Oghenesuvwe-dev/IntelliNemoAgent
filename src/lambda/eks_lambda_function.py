import json
import boto3
import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    IntelliNemo Agent - EKS Integration Handler
    Processes CloudWatch alarms using NVIDIA NIM on EKS
    """
    
    # EKS NIM endpoints (internal cluster IPs)
    LLAMA_NIM_URL = "http://llama3-nim-service.intellinemo.svc.cluster.local:8000/v1/chat/completions"
    RETRIEVAL_NIM_URL = "http://retrieval-nim-service.intellinemo.svc.cluster.local:8001/v1/embeddings"
    
    # Initialize AWS clients
    s3_client = boto3.client('s3')
    ssm_client = boto3.client('ssm')
    
    # Get environment variables
    s3_bucket = os.environ['S3_BUCKET']
    mode = os.environ.get('MODE', 'DRY_RUN')
    
    try:
        # Extract alarm details
        alarm_data = extract_alarm_data(event)
        
        # Get context using Retrieval NIM
        context = get_context_from_retrieval_nim(alarm_data, RETRIEVAL_NIM_URL)
        
        # Process with Llama-3 NIM reasoning
        reasoning_result = process_with_llama_nim(alarm_data, context, LLAMA_NIM_URL)
        
        # Generate remediation action
        action = generate_action(reasoning_result, alarm_data)
        
        # Log to S3
        log_to_s3(s3_client, s3_bucket, alarm_data, reasoning_result, action)
        
        # Execute action if in ACTIVE mode
        if mode == 'ACTIVE' and action['confidence'] >= 7:
            execute_action(ssm_client, action)
        else:
            print(f"DRY_RUN MODE: Would execute action: {action}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'IntelliNemo Agent processed alarm successfully',
                'alarm': alarm_data['alarm_name'],
                'action': action['type'],
                'confidence': action['confidence'],
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
    """Extract alarm information from EventBridge event"""
    detail = event.get('detail', {})
    return {
        'alarm_name': detail.get('alarmName', 'Unknown'),
        'state': detail.get('state', {}).get('value', 'Unknown'),
        'reason': detail.get('state', {}).get('reason', 'No reason provided'),
        'metric_name': detail.get('configuration', {}).get('metricName', 'Unknown'),
        'namespace': detail.get('configuration', {}).get('namespace', 'Unknown'),
        'timestamp': detail.get('state', {}).get('timestamp', datetime.utcnow().isoformat())
    }

def get_context_from_retrieval_nim(alarm_data, retrieval_url):
    """Get contextual information using Retrieval NIM"""
    try:
        query = f"CloudWatch alarm: {alarm_data['alarm_name']} - {alarm_data['reason']}"
        
        payload = {
            "input": [query],
            "model": "nvidia/nv-embedqa-e5-v5"
        }
        
        response = requests.post(retrieval_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json().get('data', [{}])[0].get('embedding', [])
        else:
            print(f"Retrieval NIM error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error calling Retrieval NIM: {str(e)}")
        return []

def process_with_llama_nim(alarm_data, context, llama_url):
    """Process alarm using Llama-3 NIM reasoning"""
    try:
        context_summary = "Retrieved context available" if context else "No context retrieved"
        
        prompt = f"""
        You are an expert SRE analyzing a CloudWatch alarm. Provide concise analysis and action.
        
        Alarm: {alarm_data['alarm_name']}
        State: {alarm_data['state']}
        Reason: {alarm_data['reason']}
        Metric: {alarm_data['metric_name']}
        Namespace: {alarm_data['namespace']}
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
        
        response = requests.post(llama_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            reasoning_text = result['choices'][0]['message']['content']
            
            # Extract confidence from response
            confidence = extract_confidence(reasoning_text)
            
            return {
                'reasoning': reasoning_text,
                'confidence': confidence,
                'model_used': 'llama-3.1-nemotron-70b',
                'context_available': len(context) > 0
            }
        else:
            print(f"Llama NIM error: {response.status_code}")
            return {'reasoning': 'NIM processing failed', 'confidence': 0}
            
    except Exception as e:
        print(f"Error calling Llama NIM: {str(e)}")
        return {'reasoning': f'NIM error: {str(e)}', 'confidence': 0}

def extract_confidence(reasoning_text):
    """Extract confidence score from reasoning text"""
    import re
    confidence_match = re.search(r'confidence[:\s]*(\d+)', reasoning_text.lower())
    if confidence_match:
        return int(confidence_match.group(1))
    return 5  # Default confidence

def generate_action(reasoning_result, alarm_data):
    """Generate remediation action based on reasoning"""
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

def execute_action(ssm_client, action):
    """Execute remediation action using Systems Manager"""
    if action['confidence'] < 7:
        print(f"Action confidence too low ({action['confidence']}), skipping execution")
        return
    
    try:
        if action['type'] == 'scale_instance':
            response = ssm_client.start_automation_execution(
                DocumentName='IntelliNemo-ScaleEC2',
                Parameters=action['parameters']
            )
        elif action['type'] == 'restart_service':
            response = ssm_client.send_command(
                DocumentName='IntelliNemo-RestartService',
                Parameters=action['parameters']
            )
        else:
            response = ssm_client.send_command(
                DocumentName='AWS-RunShellScript',
                Parameters={'commands': [f"echo 'Action: {action['description']}'"]}
            )
        
        execution_id = response.get('AutomationExecutionId') or response.get('Command', {}).get('CommandId')
        print(f"Executed remediation: {execution_id}")
        
    except Exception as e:
        print(f"Error executing action: {str(e)}")

def log_to_s3(s3_client, bucket, alarm_data, reasoning_result, action):
    """Log processing results to S3"""
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'alarm': alarm_data,
        'reasoning': reasoning_result,
        'action': action,
        'deployment': 'EKS-NIM'
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