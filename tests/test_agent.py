import json
import pytest
import boto3
from moto import mock_aws
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'lambda'))
from lambda_function import lambda_handler, extract_alarm_data, generate_action

class TestAutoCloudOpsAgent:
    
    def test_extract_alarm_data(self):
        """Test alarm data extraction from EventBridge event"""
        event = {
            'detail': {
                'alarmName': 'test-cpu-alarm',
                'state': {'value': 'ALARM', 'reason': 'CPU usage exceeded threshold'},
                'configuration': {
                    'metricName': 'CPUUtilization',
                    'namespace': 'AWS/EC2'
                }
            }
        }
        
        result = extract_alarm_data(event)
        
        assert result['alarm_name'] == 'test-cpu-alarm'
        assert result['state'] == 'ALARM'
        assert result['metric_name'] == 'CPUUtilization'
        assert result['namespace'] == 'AWS/EC2'
    
    def test_generate_action_cpu_alarm(self):
        """Test action generation for CPU utilization alarm"""
        reasoning_result = {
            'reasoning': 'High CPU usage detected, scaling recommended',
            'confidence': 8
        }
        
        alarm_data = {
            'alarm_name': 'test-cpu-alarm',
            'metric_name': 'CPUUtilization'
        }
        
        action = generate_action(reasoning_result, alarm_data)
        
        assert action['type'] == 'scale_instance'
        assert action['confidence'] == 8
        assert 'scale' in action['description'].lower()
    
    @mock_aws
    def test_lambda_handler_dry_run(self):
        """Test Lambda handler in dry run mode"""
        # Setup mock AWS resources
        s3 = boto3.client('s3', region_name='us-east-1')
        secrets = boto3.client('secretsmanager', region_name='us-east-1')
        
        # Create mock S3 bucket
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        
        # Create mock secret
        secret_arn = 'arn:aws:secretsmanager:us-east-1:123456789012:secret:test-secret'
        secrets.create_secret(
            Name='test-secret',
            SecretString=json.dumps({'nvidia_api_key': 'test-key'})
        )
        
        # Mock environment variables
        with patch.dict(os.environ, {
            'S3_BUCKET': bucket_name,
            'SECRETS_ARN': secret_arn,
            'MODE': 'DRY_RUN'
        }):
            # Mock NIM API call
            with patch('requests.post') as mock_post:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'choices': [{
                        'message': {
                            'content': 'High CPU usage requires scaling up instances'
                        }
                    }]
                }
                mock_post.return_value = mock_response
                
                # Test event
                event = {
                    'detail': {
                        'alarmName': 'test-cpu-alarm',
                        'state': {'value': 'ALARM', 'reason': 'CPU high'},
                        'configuration': {
                            'metricName': 'CPUUtilization',
                            'namespace': 'AWS/EC2'
                        }
                    }
                }
                
                result = lambda_handler(event, {})
                
                assert result['statusCode'] == 200
                body = json.loads(result['body'])
                assert body['alarm'] == 'test-cpu-alarm'
                assert body['mode'] == 'DRY_RUN'

def create_test_alarm():
    """Helper function to create a test CloudWatch alarm"""
    cloudwatch = boto3.client('cloudwatch')
    
    cloudwatch.put_metric_alarm(
        AlarmName='autocloudops-test-alarm',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=300,
        Statistic='Average',
        Threshold=80.0,
        ActionsEnabled=True,
        AlarmDescription='Test alarm for AutoCloudOps Agent',
        Unit='Percent'
    )
    
    print("✅ Test alarm created: autocloudops-test-alarm")

def trigger_test_alarm():
    """Helper function to trigger the test alarm"""
    cloudwatch = boto3.client('cloudwatch')
    
    cloudwatch.set_alarm_state(
        AlarmName='autocloudops-test-alarm',
        StateValue='ALARM',
        StateReason='Testing AutoCloudOps Agent functionality'
    )
    
    print("🚨 Test alarm triggered")

if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"])
    
    # Create and trigger test alarm for integration testing
    print("\n🧪 Setting up integration test...")
    create_test_alarm()
    trigger_test_alarm()
    print("✅ Integration test setup complete")