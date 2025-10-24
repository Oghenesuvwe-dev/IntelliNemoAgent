#!/usr/bin/env python3
"""
AutoCloudOps Agent - Monthly Cost Analysis
"""

def calculate_monthly_costs():
    print("💰 AutoCloudOps Agent - Monthly Cost Analysis")
    print("=" * 55)
    
    # Current deployed resources
    current_costs = {
        "Lambda Function": {
            "cost": 0.00,
            "details": "Free tier: 1M requests/month, minimal execution time"
        },
        "S3 Bucket": {
            "cost": 0.50,
            "details": "~20GB logs/month at $0.023/GB"
        },
        "Secrets Manager": {
            "cost": 0.40,
            "details": "1 secret at $0.40/month"
        },
        "CloudFormation": {
            "cost": 0.00,
            "details": "No charge for stack management"
        }
    }
    
    # Required test resources
    test_resources = {
        "EC2 Instance (t3.micro)": {
            "cost": 8.76,
            "details": "1 instance × $0.0104/hour × 24h × 30 days"
        },
        "Auto Scaling Group": {
            "cost": 0.00,
            "details": "No additional charge for ASG itself"
        },
        "RDS MySQL (db.t3.micro)": {
            "cost": 12.41,
            "details": "1 instance × $0.017/hour × 24h × 30 days"
        },
        "ECS Fargate (minimal)": {
            "cost": 5.00,
            "details": "0.25 vCPU, 0.5GB RAM running 24/7"
        },
        "Application Load Balancer": {
            "cost": 16.20,
            "details": "$0.0225/hour × 24h × 30 days"
        },
        "CloudWatch Alarms": {
            "cost": 1.00,
            "details": "10 alarms × $0.10/month each"
        },
        "EventBridge Rules": {
            "cost": 0.00,
            "details": "Free tier: 14M events/month"
        }
    }
    
    # Optional production resources
    production_resources = {
        "NAT Gateway": {
            "cost": 32.40,
            "details": "$0.045/hour × 24h × 30 days (for NVIDIA NIM access)"
        },
        "VPC Endpoints": {
            "cost": 7.20,
            "details": "S3 endpoint $0.01/hour × 24h × 30 days"
        },
        "Systems Manager": {
            "cost": 0.00,
            "details": "No charge for document execution"
        }
    }
    
    print("📊 CURRENT DEPLOYMENT:")
    current_total = 0
    for resource, info in current_costs.items():
        print(f"   {resource:<25} ${info['cost']:>6.2f}")
        current_total += info['cost']
    print(f"   {'TOTAL':<25} ${current_total:>6.2f}")
    
    print("\n🧪 REQUIRED TEST RESOURCES:")
    test_total = 0
    for resource, info in test_resources.items():
        print(f"   {resource:<25} ${info['cost']:>6.2f}")
        test_total += info['cost']
    print(f"   {'TOTAL':<25} ${test_total:>6.2f}")
    
    print("\n🚀 OPTIONAL PRODUCTION:")
    prod_total = 0
    for resource, info in production_resources.items():
        print(f"   {resource:<25} ${info['cost']:>6.2f}")
        prod_total += info['cost']
    print(f"   {'TOTAL':<25} ${prod_total:>6.2f}")
    
    print("\n💡 COST SUMMARY:")
    print(f"   Current (Working Demo):     ${current_total:>6.2f}/month")
    print(f"   + Test Resources:           ${test_total:>6.2f}/month")
    print(f"   + Production Features:      ${prod_total:>6.2f}/month")
    print(f"   {'FULL SYSTEM TOTAL:':<25} ${current_total + test_total + prod_total:>6.2f}/month")
    
    print("\n🎯 COST OPTIMIZATION:")
    print("   • Use Spot Instances: Save 70% on EC2")
    print("   • RDS Reserved: Save 40% with 1-year term")
    print("   • Schedule resources: Run only during testing")
    print("   • Optimized total: ~$25-30/month")

def setup_methods():
    print("\n🛠️  SETUP METHODS:")
    print("=" * 55)
    
    methods = {
        "AWS Console (Manual)": {
            "time": "2-3 hours",
            "complexity": "Medium",
            "pros": ["Visual interface", "Step-by-step"],
            "cons": ["Time consuming", "Error prone"]
        },
        "CloudFormation (IaC)": {
            "time": "30 minutes",
            "complexity": "Low",
            "pros": ["Automated", "Repeatable", "Version controlled"],
            "cons": ["Requires template creation"]
        },
        "Terraform": {
            "time": "45 minutes", 
            "complexity": "Medium",
            "pros": ["Multi-cloud", "State management"],
            "cons": ["Additional tool to learn"]
        },
        "AWS CDK": {
            "time": "1 hour",
            "complexity": "High",
            "pros": ["Code-based", "Type safety"],
            "cons": ["Requires programming knowledge"]
        }
    }
    
    for method, info in methods.items():
        print(f"\n{method}:")
        print(f"   Time: {info['time']}")
        print(f"   Complexity: {info['complexity']}")
        print(f"   Pros: {', '.join(info['pros'])}")
        print(f"   Cons: {', '.join(info['cons'])}")

if __name__ == "__main__":
    calculate_monthly_costs()
    setup_methods()