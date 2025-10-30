# AWS Bedrock Setup Guide

This guide explains how to configure AWS credentials for the Storyblok Voice Assistant to connect to AWS Bedrock.

---

## Overview

The application uses AWS Bedrock to access Claude AI for natural language conversation. AWS Bedrock requires proper AWS credentials and permissions to function.

---

## Authentication Methods

The application supports multiple AWS authentication methods:

### 1. Environment Variables (Recommended)

Set credentials directly in the `.env` file:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=your_session_token_here  # Optional, for temporary credentials
AWS_REGION=us-east-1
```

### 2. AWS Credentials File

Place credentials in `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here
```

And configure region in `~/.aws/config`:

```ini
[default]
region = us-east-1
```

### 3. IAM Role (For EC2/ECS/Lambda)

If running on AWS infrastructure, the application will automatically use the IAM role attached to the instance/container.

---

## Getting AWS Credentials

### Option 1: IAM User (For Development)

1. **Log in to AWS Console**
   - Go to https://console.aws.amazon.com/
   - Navigate to IAM service

2. **Create IAM User**
   - Click "Users" → "Create user"
   - Enter username (e.g., `storyblok-voice-assistant`)
   - Click "Next"

3. **Set Permissions**
   - Select "Attach policies directly"
   - Search for and select: `AmazonBedrockFullAccess`
   - (Or create custom policy with minimum permissions - see below)
   - Click "Next" → "Create user"

4. **Create Access Key**
   - Click on the user you just created
   - Go to "Security credentials" tab
   - Click "Create access key"
   - Select "Application running outside AWS"
   - Click "Next" → "Create access key"
   - **Copy the Access Key ID and Secret Access Key**
   - Store them securely (you won't be able to see the secret again)

5. **Add to .env file**
   ```env
   AWS_ACCESS_KEY_ID=AKIA...your_key...
   AWS_SECRET_ACCESS_KEY=wJalrX...your_secret...
   AWS_REGION=us-east-1
   ```

### Option 2: Temporary Credentials (AWS SSO)

If your organization uses AWS SSO:

1. **Run AWS SSO login**
   ```bash
   aws sso login --profile your-profile
   ```

2. **Get temporary credentials**
   ```bash
   aws configure export-credentials --profile your-profile
   ```

3. **Add to .env file** (including session token)
   ```env
   AWS_ACCESS_KEY_ID=ASIA...temp_key...
   AWS_SECRET_ACCESS_KEY=...temp_secret...
   AWS_SESSION_TOKEN=...long_session_token...
   AWS_REGION=us-east-1
   ```

---

## Required AWS Permissions

The IAM user or role needs access to AWS Bedrock. Minimum required permissions:

### Custom IAM Policy (Minimum Permissions)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-v1:0"
        }
    ]
}
```

### Using AWS Managed Policy (Easier)

Use the AWS managed policy: `AmazonBedrockFullAccess`

This provides full access to Bedrock services.

---

## Enabling Bedrock Model Access

Before you can use Claude models, you need to enable them in your AWS account:

1. **Go to AWS Bedrock Console**
   - Navigate to https://console.aws.amazon.com/bedrock/
   - Select your region (e.g., us-east-1)

2. **Request Model Access**
   - Click "Model access" in the left sidebar
   - Click "Manage model access" button
   - Find "Anthropic Claude" in the list
   - Check the box for "Claude Sonnet 4.5"
   - Click "Request model access" at the bottom

3. **Wait for Approval**
   - Most models are approved instantly
   - Check status: it should show "Access granted"

4. **Verify Access**
   ```bash
   aws bedrock list-foundation-models --region us-east-1 --query "modelSummaries[?contains(modelId, 'claude')].modelId"
   ```

---

## Supported AWS Regions

AWS Bedrock is available in the following regions:

- `us-east-1` (N. Virginia) - **Recommended**
- `us-west-2` (Oregon)
- `ap-southeast-1` (Singapore)
- `ap-northeast-1` (Tokyo)
- `eu-central-1` (Frankfurt)
- `eu-west-3` (Paris)

Update the `AWS_REGION` in your `.env` file to match your chosen region.

---

## Configuration in .env File

Update your `.env` file with the following AWS-related settings:

```env
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=                        # Optional
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-v1:0

# Storyblok Configuration (unchanged)
STORYBLOK_TOKEN=your_token_here
STORYBLOK_SPACE_ID=your_space_id
STORYBLOK_API_BASE=https://api-staging-d1.storyblok.com

# Application Configuration
DEBUG=false
CORS_ORIGINS=["http://localhost:8000", "http://127.0.0.1:8000"]
```

---

## Testing AWS Connection

### 1. Test with AWS CLI

First, verify your credentials work with the AWS CLI:

```bash
# Test credentials
aws sts get-caller-identity --region us-east-1

# List available Bedrock models
aws bedrock list-foundation-models --region us-east-1
```

### 2. Test with the Application

Start the server with `DEBUG=true` in `.env`:

```bash
python -m uvicorn backend.main:app --reload
```

Test the Bedrock connection:

```bash
curl http://localhost:8000/api/test-bedrock
```

**Expected Success Response:**
```json
{
  "status": "success",
  "response": {
    "action": "chat",
    "response": "Hello! I can help you search for content.",
    "raw_response": "..."
  }
}
```

**Expected Error Responses:**

**No credentials:**
```json
{
  "status": "error",
  "error": "Unable to locate credentials"
}
```

**No model access:**
```json
{
  "status": "error",
  "error": "Access denied to Bedrock. Please check your AWS credentials and permissions."
}
```

**Wrong region:**
```json
{
  "status": "error",
  "error": "Model anthropic.claude-sonnet-4-5-v1:0 not found. Please check the model ID."
}
```

---

## Troubleshooting

### Issue: "Unable to locate credentials"

**Cause:** No AWS credentials are configured.

**Solution:**
1. Add credentials to `.env` file
2. Or configure `~/.aws/credentials`
3. Restart the application

### Issue: "Access denied to Bedrock"

**Cause:** IAM permissions insufficient.

**Solution:**
1. Add `AmazonBedrockFullAccess` policy to IAM user/role
2. Or add custom policy with `bedrock:InvokeModel` permission
3. Verify credentials: `aws sts get-caller-identity`

### Issue: "Model not found"

**Cause:** Model access not enabled or wrong region.

**Solution:**
1. Enable model access in Bedrock console
2. Verify region matches where model is available
3. Check model ID is correct

### Issue: "ExpiredToken"

**Cause:** Temporary credentials (session token) have expired.

**Solution:**
1. Refresh credentials via AWS SSO
2. Update `.env` with new credentials
3. Restart application

### Issue: "Invalid security token"

**Cause:** Credentials are invalid or malformed.

**Solution:**
1. Verify credentials are correctly copied
2. Check for extra spaces or newlines
3. Regenerate access key if needed

---

## Security Best Practices

1. **Never Commit Credentials**
   - `.env` is in `.gitignore` - keep it that way
   - Never hardcode credentials in code
   - Use environment variables or AWS credentials file

2. **Use IAM Roles When Possible**
   - On EC2/ECS/Lambda, use IAM roles instead of access keys
   - Roles automatically rotate credentials

3. **Principle of Least Privilege**
   - Only grant Bedrock access, not full AWS access
   - Use custom policies with minimum required permissions

4. **Rotate Credentials Regularly**
   - Create new access keys periodically
   - Delete old unused keys

5. **Use AWS SSO for Organizations**
   - Temporary credentials are more secure
   - Centralized access management

6. **Monitor Usage**
   - Enable CloudTrail to log API calls
   - Set up billing alerts for unexpected usage

---

## Cost Considerations

AWS Bedrock charges for:
- **Input tokens:** Text sent to the model
- **Output tokens:** Text generated by the model

**Claude Sonnet 4.5 Pricing (as of Oct 2025):**
- Input: $0.003 per 1K tokens
- Output: $0.015 per 1K tokens

**Typical usage:**
- Simple query: ~100-200 tokens
- With context: ~500-1000 tokens
- Cost per query: $0.001-0.005

**To monitor costs:**
1. Set up AWS billing alerts
2. Use AWS Cost Explorer
3. Enable detailed billing reports

---

## Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

---

**Last Updated:** October 30, 2025  
**Version:** 1.0.0