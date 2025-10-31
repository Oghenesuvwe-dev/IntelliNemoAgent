#!/bin/bash

# Get AWS CLI credentials from lab
echo "1. Start the lab (click Start lab button)"
echo "2. Click 'AWS CLI' and copy the credentials"
echo "3. Paste them in terminal:"
echo ""
echo "export AWS_ACCESS_KEY_ID=your_key"
echo "export AWS_SECRET_ACCESS_KEY=your_secret"
echo "export AWS_SESSION_TOKEN=your_token"
echo "export AWS_DEFAULT_REGION=us-east-1"
echo ""
echo "4. For SSH key, click 'Download PEM' button"
echo "5. Move the .pem file and set permissions:"
echo "chmod 400 ~/Downloads/your-key.pem"