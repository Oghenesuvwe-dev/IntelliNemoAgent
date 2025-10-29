#!/bin/bash

# IntelliNemo Agent - EKS Hackathon Deployment
# Hackathon Compliant: Llama-3.1-Nemotron-nano-8B-v1 + Retrieval NIM on EKS

set -e

echo "🚀 Deploying IntelliNemo Agent - EKS Edition (Hackathon Compliant)"

# Deploy EKS Infrastructure
echo "📦 Deploying EKS infrastructure..."
aws cloudformation create-stack \
  --stack-name intellinemo-eks-hackathon \
  --template-body file://infrastructure/cloudformation/eks-nim-stack.json \
  --capabilities CAPABILITY_IAM \
  --parameters ParameterKey=NvidiaApiKey,ParameterValue=MmxtdHJyaTNpN2JnZTVuaTNuNThqbzVuOHY6ZTUyNjBhNGYtOGY1MC00ZTc2LWFjMzktNzUxODliYTM5ZTNh

echo "⏳ Waiting for EKS cluster creation..."
aws cloudformation wait stack-create-complete --stack-name intellinemo-eks-hackathon

# Get cluster info
CLUSTER_NAME=$(aws cloudformation describe-stacks --stack-name intellinemo-eks-hackathon --query 'Stacks[0].Outputs[?OutputKey==`ClusterName`].OutputValue' --output text)

# Configure kubectl
echo "🔧 Configuring kubectl..."
aws eks update-kubeconfig --name $CLUSTER_NAME --region us-east-1

# Install NVIDIA Device Plugin
echo "🎮 Installing NVIDIA GPU support..."
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.1/nvidia-device-plugin.yml

# Deploy NIMs
echo "🧠 Deploying Llama NIM..."
kubectl apply -f src/nim-deployments/llama-nim-eks.yaml

echo "🔍 Deploying Retrieval NIM..."
kubectl apply -f src/nim-deployments/retrieval-nim-eks.yaml

# Package and deploy Lambda
echo "📦 Packaging Lambda function..."
mkdir -p lambda-package-eks
cp src/lambda/eks_lambda_function.py lambda-package-eks/lambda_function.py
pip install requests -t lambda-package-eks/
cd lambda-package-eks && zip -r ../lambda-eks-package.zip . && cd ..

# Update Lambda function
aws lambda update-function-code \
  --function-name intellinemo-agent-eks \
  --zip-file fileb://lambda-eks-package.zip

echo "✅ EKS Hackathon deployment complete!"
echo "📊 Cluster: $CLUSTER_NAME"
echo "🧠 NIMs: Llama + Retrieval deployed on EKS"
echo "💰 Cost: ~$523/month (EKS + g4dn.xlarge)"

# Verify deployment
echo "🔍 Verifying deployment..."
kubectl get pods
kubectl get services