#!/usr/bin/env python3
"""
Critical Service Shutdown Scenarios for IntelliNemo Agent
"""

critical_scenarios = [
    {
        "name": "Out of Memory Kill (OOMKilled)",
        "alarm": {
            "detail": {
                "alarmName": "container-oom-killed",
                "state": {"value": "ALARM", "reason": "Container killed due to memory limit"},
                "configuration": {"metricName": "MemoryUtilization", "namespace": "AWS/ECS"}
            }
        },
        "severity": "CRITICAL",
        "action": "restart_container_increase_memory"
    },
    {
        "name": "Database Connection Pool Exhausted",
        "alarm": {
            "detail": {
                "alarmName": "db-connection-pool-full",
                "state": {"value": "ALARM", "reason": "All database connections in use"},
                "configuration": {"metricName": "DatabaseConnections", "namespace": "AWS/RDS"}
            }
        },
        "severity": "CRITICAL",
        "action": "restart_app_increase_pool_size"
    },
    {
        "name": "SSL Certificate Expired",
        "alarm": {
            "detail": {
                "alarmName": "ssl-cert-expired",
                "state": {"value": "ALARM", "reason": "SSL certificate validation failed"},
                "configuration": {"metricName": "TargetResponseTime", "namespace": "AWS/ApplicationELB"}
            }
        },
        "severity": "CRITICAL",
        "action": "renew_ssl_certificate"
    },
    {
        "name": "File Descriptor Limit Reached",
        "alarm": {
            "detail": {
                "alarmName": "fd-limit-exceeded",
                "state": {"value": "ALARM", "reason": "Too many open files"},
                "configuration": {"metricName": "FileDescriptorUtilization", "namespace": "Custom/Application"}
            }
        },
        "severity": "HIGH",
        "action": "restart_service_increase_limits"
    },
    {
        "name": "JVM Heap OutOfMemoryError",
        "alarm": {
            "detail": {
                "alarmName": "jvm-heap-exhausted",
                "state": {"value": "ALARM", "reason": "Java heap space exceeded"},
                "configuration": {"metricName": "JVMMemoryUsed", "namespace": "Custom/JVM"}
            }
        },
        "severity": "CRITICAL",
        "action": "restart_jvm_increase_heap"
    },
    {
        "name": "Thread Pool Exhaustion",
        "alarm": {
            "detail": {
                "alarmName": "thread-pool-full",
                "state": {"value": "ALARM", "reason": "All worker threads busy"},
                "configuration": {"metricName": "ThreadPoolUtilization", "namespace": "Custom/Application"}
            }
        },
        "severity": "HIGH",
        "action": "restart_app_increase_threads"
    },
    {
        "name": "Disk I/O Bottleneck",
        "alarm": {
            "detail": {
                "alarmName": "disk-io-saturated",
                "state": {"value": "ALARM", "reason": "Disk queue length > 100"},
                "configuration": {"metricName": "DiskQueueDepth", "namespace": "AWS/EBS"}
            }
        },
        "severity": "HIGH",
        "action": "scale_storage_performance"
    },
    {
        "name": "Network Port Exhaustion",
        "alarm": {
            "detail": {
                "alarmName": "ephemeral-ports-exhausted",
                "state": {"value": "ALARM", "reason": "No available ports for new connections"},
                "configuration": {"metricName": "NetworkConnections", "namespace": "Custom/Network"}
            }
        },
        "severity": "CRITICAL",
        "action": "restart_service_tune_network"
    },
    {
        "name": "Deadlock Detection",
        "alarm": {
            "detail": {
                "alarmName": "application-deadlock",
                "state": {"value": "ALARM", "reason": "Deadlock detected in application threads"},
                "configuration": {"metricName": "DeadlockCount", "namespace": "Custom/Application"}
            }
        },
        "severity": "CRITICAL",
        "action": "restart_application_immediately"
    },
    {
        "name": "DNS Resolution Failure",
        "alarm": {
            "detail": {
                "alarmName": "dns-resolution-failed",
                "state": {"value": "ALARM", "reason": "Cannot resolve external dependencies"},
                "configuration": {"metricName": "DNSQueryTime", "namespace": "Custom/Network"}
            }
        },
        "severity": "HIGH",
        "action": "restart_dns_cache_service"
    },
    {
        "name": "Log File System Full",
        "alarm": {
            "detail": {
                "alarmName": "log-filesystem-full",
                "state": {"value": "ALARM", "reason": "Cannot write logs - disk full"},
                "configuration": {"metricName": "DiskSpaceUtilization", "namespace": "AWS/EC2"}
            }
        },
        "severity": "CRITICAL",
        "action": "emergency_log_cleanup_restart"
    },
    {
        "name": "Circuit Breaker Tripped",
        "alarm": {
            "detail": {
                "alarmName": "circuit-breaker-open",
                "state": {"value": "ALARM", "reason": "Circuit breaker protecting downstream service"},
                "configuration": {"metricName": "CircuitBreakerState", "namespace": "Custom/Application"}
            }
        },
        "severity": "HIGH",
        "action": "restart_dependent_services"
    }
]

def print_scenarios():
    print("🚨 CRITICAL SERVICE SHUTDOWN SCENARIOS")
    print("=" * 60)
    
    for i, scenario in enumerate(critical_scenarios, 1):
        print(f"\n{i}. {scenario['name']} [{scenario['severity']}]")
        print(f"   Cause: {scenario['alarm']['detail']['state']['reason']}")
        print(f"   Action: {scenario['action']}")

if __name__ == "__main__":
    print_scenarios()