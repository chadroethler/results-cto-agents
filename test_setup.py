#!/usr/bin/env python3
"""
Test setup and validate configuration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 60)
print("Results CTO Agents - Setup Validation")
print("=" * 60)
print()

errors = []
warnings = []

# Check Python version
print("✓ Python version:", sys.version.split()[0])

# Check environment variables
print("\nChecking environment variables...")

required_vars = [
    'SPREADSHEET_ID',
    'CREDENTIALS_FILE',
]

optional_vars = [
    'REDDIT_CLIENT_ID',
    'REDDIT_CLIENT_SECRET',
    'REDDIT_USER_AGENT',
    'GCP_PROJECT_ID',
    'GCP_REGION'
]

for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        display_value = value[:10] + "..." if len(value) > 10 else value
        print(f"  ✓ {var}: {display_value}")
    else:
        errors.append(f"Missing required variable: {var}")
        print(f"  ✗ {var}: NOT SET")

for var in optional_vars:
    value = os.getenv(var)
    if value:
        display_value = value[:10] + "..." if len(value) > 10 else value
        print(f"  ✓ {var}: {display_value}")
    else:
        warnings.append(f"Optional variable not set: {var}")
        print(f"  ⚠ {var}: NOT SET (optional)")

# Check credentials file
print("\nChecking credentials file...")
creds_file = os.getenv('CREDENTIALS_FILE', 'credentials.json')
if os.path.exists(creds_file):
    print(f"  ✓ Credentials file found: {creds_file}")
else:
    errors.append(f"Credentials file not found: {creds_file}")
    print(f"  ✗ Credentials file not found: {creds_file}")

# Check config files
print("\nChecking configuration files...")
config_files = [
    'config/agent_3_sources.json',
    'config/agent_3_keywords.json',
    'config/agent_4_sources.json',
    'config/agent_4_keywords.json'
]

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"  ✓ {config_file}")
    else:
        errors.append(f"Config file not found: {config_file}")
        print(f"  ✗ {config_file}")

# Check directories
print("\nChecking directory structure...")
required_dirs = [
    'agents/shared',
    'agents/agent_3',
    'agents/agent_4',
    'config',
    'logs'
]

for directory in required_dirs:
    if os.path.exists(directory):
        print(f"  ✓ {directory}")
    else:
        os.makedirs(directory, exist_ok=True)
        print(f"  ⚠ Created: {directory}")

# Try importing modules
print("\nChecking Python dependencies...")
try:
    import feedparser
    print("  ✓ feedparser")
except ImportError:
    errors.append("feedparser not installed")
    print("  ✗ feedparser")

try:
    import praw
    print("  ✓ praw")
except ImportError:
    errors.append("praw not installed")
    print("  ✗ praw")

try:
    from google.oauth2.service_account import Credentials
    print("  ✓ google-api-python-client")
except ImportError:
    errors.append("google-api-python-client not installed")
    print("  ✗ google-api-python-client")

# Test Google Sheets connection (optional)
print("\nTesting Google Sheets connection...")
if os.path.exists(creds_file) and os.getenv('SPREADSHEET_ID'):
    try:
        sys.path.insert(0, 'agents')
        from shared.sheets_client import SheetsClient
        
        client = SheetsClient()
        print("  ✓ Successfully connected to Google Sheets")
    except Exception as e:
        warnings.append(f"Could not connect to Google Sheets: {str(e)}")
        print(f"  ⚠ Could not connect: {str(e)[:100]}")
else:
    print("  ⚠ Skipping (credentials or spreadsheet ID not configured)")

# Summary
print()
print("=" * 60)
if errors:
    print("❌ VALIDATION FAILED")
    print()
    print("Errors:")
    for error in errors:
        print(f"  - {error}")
    print()
    print("Fix these errors before proceeding.")
    sys.exit(1)
else:
    print("✅ VALIDATION PASSED")
    if warnings:
        print()
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    print()
    print("Setup is complete! You can now run the agents.")
    print()
    print("Next steps:")
    print("  1. Test Agent 3: python3 agents/agent_3/agent.py")
    print("  2. Test Agent 4: python3 agents/agent_4/agent.py")
    print("  3. Deploy to GCP: ./scripts/deploy_gcp.sh")

print("=" * 60)
