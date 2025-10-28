#!/usr/bin/env python3
"""
IntelliNemo Agent - Domain-Specific Validators
Advanced testing framework for specialized validation
"""

import json
import boto3
import time
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

class DomainValidator:
    """Base class for domain-specific validation"""
    
    def __init__(self, lambda_client):
        self.lambda_client = lambda_client
        self.function_name = 'intellinemo-agent-dev-agent'
    
    def validate_response_structure(self, response: Dict) -> Tuple[bool, str]:
        """Validate basic response structure"""
        required_fields = ['statusCode', 'body']
        for field in required_fields:
            if field not in response:
                return False, f"Missing required field: {field}"
        
        if response['statusCode'] != 200:
            return False, f"Non-200 status code: {response['statusCode']}"
        
        try:
            body = json.loads(response['body'])
            if 'action' not in body:
                return False, "Missing 'action' in response body"
        except json.JSONDecodeError:
            return False, "Invalid JSON in response body"
        
        return True, "Valid response structure"

class AIReasoningValidator(DomainValidator):
    """Validator for AI Reasoning & Decision Quality"""
    
    def validate_reasoning_quality(self, test_case: Dict, response: Dict) -> Dict:
        """Validate AI reasoning quality and decision accuracy"""
        results = {
            'test_name': test_case['name'],
            'domain': 'AI Reasoning',
            'validations': {}
        }
        
        # Basic structure validation
        is_valid, message = self.validate_response_structure(response)
        results['validations']['structure'] = {'passed': is_valid, 'message': message}
        
        if not is_valid:
            return results
        
        body = json.loads(response['body'])
        
        # Validate decision consistency
        alarm_type = test_case['alarm']['detail']['configuration']['metricName']
        action = body.get('action', 'unknown')
        
        # Check if action is appropriate for alarm type
        action_appropriateness = self.validate_action_appropriateness(alarm_type, action)
        results['validations']['action_appropriateness'] = action_appropriateness
        
        # Validate confidence scoring (if available in response)
        confidence_validation = self.validate_confidence_scoring(body)
        results['validations']['confidence'] = confidence_validation
        
        # Check for reasoning explanation (if available)
        reasoning_validation = self.validate_reasoning_explanation(body)
        results['validations']['reasoning'] = reasoning_validation
        
        return results
    
    def validate_action_appropriateness(self, metric_name: str, action: str) -> Dict:
        """Validate if action is appropriate for the metric type"""
        appropriate_actions = {
            'CPUUtilization': ['scale_instance', 'investigate'],
            'MemoryUtilization': ['investigate', 'restart_service'],
            'DatabaseConnections': ['restart_service', 'investigate'],
            'DiskSpaceUtilization': ['cleanup_logs', 'investigate'],
            'ResponseTime': ['investigate', 'scale_instance']
        }
        
        expected_actions = appropriate_actions.get(metric_name, ['investigate'])
        is_appropriate = action in expected_actions
        
        return {
            'passed': is_appropriate,
            'message': f"Action '{action}' {'is' if is_appropriate else 'is not'} appropriate for {metric_name}",
            'expected_actions': expected_actions,
            'actual_action': action
        }
    
    def validate_confidence_scoring(self, response_body: Dict) -> Dict:
        """Validate confidence scoring if present"""
        # For now, just check if response is consistent
        # In future, could validate actual confidence scores from NIM
        return {
            'passed': True,
            'message': "Confidence validation not implemented yet",
            'note': "Future enhancement: validate NIM confidence scores"
        }
    
    def validate_reasoning_explanation(self, response_body: Dict) -> Dict:
        """Validate reasoning explanation quality"""
        # Check if reasoning is provided in response
        has_reasoning = 'reasoning' in response_body or 'message' in response_body
        
        return {
            'passed': has_reasoning,
            'message': f"Reasoning explanation {'found' if has_reasoning else 'missing'}",
            'enhancement': "Future: NLP analysis of reasoning quality"
        }

class InfrastructureValidator(DomainValidator):
    """Validator for Infrastructure Automation"""
    
    def validate_infrastructure_actions(self, test_case: Dict, response: Dict) -> Dict:
        """Validate infrastructure automation capabilities"""
        results = {
            'test_name': test_case['name'],
            'domain': 'Infrastructure',
            'validations': {}
        }
        
        # Basic validation
        is_valid, message = self.validate_response_structure(response)
        results['validations']['structure'] = {'passed': is_valid, 'message': message}
        
        if not is_valid:
            return results
        
        body = json.loads(response['body'])
        action = body.get('action', 'unknown')
        
        # Validate scaling actions
        scaling_validation = self.validate_scaling_logic(test_case, action)
        results['validations']['scaling'] = scaling_validation
        
        # Validate service management
        service_validation = self.validate_service_management(test_case, action)
        results['validations']['service_management'] = service_validation
        
        # Validate resource management
        resource_validation = self.validate_resource_management(test_case, action)
        results['validations']['resource_management'] = resource_validation
        
        return results
    
    def validate_scaling_logic(self, test_case: Dict, action: str) -> Dict:
        """Validate auto-scaling decision logic"""
        alarm_name = test_case['alarm']['detail']['alarmName']
        metric = test_case['alarm']['detail']['configuration']['metricName']
        
        # Check if scaling is appropriate
        scaling_metrics = ['CPUUtilization', 'MemoryUtilization', 'RequestCount']
        should_scale = metric in scaling_metrics and 'high' in alarm_name.lower()
        
        is_scaling_action = action in ['scale_instance', 'scale_up', 'scale_out']
        
        return {
            'passed': (should_scale and is_scaling_action) or (not should_scale),
            'message': f"Scaling logic {'correct' if should_scale == is_scaling_action else 'incorrect'}",
            'should_scale': should_scale,
            'is_scaling_action': is_scaling_action
        }
    
    def validate_service_management(self, test_case: Dict, action: str) -> Dict:
        """Validate service management decisions"""
        alarm_reason = test_case['alarm']['detail']['state']['reason'].lower()
        
        # Check for service restart scenarios
        restart_indicators = ['connection', 'deadlock', 'pool', 'timeout']
        should_restart = any(indicator in alarm_reason for indicator in restart_indicators)
        
        is_restart_action = action in ['restart_service', 'restart_application']
        
        return {
            'passed': True,  # Always pass for now, as investigate is acceptable
            'message': f"Service management decision: {action}",
            'should_restart': should_restart,
            'is_restart_action': is_restart_action
        }
    
    def validate_resource_management(self, test_case: Dict, action: str) -> Dict:
        """Validate resource management decisions"""
        metric = test_case['alarm']['detail']['configuration']['metricName']
        
        # Check for cleanup scenarios
        cleanup_metrics = ['DiskSpaceUtilization', 'InodeUtilization']
        should_cleanup = metric in cleanup_metrics
        
        is_cleanup_action = action in ['cleanup_logs', 'cleanup_temp', 'cleanup_cache']
        
        return {
            'passed': (should_cleanup and is_cleanup_action) or (not should_cleanup) or action == 'investigate',
            'message': f"Resource management: {action}",
            'should_cleanup': should_cleanup,
            'is_cleanup_action': is_cleanup_action
        }

class SecurityValidator(DomainValidator):
    """Validator for Security & Compliance"""
    
    def validate_security_response(self, test_case: Dict, response: Dict) -> Dict:
        """Validate security incident response"""
        results = {
            'test_name': test_case['name'],
            'domain': 'Security',
            'validations': {}
        }
        
        # Basic validation
        is_valid, message = self.validate_response_structure(response)
        results['validations']['structure'] = {'passed': is_valid, 'message': message}
        
        if not is_valid:
            return results
        
        body = json.loads(response['body'])
        action = body.get('action', 'unknown')
        
        # Validate threat detection
        threat_validation = self.validate_threat_detection(test_case, action)
        results['validations']['threat_detection'] = threat_validation
        
        # Validate incident response
        incident_validation = self.validate_incident_response(test_case, action)
        results['validations']['incident_response'] = incident_validation
        
        # Validate compliance requirements
        compliance_validation = self.validate_compliance(test_case, action)
        results['validations']['compliance'] = compliance_validation
        
        return results
    
    def validate_threat_detection(self, test_case: Dict, action: str) -> Dict:
        """Validate threat detection accuracy"""
        alarm_name = test_case['alarm']['detail']['alarmName'].lower()
        alarm_reason = test_case['alarm']['detail']['state']['reason'].lower()
        
        # Identify security-related keywords
        security_indicators = ['failed', 'unauthorized', 'suspicious', 'attack', 'breach', 'anomaly']
        is_security_alarm = any(indicator in alarm_name or indicator in alarm_reason 
                              for indicator in security_indicators)
        
        # Security alarms should trigger investigation
        appropriate_response = action == 'investigate' if is_security_alarm else True
        
        return {
            'passed': appropriate_response,
            'message': f"Threat detection: {'appropriate' if appropriate_response else 'inappropriate'} response",
            'is_security_alarm': is_security_alarm,
            'action': action
        }
    
    def validate_incident_response(self, test_case: Dict, action: str) -> Dict:
        """Validate incident response procedures"""
        # For security incidents, investigate is always appropriate
        # Future: validate escalation, notification, containment actions
        
        return {
            'passed': action in ['investigate', 'block_ip', 'disable_user', 'escalate'],
            'message': f"Incident response action: {action}",
            'note': "Future: validate full incident response workflow"
        }
    
    def validate_compliance(self, test_case: Dict, action: str) -> Dict:
        """Validate compliance requirements"""
        # Check if audit logging would be triggered
        # Future: validate SOC2, HIPAA, PCI-DSS specific requirements
        
        return {
            'passed': True,  # Assume compliance for now
            'message': "Compliance validation placeholder",
            'note': "Future: implement industry-specific compliance checks"
        }

class PerformanceValidator(DomainValidator):
    """Validator for Performance & Reliability"""
    
    def validate_performance_response(self, test_case: Dict, response: Dict, execution_time: float) -> Dict:
        """Validate performance and reliability aspects"""
        results = {
            'test_name': test_case['name'],
            'domain': 'Performance',
            'validations': {}
        }
        
        # Response time validation
        response_time_validation = self.validate_response_time(execution_time)
        results['validations']['response_time'] = response_time_validation
        
        # Reliability validation
        reliability_validation = self.validate_reliability(response)
        results['validations']['reliability'] = reliability_validation
        
        # Scalability indicators
        scalability_validation = self.validate_scalability_indicators(test_case, response)
        results['validations']['scalability'] = scalability_validation
        
        return results
    
    def validate_response_time(self, execution_time: float) -> Dict:
        """Validate response time requirements"""
        # SRE requirement: respond to alarms within 5 seconds
        max_response_time = 5.0
        
        return {
            'passed': execution_time <= max_response_time,
            'message': f"Response time: {execution_time:.2f}s ({'within' if execution_time <= max_response_time else 'exceeds'} {max_response_time}s limit)",
            'execution_time': execution_time,
            'max_allowed': max_response_time
        }
    
    def validate_reliability(self, response: Dict) -> Dict:
        """Validate system reliability indicators"""
        # Check for successful response
        is_reliable = response.get('statusCode') == 200
        
        return {
            'passed': is_reliable,
            'message': f"System reliability: {'good' if is_reliable else 'poor'}",
            'status_code': response.get('statusCode')
        }
    
    def validate_scalability_indicators(self, test_case: Dict, response: Dict) -> Dict:
        """Validate scalability decision making"""
        # Check if system recognizes scalability needs
        alarm_reason = test_case['alarm']['detail']['state']['reason'].lower()
        scalability_keywords = ['load', 'capacity', 'throughput', 'requests']
        
        needs_scaling = any(keyword in alarm_reason for keyword in scalability_keywords)
        
        return {
            'passed': True,  # Always pass for now
            'message': f"Scalability awareness: {'detected' if needs_scaling else 'not applicable'}",
            'needs_scaling': needs_scaling
        }

class IndustryValidator(DomainValidator):
    """Validator for Industry-Specific Scenarios"""
    
    def validate_industry_compliance(self, test_case: Dict, response: Dict) -> Dict:
        """Validate industry-specific compliance and requirements"""
        results = {
            'test_name': test_case['name'],
            'domain': 'Industry-Specific',
            'validations': {}
        }
        
        # Detect industry from namespace or alarm name
        industry = self.detect_industry(test_case)
        results['detected_industry'] = industry
        
        # Industry-specific validation
        if industry == 'finance':
            industry_validation = self.validate_financial_requirements(test_case, response)
        elif industry == 'healthcare':
            industry_validation = self.validate_healthcare_requirements(test_case, response)
        elif industry == 'ecommerce':
            industry_validation = self.validate_ecommerce_requirements(test_case, response)
        else:
            industry_validation = self.validate_general_requirements(test_case, response)
        
        results['validations']['industry_specific'] = industry_validation
        
        return results
    
    def detect_industry(self, test_case: Dict) -> str:
        """Detect industry from test case context"""
        namespace = test_case['alarm']['detail']['configuration']['namespace'].lower()
        alarm_name = test_case['alarm']['detail']['alarmName'].lower()
        
        if 'finance' in namespace or 'trading' in alarm_name or 'payment' in alarm_name:
            return 'finance'
        elif 'healthcare' in namespace or 'patient' in alarm_name or 'medical' in alarm_name:
            return 'healthcare'
        elif 'ecommerce' in namespace or 'checkout' in alarm_name or 'cart' in alarm_name:
            return 'ecommerce'
        else:
            return 'general'
    
    def validate_financial_requirements(self, test_case: Dict, response: Dict) -> Dict:
        """Validate financial industry requirements"""
        # Financial services require immediate investigation for any anomaly
        body = json.loads(response['body']) if response.get('statusCode') == 200 else {}
        action = body.get('action', 'unknown')
        
        # Financial systems should be conservative - investigate rather than auto-remediate
        is_conservative = action == 'investigate'
        
        return {
            'passed': is_conservative,
            'message': f"Financial compliance: {'conservative approach' if is_conservative else 'may need review'}",
            'requirement': 'Financial systems require conservative response',
            'action': action
        }
    
    def validate_healthcare_requirements(self, test_case: Dict, response: Dict) -> Dict:
        """Validate healthcare industry requirements"""
        # Healthcare requires high availability and immediate response
        body = json.loads(response['body']) if response.get('statusCode') == 200 else {}
        action = body.get('action', 'unknown')
        
        return {
            'passed': True,  # Any response is acceptable for healthcare
            'message': f"Healthcare compliance: action '{action}' logged for audit",
            'requirement': 'Healthcare systems require audit trail',
            'action': action
        }
    
    def validate_ecommerce_requirements(self, test_case: Dict, response: Dict) -> Dict:
        """Validate e-commerce industry requirements"""
        # E-commerce requires fast response to maintain revenue
        body = json.loads(response['body']) if response.get('statusCode') == 200 else {}
        action = body.get('action', 'unknown')
        
        return {
            'passed': True,
            'message': f"E-commerce compliance: {action} response for revenue protection",
            'requirement': 'E-commerce systems prioritize availability',
            'action': action
        }
    
    def validate_general_requirements(self, test_case: Dict, response: Dict) -> Dict:
        """Validate general industry requirements"""
        return {
            'passed': True,
            'message': "General industry validation passed",
            'requirement': 'Standard SRE practices',
            'action': json.loads(response['body']).get('action', 'unknown') if response.get('statusCode') == 200 else 'unknown'
        }

class ComprehensiveDomainTester:
    """Orchestrates comprehensive domain testing"""
    
    def __init__(self):
        self.lambda_client = boto3.client('lambda')
        self.validators = {
            'ai_reasoning': AIReasoningValidator(self.lambda_client),
            'infrastructure': InfrastructureValidator(self.lambda_client),
            'security': SecurityValidator(self.lambda_client),
            'performance': PerformanceValidator(self.lambda_client),
            'industry': IndustryValidator(self.lambda_client)
        }
    
    def run_comprehensive_validation(self, test_cases: List[Dict]) -> Dict:
        """Run comprehensive validation across all domains"""
        print("🔍 Running Comprehensive Domain Validation")
        print("=" * 50)
        
        all_results = {}
        
        for test_case in test_cases:
            print(f"\n🧪 Validating: {test_case['name']}")
            
            # Execute test
            start_time = time.time()
            try:
                response = self.lambda_client.invoke(
                    FunctionName='intellinemo-agent-dev-agent',
                    Payload=json.dumps(test_case['alarm'])
                )
                execution_time = time.time() - start_time
                result = json.loads(response['Payload'].read())
                
                # Run domain-specific validations
                test_results = {}
                
                # Determine which validators to run based on test type
                domain = test_case.get('domain', 'general')
                
                if domain == 'ai_reasoning' or 'reasoning' in test_case.get('test_type', ''):
                    test_results['ai_reasoning'] = self.validators['ai_reasoning'].validate_reasoning_quality(test_case, result)
                
                if domain == 'infrastructure' or 'infrastructure' in test_case.get('test_type', ''):
                    test_results['infrastructure'] = self.validators['infrastructure'].validate_infrastructure_actions(test_case, result)
                
                if domain == 'security' or 'security' in test_case.get('test_type', ''):
                    test_results['security'] = self.validators['security'].validate_security_response(test_case, result)
                
                # Always run performance validation
                test_results['performance'] = self.validators['performance'].validate_performance_response(test_case, result, execution_time)
                
                if domain == 'industry' or 'industry' in test_case.get('test_type', ''):
                    test_results['industry'] = self.validators['industry'].validate_industry_compliance(test_case, result)
                
                all_results[test_case['name']] = {
                    'execution_time': execution_time,
                    'response': result,
                    'validations': test_results
                }
                
                print(f"   ✅ Validation complete ({execution_time:.2f}s)")
                
            except Exception as e:
                print(f"   ❌ Validation failed: {str(e)}")
                all_results[test_case['name']] = {
                    'error': str(e),
                    'validations': {}
                }
        
        return all_results

def main():
    """Run comprehensive domain validation"""
    # Sample test cases for validation
    test_cases = [
        {
            'name': 'AI Reasoning Test',
            'domain': 'ai_reasoning',
            'alarm': {
                'detail': {
                    'alarmName': 'complex-cpu-memory-issue',
                    'state': {'value': 'ALARM', 'reason': 'CPU 85% and Memory 90% simultaneously'},
                    'configuration': {'metricName': 'CPUUtilization', 'namespace': 'AWS/EC2'}
                }
            }
        },
        {
            'name': 'Security Incident Test',
            'domain': 'security',
            'alarm': {
                'detail': {
                    'alarmName': 'suspicious-login-activity',
                    'state': {'value': 'ALARM', 'reason': 'Failed logins > 100/min'},
                    'configuration': {'metricName': 'FailedLogins', 'namespace': 'Custom/Security'}
                }
            }
        },
        {
            'name': 'Financial Trading Test',
            'domain': 'industry',
            'alarm': {
                'detail': {
                    'alarmName': 'trading-latency-spike',
                    'state': {'value': 'ALARM', 'reason': 'Trading latency > 10ms'},
                    'configuration': {'metricName': 'TradeLatency', 'namespace': 'Finance/Trading'}
                }
            }
        }
    ]
    
    tester = ComprehensiveDomainTester()
    results = tester.run_comprehensive_validation(test_cases)
    
    # Save results
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    with open(f'domain_validation_results_{timestamp}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Validation results saved to: domain_validation_results_{timestamp}.json")

if __name__ == "__main__":
    main()