# AWS Credentials Fix - Migration from Bearer Token to AWS SDK

**Date:** October 30, 2025  
**Status:** ✅ Complete - All Tests Passing

---

## 🎯 Problem Fixed

The application was attempting to use a bearer token for AWS Bedrock authentication, which is incorrect. AWS Bedrock requires proper AWS Signature Version 4 (SigV4) authentication.

### Previous Error
```
403 Forbidden from AWS Bedrock
Unable to authenticate with bearer token
```

---

## ✅ Solution Implemented

Migrated from manual HTTP requests with bearer tokens to **boto3 (AWS SDK)**, which handles:
- AWS SigV4 authentication
- Credential chain resolution
- Automatic credential rotation
- Better error messages

---

## 🔧 Changes Made

### 1. Backend Code Changes

#### `backend/bedrock_client.py`
- **Before:** Used `httpx` with bearer token authentication
- **After:** Uses `boto3` with proper AWS credential chain

**Key changes:**
- Removed manual HTTP headers with bearer token
- Added boto3 client initialization
- Implemented proper AWS credential handling
- Added support for temporary credentials (session tokens)
- Improved error messages with specific AWS error codes

#### `backend/config.py`
- **Removed:** `aws_bearer_token_bedrock: str`
- **Added:** 
  - `aws_access_key_id: str = ""`
  - `aws_secret_access_key: str = ""`
  - `aws_session_token: str = ""` (optional)

#### `backend/main.py`
- Added thread pool executor for running synchronous boto3 calls
- Updated conversation endpoint to use `run_in_executor` for boto3 calls
- Maintained async behavior for overall application

### 2. Environment Configuration

#### Previous `.env` format:
```env
AWS_BEARER_TOKEN_BEDROCK=your_bearer_token_here  # ❌ Invalid
```

#### New `.env` format:
```env
AWS_ACCESS_KEY_ID=AKIA...your_key...            # ✅ Correct
AWS_SECRET_ACCESS_KEY=wJalrX...your_secret...   # ✅ Correct
AWS_SESSION_TOKEN=...optional_session_token...  # ✅ Optional
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-5-v1:0
```

### 3. Test Updates

Updated test mocks to reflect synchronous boto3 calls:
- Changed `AsyncMock` to `MagicMock` for bedrock client
- Maintained `AsyncMock` for storyblok client (still uses httpx)
- All 8 tests passing

---

## 📚 AWS Authentication Methods Supported

The application now supports all standard AWS credential methods:

### 1. Environment Variables (Recommended)
Set in `.env` file:
```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

### 2. AWS Credentials File
Place in `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_key
aws_secret_access_key = your_secret
```

### 3. IAM Role (Production)
When running on AWS infrastructure (EC2, ECS, Lambda), credentials are automatically obtained from the instance/container IAM role.

### 4. AWS SSO
For organizations using AWS SSO:
```bash
aws sso login --profile your-profile
# Credentials automatically available
```

---

## 🔐 Required AWS Permissions

The IAM user or role needs these permissions:

### Minimum Permissions
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

### Or Use AWS Managed Policy
Attach `AmazonBedrockFullAccess` to your IAM user/role.

---

## 📋 How to Configure AWS Credentials

### Step 1: Create IAM User (if needed)

1. Go to AWS Console → IAM → Users
2. Create user: `storyblok-voice-assistant`
3. Attach policy: `AmazonBedrockFullAccess`
4. Create access key
5. Copy Access Key ID and Secret Access Key

### Step 2: Enable Bedrock Model Access

1. Go to AWS Bedrock Console
2. Click "Model access" → "Manage model access"
3. Enable "Anthropic Claude Sonnet 4.5"
4. Wait for approval (usually instant)

### Step 3: Configure Application

Update `.env` file:
```env
AWS_ACCESS_KEY_ID=AKIA...your_key...
AWS_SECRET_ACCESS_KEY=wJalrX...your_secret...
AWS_REGION=us-east-1
```

### Step 4: Test

```bash
# Test with AWS CLI first
aws sts get-caller-identity --region us-east-1

# Start application
python -m uvicorn backend.main:app --reload

# Test Bedrock endpoint (with DEBUG=true)
curl http://localhost:8000/api/test-bedrock
```

---

## ✅ Verification

### Tests Passing
```bash
pytest tests/ -v
# ============================== 8 passed in 0.44s ===============================
```

### Server Starts Successfully
```bash
INFO:     Starting Storyblok Voice Assistant...
INFO:     AWS Region: us-east-1
INFO:     Bedrock Model: anthropic.claude-sonnet-4-5-v1:0
INFO:     Application startup complete.
```

### Health Check Works
```bash
curl http://localhost:8000/health
# {"status":"healthy","service":"Storyblok Voice Assistant","version":"1.0.0"}
```

---

## 🐛 Common Issues & Solutions

### Issue: "Unable to locate credentials"

**Cause:** No AWS credentials configured.

**Solution:**
1. Add credentials to `.env`
2. Or run `aws configure`
3. Restart application

### Issue: "Access denied to Bedrock"

**Cause:** IAM permissions missing.

**Solution:**
1. Add `AmazonBedrockFullAccess` policy
2. Enable model access in Bedrock console
3. Verify with: `aws bedrock list-foundation-models --region us-east-1`

### Issue: "Model not found"

**Cause:** Model not available in region or access not enabled.

**Solution:**
1. Verify region supports Claude models
2. Enable model access in Bedrock console
3. Check model ID is correct

### Issue: "ExpiredToken"

**Cause:** Using temporary credentials that expired.

**Solution:**
1. Refresh AWS SSO login
2. Update session token in `.env`
3. Or use long-term IAM user credentials

---

## 📊 Impact

### Before Fix
- ❌ 503 Service Unavailable errors
- ❌ 403 Forbidden from AWS
- ❌ Bearer token authentication (incorrect method)
- ❌ No support for standard AWS credential chain

### After Fix
- ✅ Proper AWS authentication
- ✅ Support for all AWS credential methods
- ✅ Better error messages
- ✅ Production-ready (IAM role support)
- ✅ All 8 tests passing
- ✅ Server starts without errors

---

## 🔗 Related Documentation

- [AWS_SETUP.md](docs/AWS_SETUP.md) - Complete AWS setup guide
- [SETUP.md](docs/SETUP.md) - General setup instructions
- [API.md](docs/API.md) - API documentation
- [FIXES_APPLIED.md](FIXES_APPLIED.md) - Previous fixes

---

## 🎉 Summary

The application now uses proper AWS authentication via boto3 SDK instead of invalid bearer tokens. This provides:

1. **Correct authentication** - AWS SigV4 signatures
2. **Multiple auth methods** - Environment vars, credentials file, IAM roles, SSO
3. **Better security** - No hardcoded tokens, supports temporary credentials
4. **Production ready** - Works with IAM roles on AWS infrastructure
5. **Better errors** - Specific AWS error codes with helpful messages

**All tests passing. Application ready for use with valid AWS credentials.**

---

**Last Updated:** October 30, 2025  
**Version:** 1.0.0