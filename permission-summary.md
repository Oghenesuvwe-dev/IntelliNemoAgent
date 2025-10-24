# 🔐 Required Permissions for AutoCloudOps Agent

## Current Issue
The EKS deployment failed because the IAM user `Synapse-Agent` lacks the necessary permissions to create AWS resources.

## Required Permission Categories

### 1. **EKS Cluster Management**
```
eks:CreateCluster
eks:DescribeCluster  
eks:CreateNodegroup
eks:DescribeNodegroup
```

### 2. **EC2 Networking (Critical)**
```
ec2:CreateVpc          ← FAILED HERE
ec2:CreateSubnet
ec2:CreateSecurityGroup
ec2:CreateInternetGateway
ec2:CreateNatGateway
ec2:AllocateAddress
```

### 3. **IAM Role Management**
```
iam:CreateRole
iam:PassRole
iam:AttachRolePolicy
```

### 4. **EventBridge & CloudWatch**
```
events:CreateRule      ← ALSO FAILED EARLIER
events:PutTargets
cloudwatch:PutMetricAlarm
```

### 5. **Systems Manager**
```
ssm:CreateDocument     ← FAILED EARLIER
ssm:SendCommand
ssm:StartAutomationExecution
```

## Solutions

### Option 1: Add Permissions (Recommended)
```bash
# Attach the comprehensive policy
aws iam attach-user-policy \
  --user-name Synapse-Agent \
  --policy-arn arn:aws:iam::442042519962:policy/AutoCloudOpsFullAccess
```

### Option 2: Use Administrator Access (Quick)
```bash
# Temporary admin access for hackathon
aws iam attach-user-policy \
  --user-name Synapse-Agent \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### Option 3: Deploy with Different Approach
- Use existing Lambda approach (already working)
- Simulate EKS deployment without actual resources
- Focus on AI logic demonstration

## Current Working Components
✅ **Lambda Function**: Deployed and active  
✅ **S3 Logging**: Working with audit trail  
✅ **Secrets Manager**: NVIDIA API key secured  
✅ **NVIDIA NIM Integration**: API calls functional  

## Missing Components (Due to Permissions)
❌ **EKS Cluster**: Cannot create VPC  
❌ **EventBridge Rules**: Cannot create rules  
❌ **SSM Documents**: Cannot create documents  
❌ **Auto Scaling Groups**: Cannot create ASG  

## Recommendation
For hackathon demonstration, the **current Lambda approach** fully demonstrates the AI-powered SRE automation concept. The EKS deployment is an infrastructure scaling option but not required for core functionality.

**Cost Impact:**
- Current working system: $0.90/month
- Full EKS system (if permissions added): $654.92/month

The AI reasoning, automated decision-making, and SRE automation are all functional in the current deployment.