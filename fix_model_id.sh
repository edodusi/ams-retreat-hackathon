#!/bin/bash
# Script to fix AWS Bedrock model ID to use inference profile

echo "=== AWS Bedrock Model ID Fix ==="
echo ""
echo "AWS Bedrock now requires using inference profiles instead of direct model IDs."
echo "This script will update your .env file to use the correct format."
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please copy .env.example to .env first:"
    echo "  cp .env.example .env"
    exit 1
fi

# Backup .env
echo "Creating backup: .env.backup"
cp .env .env.backup

# Check current model ID
CURRENT_MODEL=$(grep "BEDROCK_MODEL_ID" .env | cut -d'=' -f2)
echo "Current model ID: $CURRENT_MODEL"
echo ""

# Recommended inference profile for Claude Sonnet 4.5
NEW_MODEL="us.anthropic.claude-sonnet-4-5-v1:0"

echo "Recommended change:"
echo "  FROM: $CURRENT_MODEL"
echo "  TO:   $NEW_MODEL"
echo ""
echo "This uses a cross-region inference profile which is supported for on-demand use."
echo ""

read -p "Apply this fix? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Update the model ID in .env
    if grep -q "BEDROCK_MODEL_ID" .env; then
        # Use different sed syntax for macOS vs Linux
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s|BEDROCK_MODEL_ID=.*|BEDROCK_MODEL_ID=$NEW_MODEL|" .env
        else
            sed -i "s|BEDROCK_MODEL_ID=.*|BEDROCK_MODEL_ID=$NEW_MODEL|" .env
        fi
        echo "✅ Updated .env file"
    else
        echo "BEDROCK_MODEL_ID=$NEW_MODEL" >> .env
        echo "✅ Added BEDROCK_MODEL_ID to .env"
    fi
    
    echo ""
    echo "Verification:"
    grep "BEDROCK_MODEL_ID" .env
    echo ""
    echo "✅ Fix applied successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Restart your server if it's running"
    echo "2. Run: bash test_aws_endpoints.sh"
    echo ""
    echo "If you still get errors, check:"
    echo "- AWS credentials are correct in .env"
    echo "- Claude Sonnet 4.5 model access is enabled in AWS Bedrock Console"
    echo "- Your AWS region is set correctly (default: us-east-1)"
else
    echo "❌ Fix cancelled"
    echo "You can manually update .env with:"
    echo "  BEDROCK_MODEL_ID=$NEW_MODEL"
fi

echo ""
echo "Backup saved at: .env.backup"