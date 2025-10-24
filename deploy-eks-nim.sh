#!/bin/bash

# AutoCloudOps Agent - EKS + NVIDIA NIM Deployment
set -e

PROJECT_NAME="autocloudops-agent"
CLUSTER_NAME="autocloudops-eks"
REGION="us-east-1"

echo "🚀 Deploying AutoCloudOps Agent with EKS + NVIDIA NIM"
echo "💰 Estimated cost: $654.92/month"
echo ""

# Check prerequisites
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ Error: NVIDIA_API_KEY environment variable required"
    exit 1
fi

# Deploy EKS cluster
echo "☁️ Deploying EKS cluster..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation/eks-nvidia-stack.json \
    --stack-name ${PROJECT_NAME}-eks \
    --parameter-overrides \
        ClusterName=${CLUSTER_NAME} \
        NvidiaApiKey=${NVIDIA_API_KEY} \
    --capabilities CAPABILITY_IAM \
    --region ${REGION}

# Configure kubectl
echo "🔧 Configuring kubectl..."
aws eks update-kubeconfig --region ${REGION} --name ${CLUSTER_NAME}

# Create namespace
echo "📦 Creating Kubernetes namespace..."
kubectl create namespace autocloudops --dry-run=client -o yaml | kubectl apply -f -

# Create NVIDIA secrets
echo "🔐 Creating NVIDIA secrets..."
kubectl create secret generic nvidia-secrets \
    --from-literal=ngc-api-key=${NVIDIA_API_KEY} \
    --namespace=autocloudops \
    --dry-run=client -o yaml | kubectl apply -f -

# Install NVIDIA device plugin
echo "🎮 Installing NVIDIA device plugin..."
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.1/nvidia-device-plugin.yml

# Deploy NIM services
echo "🤖 Deploying NVIDIA NIM services..."
kubectl apply -f src/nim-deployments/llama3-nim-deployment.yaml
kubectl apply -f src/nim-deployments/retrieval-nim-deployment.yaml

# Wait for deployments
echo "⏳ Waiting for NIM services to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/llama3-nim-reasoning -n autocloudops
kubectl wait --for=condition=available --timeout=300s deployment/retrieval-nim-embedding -n autocloudops

# Update Lambda function
echo "🔄 Updating Lambda function for EKS integration..."
cd src/lambda
zip -r ../../lambda-eks.zip eks_lambda_function.py
cd ../..

aws lambda update-function-code \
    --function-name autocloudops-agent \
    --zip-file fileb://lambda-eks.zip \
    --region ${REGION}

aws lambda update-function-configuration \
    --function-name autocloudops-agent \
    --handler eks_lambda_function.lambda_handler \
    --region ${REGION}

# Test deployment
echo "🧪 Testing EKS + NIM deployment..."
kubectl get pods -n autocloudops
kubectl get services -n autocloudops

echo ""
echo "✅ EKS + NVIDIA NIM deployment completed!"
echo ""
echo "📊 Deployed Resources:"
echo "   • EKS Cluster: ${CLUSTER_NAME}"
echo "   • GPU Nodes: 1x g4dn.xlarge"
echo "   • Worker Nodes: 2x m5.large"
echo "   • NIM Services: Llama-3 + Retrieval"
echo "   • Lambda: EKS-integrated handler"
echo ""
echo "💰 Monthly Cost: ~$654.92"
echo "🎯 Status: Production-ready AI-powered SRE automation"

# Cleanup
rm -f lambda-eks.zip