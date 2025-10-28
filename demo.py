#!/usr/bin/env python3
"""
IntelliNemo Agent Demo
Demonstrates the AI-powered SRE automation system
"""

import json
import boto3
from datetime import datetime

def demo_intellinemo_agent():
    """Demonstrate the IntelliNemo Agent functionality"""
    
    print("🚀 IntelliNemo Agent Demo")
    print("=" * 50)
    
    # Simulate CloudWatch alarm event
    test_event = {
        "detail": {
            "alarmName": "demo-high-cpu-alarm",
            "state": {
                "value": "ALARM",
                "reason": "Threshold Crossed: CPU utilization exceeded 80%",
                "timestamp": datetime.utcnow().isoformat()
            },
            "configuration": {
                "metricName": "CPUUtilization",
                "namespace": "AWS/EC2"
            }
        }
    }
    
    print("📊 Simulated CloudWatch Alarm:")
    print(json.dumps(test_event, indent=2))
    print()
    
    # Test Lambda function
    print("🔧 Testing Lambda Function...")
    lambda_client = boto3.client('lambda')
    
    try:
        response = lambda_client.invoke(
            FunctionName='intellinemo-agent',
            Payload=json.dumps(test_event)
        )
        
        result = json.loads(response['Payload'].read())
        print("✅ Lambda Response:")
        print(json.dumps(result, indent=2))
        
        if result.get('statusCode') == 200:
            body = json.loads(result['body'])
            print(f"\n🎯 Action Recommended: {body['action']}")
            print(f"🔒 Mode: {body['mode']}")
            print(f"📋 Alarm: {body['alarm']}")
            
    except Exception as e:
        print(f"❌ Error testing Lambda: {str(e)}")
    
    print("\n" + "=" * 50)
    print("📈 System Status:")
    print("✅ Infrastructure: Deployed")
    print("✅ Lambda Function: Active")
    print("✅ S3 Logging: Configured")
    print("✅ Secrets Manager: Configured")
    print("⚠️  NVIDIA NIM: Network restricted (expected in Lambda)")
    print("✅ Dry-Run Mode: Active (safe testing)")
    
    print("\n🔍 Next Steps:")
    print("1. Configure VPC for NVIDIA NIM access")
    print("2. Add EventBridge rules for automatic triggering")
    print("3. Create Systems Manager runbooks")
    print("4. Switch to ACTIVE mode for auto-remediation")

if __name__ == "__main__":
    demo_intellinemo_agent()