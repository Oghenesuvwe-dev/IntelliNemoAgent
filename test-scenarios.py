#!/usr/bin/env python3
"""
IntelliNemo Agent - Comprehensive Test Scenarios
"""

import json
import boto3
from datetime import datetime

def test_scenarios():
    """Test various alarm scenarios"""
    
    scenarios = [
        {
            "name": "High CPU Load",
            "alarm": {
                "detail": {
                    "alarmName": "prod-web-cpu-high",
                    "state": {"value": "ALARM", "reason": "CPU > 85% for 5 minutes"},
                    "configuration": {"metricName": "CPUUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected": "scale_instance"
        },
        {
            "name": "Memory Pressure", 
            "alarm": {
                "detail": {
                    "alarmName": "memory-exhaustion",
                    "state": {"value": "ALARM", "reason": "Memory > 90%"},
                    "configuration": {"metricName": "MemoryUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected": "investigate"
        },
        {
            "name": "Database Deadlocks",
            "alarm": {
                "detail": {
                    "alarmName": "db-deadlock-spike",
                    "state": {"value": "ALARM", "reason": "Deadlocks > 10/min"},
                    "configuration": {"metricName": "DatabaseConnections", "namespace": "AWS/RDS"}
                }
            },
            "expected": "restart_service"
        },
        {
            "name": "Disk Full",
            "alarm": {
                "detail": {
                    "alarmName": "disk-space-critical",
                    "state": {"value": "ALARM", "reason": "Disk usage > 95%"},
                    "configuration": {"metricName": "DiskSpaceUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected": "cleanup_logs"
        },
        {
            "name": "Network Latency",
            "alarm": {
                "detail": {
                    "alarmName": "api-response-slow",
                    "state": {"value": "ALARM", "reason": "Response time > 2s"},
                    "configuration": {"metricName": "ResponseTime", "namespace": "AWS/ApplicationELB"}
                }
            },
            "expected": "investigate"
        }
    ]
    
    lambda_client = boto3.client('lambda')
    
    print("🧪 Testing IntelliNemo Agent Scenarios")
    print("=" * 50)
    
    for scenario in scenarios:
        print(f"\n📊 Testing: {scenario['name']}")
        
        try:
            response = lambda_client.invoke(
                FunctionName='autocloudops-agent-dev-agent',
                Payload=json.dumps(scenario['alarm'])
            )
            
            result = json.loads(response['Payload'].read())
            if result.get('statusCode') == 200:
                body = json.loads(result['body'])
                actual_action = body['action']
                
                status = "✅ PASS" if actual_action == scenario['expected'] else "❌ FAIL"
                print(f"   Expected: {scenario['expected']}")
                print(f"   Actual: {actual_action}")
                print(f"   Status: {status}")
            else:
                print(f"   ❌ ERROR: {result}")
                
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_scenarios()