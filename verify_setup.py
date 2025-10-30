#!/usr/bin/env python3
"""
Setup verification script for Storyblok Voice Assistant.
Checks that all dependencies and configurations are correct.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required Python packages are installed."""
    required = [
        "fastapi",
        "uvicorn",
        "httpx",
        "pydantic",
        "pydantic_settings",
        "boto3",
        "pytest"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages: pip install {' '.join(missing)}")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Copy .env.example to .env and configure it")
        return False
    
    print("✅ .env file exists")
    
    # Read and check for required variables
    required_vars = [
        "AWS_BEARER_TOKEN_BEDROCK",
        "STORYBLOK_TOKEN",
        "STORYBLOK_SPACE_ID"
    ]
    
    env_content = env_path.read_text()
    missing = []
    
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=your_" in env_content or f"{var}=<" in env_content:
            missing.append(var)
            print(f"⚠️  {var} not configured")
        else:
            print(f"✅ {var} configured")
    
    if missing:
        print("\n⚠️  Configure missing variables in .env file")
        return False
    
    return True


def check_project_structure():
    """Check if all required directories and files exist."""
    required_paths = [
        "backend/__init__.py",
        "backend/main.py",
        "backend/config.py",
        "backend/models.py",
        "backend/bedrock_client.py",
        "backend/storyblok_client.py",
        "frontend/index.html",
        "tests/test_main.py",
        "requirements.txt"
    ]
    
    all_exist = True
    for path in required_paths:
        if Path(path).exists():
            print(f"✅ {path}")
        else:
            print(f"❌ {path} missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks."""
    print("🔍 Verifying Storyblok Voice Assistant Setup\n")
    
    print("=" * 50)
    print("Checking Python Version...")
    print("=" * 50)
    python_ok = check_python_version()
    print()
    
    print("=" * 50)
    print("Checking Dependencies...")
    print("=" * 50)
    deps_ok = check_dependencies()
    print()
    
    print("=" * 50)
    print("Checking Environment Configuration...")
    print("=" * 50)
    env_ok = check_env_file()
    print()
    
    print("=" * 50)
    print("Checking Project Structure...")
    print("=" * 50)
    structure_ok = check_project_structure()
    print()
    
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    
    all_ok = python_ok and deps_ok and env_ok and structure_ok
    
    if all_ok:
        print("✅ All checks passed!")
        print("\n🚀 You can start the application with:")
        print("   ./run.sh")
        print("   or")
        print("   python -m uvicorn backend.main:app --reload")
        return 0
    else:
        print("❌ Some checks failed")
        print("\n📖 See docs/SETUP.md for detailed setup instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())