#!/usr/bin/env python3
"""
AutoCloudOps Agent - EKS + NVIDIA NIM Cost Analysis
As specified in the original project requirements
"""

def eks_nvidia_costs():
    print("🚀 AutoCloudOps Agent - EKS + NVIDIA NIM Deployment")
    print("=" * 60)
    
    # EKS + NVIDIA NIM deployment costs
    eks_costs = {
        "EKS Control Plane": {
            "cost": 72.00,
            "details": "$0.10/hour × 24h × 30 days"
        },
        "EKS Worker Nodes (2x m5.large)": {
            "cost": 140.16,
            "details": "2 × $0.096/hour × 24h × 30 days"
        },
        "GPU Node (1x g4dn.xlarge)": {
            "cost": 380.16,
            "details": "1 × $0.526/hour × 24h × 30 days (for NVIDIA NIM)"
        },
        "EBS Storage (100GB gp3)": {
            "cost": 8.00,
            "details": "100GB × $0.08/GB/month"
        },
        "Load Balancer": {
            "cost": 16.20,
            "details": "$0.0225/hour × 24h × 30 days"
        },
        "NAT Gateway": {
            "cost": 32.40,
            "details": "$0.045/hour × 24h × 30 days"
        }
    }
    
    # NVIDIA NIM specific costs
    nvidia_costs = {
        "NVIDIA NIM License": {
            "cost": 0.00,
            "details": "Free for development/testing"
        },
        "Container Registry": {
            "cost": 1.00,
            "details": "ECR storage for NIM images"
        },
        "Data Transfer": {
            "cost": 5.00,
            "details": "API calls to NVIDIA endpoints"
        }
    }
    
    # Alternative: SageMaker deployment
    sagemaker_costs = {
        "SageMaker Endpoint (ml.g4dn.xlarge)": {
            "cost": 380.16,
            "details": "1 × $0.526/hour × 24h × 30 days"
        },
        "SageMaker Model Storage": {
            "cost": 2.30,
            "details": "100GB × $0.023/GB/month"
        },
        "Data Processing": {
            "cost": 10.00,
            "details": "Processing and inference costs"
        }
    }
    
    print("🎯 EKS + NVIDIA NIM DEPLOYMENT:")
    eks_total = 0
    for resource, info in eks_costs.items():
        print(f"   {resource:<30} ${info['cost']:>7.2f}")
        eks_total += info['cost']
    
    nvidia_total = 0
    for resource, info in nvidia_costs.items():
        print(f"   {resource:<30} ${info['cost']:>7.2f}")
        nvidia_total += info['cost']
    
    print(f"   {'EKS + NVIDIA TOTAL':<30} ${eks_total + nvidia_total:>7.2f}")
    
    print("\n🔄 ALTERNATIVE: SAGEMAKER + NVIDIA NIM:")
    sagemaker_total = 0
    for resource, info in sagemaker_costs.items():
        print(f"   {resource:<30} ${info['cost']:>7.2f}")
        sagemaker_total += info['cost']
    print(f"   {'SAGEMAKER TOTAL':<30} ${sagemaker_total:>7.2f}")
    
    print("\n💡 COST COMPARISON:")
    print(f"   Current Lambda Approach:      $    0.90/month")
    print(f"   EKS + NVIDIA NIM:             ${eks_total + nvidia_total:>7.2f}/month")
    print(f"   SageMaker + NVIDIA NIM:       ${sagemaker_total:>7.2f}/month")
    
    print("\n🎯 PROJECT REQUIREMENTS COMPLIANCE:")
    print("   ✅ Uses NVIDIA NIM (Llama-3.1-Nemotron)")
    print("   ✅ Can deploy on EKS or SageMaker")
    print("   ✅ Integrates with AWS services")
    print("   ❌ Currently using Lambda (cost optimization)")
    
    print("\n🚀 RECOMMENDED APPROACH:")
    print("   Development: Lambda + API calls ($0.90/month)")
    print("   Production: EKS + NIM containers ($655/month)")
    print("   Alternative: SageMaker endpoints ($392/month)")

def deployment_architectures():
    print("\n🏗️  DEPLOYMENT ARCHITECTURES:")
    print("=" * 60)
    
    architectures = {
        "Current (Lambda + API)": {
            "cost": "$0.90/month",
            "complexity": "Low",
            "nvidia_integration": "API calls to NVIDIA cloud",
            "pros": ["Minimal cost", "Serverless", "Quick deployment"],
            "cons": ["Network dependency", "API rate limits"]
        },
        "EKS + NIM Containers": {
            "cost": "$655/month", 
            "complexity": "High",
            "nvidia_integration": "Self-hosted NIM containers",
            "pros": ["Full control", "No API limits", "Production ready"],
            "cons": ["High cost", "Complex setup", "GPU management"]
        },
        "SageMaker + NIM": {
            "cost": "$392/month",
            "complexity": "Medium", 
            "nvidia_integration": "Managed NIM endpoints",
            "pros": ["Managed service", "Auto-scaling", "ML optimized"],
            "cons": ["Vendor lock-in", "Still expensive"]
        }
    }
    
    for arch, details in architectures.items():
        print(f"\n{arch}:")
        print(f"   Cost: {details['cost']}")
        print(f"   Complexity: {details['complexity']}")
        print(f"   NVIDIA: {details['nvidia_integration']}")
        print(f"   Pros: {', '.join(details['pros'])}")
        print(f"   Cons: {', '.join(details['cons'])}")

if __name__ == "__main__":
    eks_nvidia_costs()
    deployment_architectures()