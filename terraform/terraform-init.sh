#!/bin/bash

# Terraform initialization and deployment script for EU AI Act QA System
echo "Starting Terraform Infrastructure Deployment"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "Terraform is not installed. Please install it first."
    exit 1
fi

# Check for AWS credentials
echo "Verifying AWS credentials..."
aws sts get-caller-identity > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "AWS credentials not configured correctly. Please run 'aws configure'"
    exit 1
fi

echo "Creating terraform.tfvars file..."
# Generate random passwords for databases
DB_PASSWORD=$(openssl rand -base64 12)
LOGS_DB_PASSWORD=$(openssl rand -base64 12)

cat > terraform.tfvars << EOF
aws_region = "us-east-1"
project_name = "euaiact-qa"
environment = "dev"
db_name = "euaiact"
db_password = "${DB_PASSWORD}"
logs_db_name = "logs"
logs_db_password = "${LOGS_DB_PASSWORD}"
EOF

echo "Initializing Terraform..."
terraform init

echo "Validating Terraform configuration..."
terraform validate

if [ $? -eq 0 ]; then
    echo "Configuration validated successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Review the terraform.tfvars file and update if needed"
    echo "2. Run 'terraform plan' to see what resources will be created"
    echo "3. Run 'terraform apply' to create the infrastructure"
    echo ""
    echo "After deploying infrastructure, add these secrets to your GitHub repository:"
    echo "AWS_ACCESS_KEY_ID: Your AWS access key"
    echo "AWS_SECRET_ACCESS_KEY: Your AWS secret key"
    echo "DB_USER: postgres"
    echo "DB_PASSWORD: ${DB_PASSWORD}"
    echo "DB_NAME: euaiact"
    echo "LOGS_USER: postgres"
    echo "LOGS_PASSWORD: ${LOGS_DB_PASSWORD}"
    echo "LOGS_DB: logs"
    echo "VOYAGE_API_KEY: Your Voyage API key"
    echo "GOOGLE_API_KEY: Your Google API key"
else
    echo "Configuration validation failed!"
fi