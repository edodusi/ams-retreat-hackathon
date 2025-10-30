# Migration Guide: Bearer Token to AWS Credentials

**Date:** October 30, 2025  
**Affects:** Users with existing `.env` files using bearer token authentication

---

## 🎯 What Changed

The application previously used an **incorrect authentication method** for AWS Bedrock (bearer token). We've updated it to use **proper AWS SDK authentication** via boto3.

### Old Format (❌ No Longer Supported)
```env
AWS_BEARER_TOKEN_BEDROCK=your_bearer_token_here
```

### New Format (✅ Required)
```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=                        # Optional, for temporary credentials
```

---

## 🔄 Migration Steps

### Step 1: Update Your `.env` File

Open your `.env` file and make the following changes:

**Remove this line:**
```env
AWS_BEARER_TOKEN_BEDROCK=your_bearer_token_here
```

**Add these lines:**
```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=                        # Optional, leave empty if not using temporary credentials
AWS_REGION=us-east-1
```

### Step 2: Get AWS Credentials

If you don't have AWS access keys, you need to create them:

#### Option A: Using AWS Console

1. Log in to AWS Console: https://console.aws.amazon.com/
2. Navigate to IAM → Users
3. Select your user (or create a new one)
4. Go to "Security credentials" tab
5. Click "Create access key"
6. Select "Application running outside AWS"
7. Copy the Access Key ID and Secret Access Key
8. Paste them into your `.env` file

#### Option B: Using AWS CLI

If you already have AWS CLI configured:

```bash
# View your credentials
cat ~/.aws/credentials

# Copy the values to your .env file
# aws_access_key_id → AWS_ACCESS_KEY_ID
# aws_secret_access_key → AWS_SECRET_ACCESS_KEY
```

#### Option C: Using Existing Credentials File

If you have `~/.aws/credentials`, you can leave the `.env` fields empty and boto3 will automatically use those credentials:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
```

### Step 3: Enable Bedrock Model Access

**Important:** Even with valid credentials, you must enable model access in AWS Bedrock:

1. Go to AWS Bedrock Console: https://console.aws.amazon.com/bedrock/
2. Select region: **us-east-1** (or your configured region)
3. Click "Model access" in left sidebar
4. Click "Manage model access"
5. Find "Anthropic Claude" section
6. Check the box for "Claude Sonnet 4.5"
7. Click "Request model access" at bottom
8. Wait for approval (usually instant)

### Step 4: Verify IAM Permissions

Your IAM user/role needs the following permissions:

**Minimum Required:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-5-v1:0"
        }
    ]
}
```

**Or use AWS Managed Policy:** `AmazonBedrockFullAccess`

### Step 5: Restart the Application

```bash
# Stop the server if running (Ctrl+C)

# Activate virtual environment
source venv/bin/activate

# Start the server
python -m uvicorn backend.main:app --reload
```

### Step 6: Test the Connection

With `DEBUG=true` in your `.env`:

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

---

## 📋 Complete `.env` File Template

Here's a complete working example:

```env
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_SESSION_TOKEN=                        # Leave empty unless using temporary credentials
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-v1:0

# Storyblok Configuration
STORYBLOK_TOKEN=your_storyblok_token_here
STORYBLOK_SPACE_ID=123456
STORYBLOK_API_BASE=https://api-staging-d1.storyblok.com

# Application Configuration
APP_NAME=Storyblok Voice Assistant
DEBUG=false
CORS_ORIGINS=["http://localhost:8000", "http://127.0.0.1:8000"]

# API Configuration
MAX_CONVERSATION_HISTORY=10
DEFAULT_SEARCH_LIMIT=10
REQUEST_TIMEOUT=30
```

---

## 🐛 Troubleshooting

### Issue: "Unable to locate credentials"

**Cause:** No AWS credentials are configured.

**Solution:**
1. Ensure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set in `.env`
2. Or ensure `~/.aws/credentials` file exists
3. Restart the application

### Issue: "Access denied to Bedrock"

**Cause:** IAM permissions insufficient or model access not enabled.

**Solution:**
1. Add `AmazonBedrockFullAccess` policy to your IAM user
2. Enable model access in Bedrock console (see Step 3 above)
3. Verify: `aws sts get-caller-identity` to check credentials work

### Issue: "Model not found"

**Cause:** Model not available in your region or access not enabled.

**Solution:**
1. Ensure you're using a supported region (us-east-1 recommended)
2. Enable model access in Bedrock console
3. Verify: `aws bedrock list-foundation-models --region us-east-1`

### Issue: "InvalidSignatureException"

**Cause:** Credentials are invalid or malformed.

**Solution:**
1. Verify credentials are correctly copied (no extra spaces)
2. Regenerate access key in AWS Console
3. Update `.env` with new credentials

### Issue: "ExpiredToken"

**Cause:** Using temporary credentials (session token) that have expired.

**Solution:**
1. Use long-term IAM user credentials instead
2. Or refresh your AWS SSO session: `aws sso login`
3. Update `AWS_SESSION_TOKEN` in `.env` if using temporary credentials

---

## 🔐 Security Best Practices

### 1. Never Commit Credentials
- `.env` is in `.gitignore` - keep it there
- Never hardcode credentials in code
- Use environment variables or AWS credentials file

### 2. Use IAM Roles When Possible
- On EC2/ECS/Lambda, use IAM roles instead of access keys
- Roles automatically rotate credentials
- More secure than long-term access keys

### 3. Principle of Least Privilege
- Only grant Bedrock access, not full AWS access
- Use custom policies with minimum required permissions
- Regularly review and audit permissions

### 4. Rotate Credentials Regularly
- Create new access keys every 90 days
- Delete old unused keys
- Use temporary credentials when possible

### 5. Monitor Usage
- Enable CloudTrail to log API calls
- Set up billing alerts for unexpected usage
- Review access patterns regularly

---

## 📊 Benefits of New Authentication

### Before (Bearer Token)
- ❌ Incorrect authentication method
- ❌ Always returned 403 Forbidden
- ❌ No support for standard AWS tools
- ❌ Not production-ready

### After (AWS SDK/boto3)
- ✅ Proper AWS Signature V4 authentication
- ✅ Works with all AWS credential methods
- ✅ Supports IAM roles for production
- ✅ Compatible with AWS CLI and SDK tools
- ✅ Better error messages
- ✅ Automatic credential rotation support

---

## 🔗 Additional Resources

- **[AWS Setup Guide](docs/AWS_SETUP.md)** - Complete AWS configuration instructions
- **[AWS Credentials Fix](AWS_CREDENTIALS_FIX.md)** - Technical details of the fix
- **[Start Here](START_HERE.md)** - Quick start guide
- **[AWS Documentation](https://docs.aws.amazon.com/bedrock/)** - Official AWS Bedrock docs
- **[Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)** - AWS SDK for Python

---

## ✅ Migration Checklist

Use this checklist to ensure successful migration:

- [ ] Removed `AWS_BEARER_TOKEN_BEDROCK` from `.env`
- [ ] Added `AWS_ACCESS_KEY_ID` to `.env`
- [ ] Added `AWS_SECRET_ACCESS_KEY` to `.env`
- [ ] Verified AWS credentials work: `aws sts get-caller-identity`
- [ ] Enabled Claude model access in Bedrock console
- [ ] Verified IAM permissions include `bedrock:InvokeModel`
- [ ] Restarted the application
- [ ] Tested health endpoint: `curl http://localhost:8000/health`
- [ ] Tested Bedrock endpoint: `curl http://localhost:8000/api/test-bedrock`
- [ ] Verified no errors in server logs
- [ ] Tested conversation in frontend

---

## 🎉 Migration Complete!

Once all steps are completed and tests pass, your application is ready to use with proper AWS authentication.

**Questions?** See [docs/AWS_SETUP.md](docs/AWS_SETUP.md) or [docs/SETUP.md](docs/SETUP.md) for more help.

---

**Last Updated:** October 30, 2025  
**Version:** 1.0.0