#!/usr/bin/env python3
"""
Script to check available AWS Bedrock models and inference profiles.
Helps identify the correct model ID to use.
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError, NoCredentialsError


def load_env():
    """Load environment variables from .env file."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment only")
    
    import os
    return {
        'region': os.getenv('AWS_REGION', 'us-east-1'),
        'access_key': os.getenv('AWS_ACCESS_KEY_ID', ''),
        'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
        'session_token': os.getenv('AWS_SESSION_TOKEN', '')
    }


def check_credentials():
    """Check if AWS credentials are configured."""
    config = load_env()
    
    print("\n=== AWS Credentials Check ===")
    print(f"Region: {config['region']}")
    print(f"Access Key ID: {'✅ Set' if config['access_key'] else '❌ Not set'}")
    print(f"Secret Access Key: {'✅ Set' if config['secret_key'] else '❌ Not set'}")
    print(f"Session Token: {'✅ Set' if config['session_token'] else '(Optional) Not set'}")
    
    if not config['access_key'] or not config['secret_key']:
        print("\n❌ AWS credentials not configured!")
        print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env")
        return None
    
    return config


def list_foundation_models(config):
    """List available foundation models."""
    print("\n=== Checking Foundation Models ===")
    
    try:
        client = boto3.client(
            'bedrock',
            region_name=config['region'],
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            aws_session_token=config['session_token'] if config['session_token'] else None
        )
        
        response = client.list_foundation_models()
        
        # Filter for Claude models
        claude_models = [
            model for model in response.get('modelSummaries', [])
            if 'claude' in model.get('modelId', '').lower()
        ]
        
        print(f"Found {len(claude_models)} Claude models:")
        print()
        
        for model in claude_models:
            model_id = model.get('modelId', 'Unknown')
            model_name = model.get('modelName', 'Unknown')
            provider = model.get('providerName', 'Unknown')
            status = model.get('modelLifecycle', {}).get('status', 'Unknown')
            
            print(f"  • {model_name}")
            print(f"    ID: {model_id}")
            print(f"    Provider: {provider}")
            print(f"    Status: {status}")
            
            # Check if inference profiles are supported
            inference_types = model.get('inferenceTypesSupported', [])
            if inference_types:
                print(f"    Inference Types: {', '.join(inference_types)}")
            
            print()
        
        return claude_models
        
    except NoCredentialsError:
        print("❌ AWS credentials not found")
        return None
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        print(f"❌ AWS Error [{error_code}]: {error_msg}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None


def list_inference_profiles(config):
    """List available inference profiles."""
    print("\n=== Checking Inference Profiles ===")
    
    try:
        client = boto3.client(
            'bedrock',
            region_name=config['region'],
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            aws_session_token=config['session_token'] if config['session_token'] else None
        )
        
        # Try to list inference profiles (may not be available in all regions)
        try:
            response = client.list_inference_profiles()
            profiles = response.get('inferenceProfileSummaries', [])
            
            if profiles:
                print(f"Found {len(profiles)} inference profiles:")
                print()
                
                for profile in profiles:
                    profile_id = profile.get('inferenceProfileId', 'Unknown')
                    profile_name = profile.get('inferenceProfileName', 'Unknown')
                    models = profile.get('models', [])
                    
                    # Filter for Claude
                    if 'claude' in profile_id.lower() or any('claude' in m.get('modelId', '').lower() for m in models):
                        print(f"  • {profile_name}")
                        print(f"    ID: {profile_id}")
                        print(f"    Type: {profile.get('type', 'Unknown')}")
                        if models:
                            print(f"    Models: {', '.join([m.get('modelId', 'Unknown') for m in models])}")
                        print()
                
                return profiles
            else:
                print("No inference profiles found")
                print("Note: Inference profiles may not be available in all regions")
                return []
                
        except AttributeError:
            print("⚠️  list_inference_profiles not available in this boto3 version")
            print("Inference profiles are a newer feature")
            return None
            
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'AccessDeniedException':
            print("⚠️  No permission to list inference profiles")
            print("This is OK - you may still be able to use them")
        else:
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            print(f"⚠️  Error [{error_code}]: {error_msg}")
        return None
    except Exception as e:
        print(f"⚠️  Could not list inference profiles: {str(e)}")
        return None


def test_model_invoke(config, model_id):
    """Test if a specific model can be invoked."""
    print(f"\n=== Testing Model: {model_id} ===")
    
    try:
        client = boto3.client(
            'bedrock-runtime',
            region_name=config['region'],
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            aws_session_token=config['session_token'] if config['session_token'] else None
        )
        
        # Try to invoke with a simple message
        response = client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Hello, reply with just 'OK'"}]
                }
            ]
        )
        
        print(f"✅ Model {model_id} is accessible and working!")
        
        # Extract response
        output = response.get('output', {})
        message = output.get('message', {})
        content = message.get('content', [])
        if content:
            text = content[0].get('text', '')
            print(f"Response: {text}")
        
        return True
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        print(f"❌ Cannot use model [{error_code}]: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main function."""
    print("=" * 60)
    print("AWS Bedrock Model Checker")
    print("=" * 60)
    
    # Check credentials
    config = check_credentials()
    if not config:
        sys.exit(1)
    
    # List foundation models
    models = list_foundation_models(config)
    
    # List inference profiles
    profiles = list_inference_profiles(config)
    
    # Suggest models to test
    print("\n=== Recommended Model IDs to Test ===")
    print()
    
    suggestions = [
        ("anthropic.claude-3-5-sonnet-20240620-v1:0", "Claude 3.5 Sonnet (Base Model)"),
        ("us.anthropic.claude-3-5-sonnet-20240620-v1:0", "Claude 3.5 Sonnet (US Cross-Region)"),
        ("anthropic.claude-3-sonnet-20240229-v1:0", "Claude 3 Sonnet (Base Model)"),
    ]
    
    for model_id, description in suggestions:
        print(f"  • {description}")
        print(f"    Model ID: {model_id}")
        print()
    
    # Ask if user wants to test
    print("Would you like to test these models? (y/n)")
    try:
        response = input("> ").strip().lower()
        if response == 'y':
            print()
            for model_id, description in suggestions:
                test_model_invoke(config, model_id)
    except (KeyboardInterrupt, EOFError):
        print("\n\nSkipping model tests")
    
    print("\n" + "=" * 60)
    print("Tips:")
    print("  1. If models show as available but fail to invoke,")
    print("     enable model access in AWS Bedrock Console")
    print("  2. Cross-region inference profiles (us.* prefix) often")
    print("     have better availability")
    print("  3. Update your .env with the working model ID:")
    print("     BEDROCK_MODEL_ID=<model_id_here>")
    print("=" * 60)


if __name__ == "__main__":
    main()