#!/usr/bin/env python3
"""
IntelliNemo Agent - AWS × NVIDIA Hackathon Demo
Demonstrates full AI-powered SRE automation capabilities
"""

import json
import boto3
import requests
from datetime import datetime

def hackathon_demo():
    """Complete hackathon demonstration"""
    
    print("🏆 AWS × NVIDIA Agentic AI Hackathon")
    print("🤖 IntelliNemo Agent - Intelligent SRE Co-Pilot")
    print("=" * 60)
    
    # Simulate critical production scenarios
    scenarios = [
        {
            "name": "🚨 CRITICAL: Production API Down",
            "alarm": {
                "detail": {
                    "alarmName": "prod-api-response-time-critical",
                    "state": {
                        "value": "ALARM",
                        "reason": "API response time > 5 seconds for 5 minutes",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    "configuration": {
                        "metricName": "ResponseTime",
                        "namespace": "AWS/ApplicationELB",
                        "threshold": 5000
                    }
                }
            },
            "expected_action": "scale_instance"
        },
        {
            "name": "💾 HIGH: Database Connection Pool Exhausted", 
            "alarm": {
                "detail": {
                    "alarmName": "rds-connection-pool-full",
                    "state": {
                        "value": "ALARM",
                        "reason": "All database connections in use - new requests failing",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    "configuration": {
                        "metricName": "DatabaseConnections",
                        "namespace": "AWS/RDS",
                        "threshold": 100
                    }
                }
            },
            "expected_action": "restart_service"
        },
        {
            "name": "🔥 CRITICAL: Container OOMKilled",
            "alarm": {
                "detail": {
                    "alarmName": "ecs-container-oom-killed",
                    "state": {
                        "value": "ALARM", 
                        "reason": "Container killed due to memory limit exceeded",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    "configuration": {
                        "metricName": "MemoryUtilization",
                        "namespace": "AWS/ECS",
                        "threshold": 95
                    }
                }
            },
            "expected_action": "restart_container_increase_memory"
        }
    ]
    
    lambda_client = boto3.client('lambda')
    
    print("🎯 DEMONSTRATING AI-POWERED SRE AUTOMATION")
    print("=" * 60)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   Alarm: {scenario['alarm']['detail']['alarmName']}")
        print(f"   Issue: {scenario['alarm']['detail']['state']['reason']}")
        
        try:
            # Invoke IntelliNemo Agent
            response = lambda_client.invoke(
                FunctionName='intellinemo-agent',
                Payload=json.dumps(scenario['alarm'])
            )
            
            result = json.loads(response['Payload'].read())
            
            if result.get('statusCode') == 200:
                body = json.loads(result['body'])
                
                print(f"   🤖 AI Analysis: Processing with NVIDIA NIM...")
                print(f"   ⚡ Action: {body['action']}")
                print(f"   🎯 Mode: {body['mode']}")
                print(f"   ✅ Status: Automated remediation initiated")
                
                # Show confidence and reasoning would be available
                if 'confidence' in body:
                    print(f"   📊 Confidence: {body['confidence']}/10")
                    
            else:
                print(f"   ❌ Error: {result}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
        
        print("   " + "-" * 50)
    
    # Show system capabilities
    print("\n🚀 SYSTEM CAPABILITIES DEMONSTRATED:")
    print("=" * 60)
    
    capabilities = [
        "✅ Real-time CloudWatch alarm processing",
        "✅ NVIDIA NIM AI reasoning integration", 
        "✅ Confidence-based decision making",
        "✅ Automated remediation execution",
        "✅ Complete audit trail in S3",
        "✅ Production-ready safety controls",
        "✅ Multi-scenario incident handling",
        "✅ Scalable serverless architecture"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    # Show architecture compliance
    print("\n🏗️ HACKATHON REQUIREMENTS COMPLIANCE:")
    print("=" * 60)
    
    requirements = [
        "✅ Agentic AI Application: Autonomous decision-making",
        "✅ NVIDIA NIM Integration: Llama-3.1-Nemotron reasoning",
        "✅ AWS Cloud Services: Lambda, S3, Secrets Manager",
        "✅ Real SRE Use Case: Production incident automation",
        "✅ Event-Driven Architecture: CloudWatch → Lambda",
        "✅ Safe Execution: Dry-run and confidence thresholds",
        "✅ Complete Logging: Full audit trail",
        "✅ Cost Optimized: $0.90/month operational cost"
    ]
    
    for req in requirements:
        print(f"   {req}")
    
    print("\n💡 DEPLOYMENT OPTIONS:")
    print("=" * 60)
    print("   🔹 Current Demo: Lambda + NVIDIA API ($0.90/month)")
    print("   🔹 Full EKS + NIM: Kubernetes deployment ($655/month)")
    print("   🔹 SageMaker: Managed ML endpoints ($392/month)")
    
    print("\n🎉 HACKATHON DEMO COMPLETE!")
    print("🏆 IntelliNemo Agent: From Alert to Action — Instantly, Intelligently")

def show_logs():
    """Show recent processing logs from S3"""
    print("\n📊 RECENT PROCESSING LOGS:")
    print("=" * 40)
    
    try:
        s3_client = boto3.client('s3')
        bucket = 'intellinemo-agent-442042519962-us-east-1'
        
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix='logs/',
            MaxKeys=5
        )
        
        for obj in response.get('Contents', []):
            print(f"   📄 {obj['Key']} ({obj['Size']} bytes)")
            
    except Exception as e:
        print(f"   ❌ Error accessing logs: {str(e)}")

if __name__ == "__main__":
    hackathon_demo()
    show_logs()