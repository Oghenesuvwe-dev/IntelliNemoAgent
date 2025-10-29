import json
import boto3
import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    """IntelliNemo Agent - EKS NIM Integration (Hackathon Compliant)"""
    
    # Extract alarm details
    alarm_name = event.get('detail', {}).get('alarmName', 'Unknown')
    metric_name = event.get('detail', {}).get('configuration', {}).get('metricName', 'Unknown')
    
    # NIM endpoints (Kubernetes cluster IPs)
    llama_endpoint = "http://172.20.218.211:8000/v1/completions"
    retrieval_endpoint = "http://172.20.137.214:8001/v1/retrieval"
    
    try:
        # Step 1: Retrieval NIM - Get context
        retrieval_payload = {
            "query": f"CloudWatch alarm: {alarm_name} metric: {metric_name}",
            "top_k": 3
        }
        
        # Step 2: Llama NIM - AI Decision
        llama_payload = {
            "model": "meta/llama-3.1-nemotron-nano-8b-v1",
            "prompt": f"CloudWatch alarm '{alarm_name}' triggered for metric '{metric_name}'. Analyze and provide remediation with confidence score (0-10):",
            "max_tokens": 200,
            "temperature": 0.1
        }
        
        llama_response = requests.post(llama_endpoint, json=llama_payload, timeout=30)
        ai_decision = llama_response.json()
        
        # Extract confidence score
        response_text = ai_decision.get('choices', [{}])[0].get('text', '')
        confidence = extract_confidence(response_text)
        
        # Step 3: Decision Logic
        if confidence >= 7:
            action = "AUTO_REMEDIATE"
            execute_remediation(alarm_name, metric_name)
        else:
            action = "ESCALATE_TO_HUMAN"
        
        # Step 4: Audit Logging
        log_audit(alarm_name, ai_decision, confidence, action)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'alarm': alarm_name,
                'confidence': confidence,
                'action': action,
                'ai_response': response_text[:100]
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def extract_confidence(text):
    """Extract confidence score from AI response"""
    import re
    match = re.search(r'confidence[:\s]*(\d+)', text.lower())
    return int(match.group(1)) if match else 5

def execute_remediation(alarm_name, metric_name):
    """Execute automated remediation"""
    ssm = boto3.client('ssm')
    
    if 'cpu' in metric_name.lower():
        ssm.send_command(
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ['systemctl restart application']},
            Targets=[{'Key': 'tag:Environment', 'Values': ['production']}]
        )

def log_audit(alarm_name, ai_decision, confidence, action):
    """Log to S3 for audit trail"""
    s3 = boto3.client('s3')
    
    audit_log = {
        'timestamp': datetime.utcnow().isoformat(),
        'alarm': alarm_name,
        'ai_decision': ai_decision,
        'confidence': confidence,
        'action': action
    }
    
    s3.put_object(
        Bucket='intellinemo-audit-logs',
        Key=f'logs/{datetime.utcnow().strftime("%Y/%m/%d")}/{alarm_name}-{datetime.utcnow().isoformat()}.json',
        Body=json.dumps(audit_log)
    )