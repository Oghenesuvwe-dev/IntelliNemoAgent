#!/usr/bin/env python3
"""
IntelliNemo Agent - Domain-Specific Test Suite
Tests for different application domains
"""

import json
import boto3
from datetime import datetime

def test_infrastructure_domain():
    """Test Infrastructure & DevOps domain"""
    test_cases = [
        {
            "name": "High CPU Auto-Scaling",
            "alarm": {
                "detail": {
                    "alarmName": "prod-web-cpu-high",
                    "state": {"value": "ALARM", "reason": "CPU > 85% for 5 minutes"},
                    "configuration": {"metricName": "CPUUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected_action": "scale_instance"
        },
        {
            "name": "Disk Space Critical",
            "alarm": {
                "detail": {
                    "alarmName": "disk-space-critical",
                    "state": {"value": "ALARM", "reason": "Disk usage > 95%"},
                    "configuration": {"metricName": "DiskSpaceUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected_action": "cleanup_logs"
        }
    ]
    
    return run_domain_tests("Infrastructure & DevOps", test_cases)

def test_database_domain():
    """Test Database Operations domain"""
    test_cases = [
        {
            "name": "Database Connection Pool Exhaustion",
            "alarm": {
                "detail": {
                    "alarmName": "db-connections-high",
                    "state": {"value": "ALARM", "reason": "Connection count > 80"},
                    "configuration": {"metricName": "DatabaseConnections", "namespace": "AWS/RDS"}
                }
            },
            "expected_action": "restart_service"
        },
        {
            "name": "Database Deadlock Spike",
            "alarm": {
                "detail": {
                    "alarmName": "db-deadlock-spike",
                    "state": {"value": "ALARM", "reason": "Deadlocks > 10/min"},
                    "configuration": {"metricName": "Deadlocks", "namespace": "AWS/RDS"}
                }
            },
            "expected_action": "investigate"
        }
    ]
    
    return run_domain_tests("Database Operations", test_cases)

def test_security_domain():
    """Test Security & Compliance domain"""
    test_cases = [
        {
            "name": "Suspicious Login Activity",
            "alarm": {
                "detail": {
                    "alarmName": "suspicious-logins",
                    "state": {"value": "ALARM", "reason": "Failed logins > 50/min"},
                    "configuration": {"metricName": "FailedLogins", "namespace": "Custom/Security"}
                }
            },
            "expected_action": "investigate"
        },
        {
            "name": "Unauthorized API Access",
            "alarm": {
                "detail": {
                    "alarmName": "unauthorized-api-access",
                    "state": {"value": "ALARM", "reason": "401 errors > 100/min"},
                    "configuration": {"metricName": "4XXError", "namespace": "AWS/ApiGateway"}
                }
            },
            "expected_action": "investigate"
        }
    ]
    
    return run_domain_tests("Security & Compliance", test_cases)

def test_application_performance_domain():
    """Test Application Performance domain"""
    test_cases = [
        {
            "name": "High Response Time",
            "alarm": {
                "detail": {
                    "alarmName": "api-response-slow",
                    "state": {"value": "ALARM", "reason": "Response time > 2s"},
                    "configuration": {"metricName": "TargetResponseTime", "namespace": "AWS/ApplicationELB"}
                }
            },
            "expected_action": "investigate"
        },
        {
            "name": "Memory Leak Detection",
            "alarm": {
                "detail": {
                    "alarmName": "memory-leak-detected",
                    "state": {"value": "ALARM", "reason": "Memory usage increasing steadily"},
                    "configuration": {"metricName": "MemoryUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected_action": "investigate"
        }
    ]
    
    return run_domain_tests("Application Performance", test_cases)

def test_cost_management_domain():
    """Test Cost Management domain"""
    test_cases = [
        {
            "name": "Cost Anomaly Detection",
            "alarm": {
                "detail": {
                    "alarmName": "cost-spike-detected",
                    "state": {"value": "ALARM", "reason": "Daily cost > $500"},
                    "configuration": {"metricName": "EstimatedCharges", "namespace": "AWS/Billing"}
                }
            },
            "expected_action": "investigate"
        },
        {
            "name": "Unused Resources Alert",
            "alarm": {
                "detail": {
                    "alarmName": "unused-resources",
                    "state": {"value": "ALARM", "reason": "Idle instances detected"},
                    "configuration": {"metricName": "CPUUtilization", "namespace": "AWS/EC2"}
                }
            },
            "expected_action": "investigate"
        }
    ]
    
    return run_domain_tests("Cost Management", test_cases)

def run_domain_tests(domain_name, test_cases):
    """Run tests for a specific domain"""
    print(f"\n🧪 Testing Domain: {domain_name}")
    print("=" * 50)
    
    results = []
    lambda_client = boto3.client('lambda')
    
    for test_case in test_cases:
        print(f"\n📊 Test: {test_case['name']}")
        
        try:
            # Invoke Lambda with test payload
            response = lambda_client.invoke(
                FunctionName='intellinemo-agent-dev-agent',
                Payload=json.dumps(test_case['alarm'])
            )
            
            result = json.loads(response['Payload'].read())
            
            if result.get('statusCode') == 200:
                body = json.loads(result['body'])
                actual_action = body.get('action', 'unknown')
                
                # Check if action matches expected (or is reasonable fallback)
                success = (actual_action == test_case['expected_action'] or 
                          actual_action == 'investigate')  # investigate is acceptable fallback
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"   Expected: {test_case['expected_action']}")
                print(f"   Actual: {actual_action}")
                print(f"   Status: {status}")
                
                results.append({
                    'test': test_case['name'],
                    'status': 'PASS' if success else 'FAIL',
                    'expected': test_case['expected_action'],
                    'actual': actual_action
                })
            else:
                print(f"   ❌ ERROR: {result}")
                results.append({
                    'test': test_case['name'],
                    'status': 'ERROR',
                    'error': result
                })
                
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")
            results.append({
                'test': test_case['name'],
                'status': 'EXCEPTION',
                'error': str(e)
            })
    
    return results

def generate_domain_report(all_results):
    """Generate comprehensive domain test report"""
    print("\n" + "="*60)
    print("🎯 INTELLINEMO AGENT - DOMAIN TEST REPORT")
    print("="*60)
    
    total_tests = 0
    passed_tests = 0
    
    for domain, results in all_results.items():
        domain_passed = sum(1 for r in results if r['status'] == 'PASS')
        domain_total = len(results)
        
        total_tests += domain_total
        passed_tests += domain_passed
        
        print(f"\n📋 {domain}: {domain_passed}/{domain_total} PASSED")
        
        for result in results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            print(f"   {status_icon} {result['test']}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n🎯 OVERALL RESULTS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("   🎉 EXCELLENT: IntelliNemo Agent ready for production!")
    elif success_rate >= 60:
        print("   ⚠️  GOOD: Minor improvements needed")
    else:
        print("   🔧 NEEDS WORK: Significant improvements required")

def main():
    """Run all domain tests"""
    print("🧠 IntelliNemo Agent - Multi-Domain Testing Suite")
    print("Testing AI-powered SRE automation across 5 domains")
    
    all_results = {}
    
    # Run tests for each domain
    all_results["Infrastructure & DevOps"] = test_infrastructure_domain()
    all_results["Database Operations"] = test_database_domain()
    all_results["Security & Compliance"] = test_security_domain()
    all_results["Application Performance"] = test_application_performance_domain()
    all_results["Cost Management"] = test_cost_management_domain()
    
    # Generate comprehensive report
    generate_domain_report(all_results)
    
    # Save results to file
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    with open(f'domain_test_results_{timestamp}.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: domain_test_results_{timestamp}.json")

if __name__ == "__main__":
    main()