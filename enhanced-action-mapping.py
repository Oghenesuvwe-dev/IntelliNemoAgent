"""
Enhanced Action Mapping for Critical Shutdown Scenarios
Add to lambda_function.py generate_action() function
"""

enhanced_action_map = {
    # Memory Issues
    'MemoryUtilization': {
        'type': 'restart_container_increase_memory',
        'description': 'Restart container with increased memory limits',
        'parameters': {
            'ServiceName': 'web-service',
            'MemoryReservation': '2048',
            'RestartPolicy': 'immediate'
        }
    },
    
    # JVM Issues  
    'JVMMemoryUsed': {
        'type': 'restart_jvm_increase_heap',
        'description': 'Restart JVM with larger heap size',
        'parameters': {
            'ServiceName': 'java-app',
            'HeapSize': '4g',
            'GCSettings': 'G1GC'
        }
    },
    
    # File Descriptor Issues
    'FileDescriptorUtilization': {
        'type': 'restart_service_increase_limits',
        'description': 'Restart service with increased file descriptor limits',
        'parameters': {
            'ServiceName': 'app-service',
            'FileDescriptorLimit': '65536'
        }
    },
    
    # Thread Pool Issues
    'ThreadPoolUtilization': {
        'type': 'restart_app_increase_threads',
        'description': 'Restart application with larger thread pool',
        'parameters': {
            'ServiceName': 'worker-service',
            'ThreadPoolSize': '200'
        }
    },
    
    # Network Issues
    'NetworkConnections': {
        'type': 'restart_service_tune_network',
        'description': 'Restart service with network tuning',
        'parameters': {
            'ServiceName': 'api-service',
            'NetworkOptimization': 'true'
        }
    },
    
    # Disk I/O Issues
    'DiskQueueDepth': {
        'type': 'scale_storage_performance',
        'description': 'Scale storage performance tier',
        'parameters': {
            'VolumeId': 'vol-xxx',
            'IOPS': '3000',
            'VolumeType': 'gp3'
        }
    },
    
    # Application Deadlocks
    'DeadlockCount': {
        'type': 'restart_application_immediately',
        'description': 'Emergency restart due to deadlock',
        'parameters': {
            'ServiceName': 'app-service',
            'RestartType': 'force',
            'HealthCheckGracePeriod': '30'
        }
    },
    
    # DNS Issues
    'DNSQueryTime': {
        'type': 'restart_dns_cache_service',
        'description': 'Restart DNS cache and resolver',
        'parameters': {
            'ServiceName': 'dns-cache',
            'FlushCache': 'true'
        }
    },
    
    # Circuit Breaker
    'CircuitBreakerState': {
        'type': 'restart_dependent_services',
        'description': 'Restart services in dependency chain',
        'parameters': {
            'ServiceGroup': 'api-tier',
            'RestartOrder': 'reverse-dependency'
        }
    }
}