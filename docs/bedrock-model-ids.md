# Correct AWS Bedrock Model IDs

## Issue: Invalid Model ID

❌ **INCORRECT:** `anthropic.claude-sonnet-4-5-20250929-v1:0`
- This model ID does not exist
- The date format is invalid
- There is no "Claude 4.5" model

## Solution: Use Valid Model IDs

### Claude 3.5 Sonnet (Latest & Recommended)

✅ **Base Model:**
```
anthropic.claude-3-5-sonnet-20240620-v1:0
```

✅ **Cross-Region Inference Profile:**
```
us.anthropic.claude-3-5-sonnet-20240620-v1:0
```

### Other Available Models

**Claude 3 Sonnet:**
```
anthropic.claude-3-sonnet-20240229-v1:0
```

**Claude 3 Haiku (Faster, cheaper):**
```
anthropic.claude-3-haiku-20240307-v1:0
```

## How to Update

### 1. Update `.env` file:
```bash
# Change this line in your .env file:
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
```

### 2. Verify in config.py
The default is already set correctly:
```python
bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
```

## Testing Model Availability

Run the model checker script:
```bash
python check_bedrock_models.py
```

This will:
- List all available Claude models in your AWS region
- Show which models you have access to
- Test if the model can be invoked

## Common Issues

### Issue: Model Not Found
```
ResourceNotFoundException: Could not resolve model
```

**Solutions:**
1. Enable model access in AWS Bedrock Console
2. Check your AWS region (model availability varies by region)
3. Verify the model ID spelling

### Issue: Access Denied
```
AccessDeniedException: User is not authorized
```

**Solutions:**
1. Enable model access in AWS Bedrock Console:
   - Go to AWS Bedrock Console
   - Click "Model access" in left sidebar
   - Request access for Claude models
2. Wait 1-2 minutes for access to be granted
3. Verify IAM permissions include `bedrock:InvokeModel`

## Model Naming Convention

AWS Bedrock uses this format:
```
<provider>.<model-family>-<model-size>-<release-date>-<version>
```

Example breakdown:
```
anthropic.claude-3-5-sonnet-20240620-v1:0
│         │       │ │ │      │        │  │
│         │       │ │ │      │        │  └─ Revision (0)
│         │       │ │ │      │        └──── Version (v1)
│         │       │ │ │      └───────────── Release date (June 20, 2024)
│         │       │ │ └──────────────────── Model size (Sonnet)
│         │       │ └─────────────────────── Version number (3.5)
│         │       └───────────────────────── Model family (Claude)
│         └───────────────────────────────── Provider (Anthropic)
└─────────────────────────────────────────── Namespace
```

## Why No "Claude 4.5"?

As of now, the latest Claude model is **Claude 3.5 Sonnet** released in June 2024. There is no Claude 4 or Claude 4.5 yet. The SPECS.md reference to "claude-sonnet-4-5-v1:0" was an error or future speculation.

## Recommended Configuration

For best results with this project:
```bash
# .env
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
```

**Why Claude 3.5 Sonnet?**
- Best reasoning and context understanding
- Supports up to 200K tokens context
- Excellent at following JSON instructions
- Good balance of speed and quality

## Cross-Region Inference

If you need better availability, use cross-region inference profiles:
```bash
BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20240620-v1:0
```

Benefits:
- Better availability across US regions
- Automatic routing to available capacity
- Same model, same pricing

## References

- [AWS Bedrock Model IDs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html)
- [Claude on AWS Bedrock](https://docs.anthropic.com/en/api/claude-on-amazon-bedrock)
- [Bedrock Model Access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)

---

**Last Updated:** 2025-01-XX
