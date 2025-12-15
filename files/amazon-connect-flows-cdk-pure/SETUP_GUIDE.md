# Setup Guide

Complete guide for using Amazon Connect Flows CDK - both standalone and integrated into existing projects.

---

## 🎯 Two Usage Methods

1. **Standalone** - Use as a dedicated CDK project
2. **Integration** - Add to your existing CDK project

---

# Method 1: Standalone Usage

Use this CDK project on its own.

## Step 1: Extract Package

```bash
# Extract the archive
tar -xzf amazon-connect-flows-cdk-pure.tar.gz
cd amazon-connect-flows-cdk-pure

# Or with zip
unzip amazon-connect-flows-cdk-pure.zip
cd amazon-connect-flows-cdk-pure
```

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows Command Prompt:
.venv\Scripts\activate.bat
```

**Verify activation** - Your prompt should show `(.venv)`:
```bash
(.venv) user@machine:~/amazon-connect-flows-cdk-pure$
```

## Step 3: Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# (Optional) Install development dependencies for testing
pip install -r requirements-dev.txt
```

## Step 4: Configure AWS

```bash
# Configure AWS credentials (if not already done)
aws configure

# Verify configuration
aws sts get-caller-identity
```

## Step 5: Bootstrap CDK (First Time Only)

```bash
# Bootstrap CDK in your AWS account/region
cdk bootstrap

# Or specify account/region explicitly
cdk bootstrap aws://123456789012/us-east-1
```

## Step 6: Configure Connect Instance

Edit `config/connect_flows/dev/sales_flows_config.json`:

```json
{
  "instance_name": "your-connect-instance-name",
  "flows": [
    {
      "filename": "sales/sales_main_flow.json",
      "name": "SalesMainFlow",
      "type": "CONTACT_FLOW",
      "description": "Main sales contact flow",
      "parameter_updates": {
        "welcome-block-id": {
          "Text": "$.Attributes.welcomeMessage"
        }
      }
    }
  ]
}
```

**Key fields to update:**
- `instance_name` - Your Amazon Connect instance alias/name
- `filename` - Path to your flow JSON file (relative to `flows/`)
- `name` - Unique name for the flow in CDK
- `type` - Flow type (CONTACT_FLOW, CUSTOMER_HOLD, etc.)
- `parameter_updates` - Block IDs and parameters to update (optional)

## Step 7: Add Your Flow Files

Place your Amazon Connect flow JSON files in the `flows/` directory:

```bash
flows/
├── sales/
│   └── your_flow.json          # Your exported flow
└── support/
    └── your_support_flow.json
```

## Step 8: Validate Configuration

```bash
# Validate configuration files
python scripts/validate_configs.py

# Validate flow JSON files
python scripts/validate_flows.py
```

## Step 9: Preview Deployment

```bash
# See what will be deployed
cdk synth

# See differences from current state
cdk diff -c environment=dev
```

## Step 10: Deploy

```bash
# Deploy to development
cdk deploy --all -c environment=dev

# Deploy to staging
cdk deploy --all -c environment=staging

# Deploy to production
cdk deploy --all -c environment=prod
```

## Step 11: Verify Deployment

After successful deployment, check:
- AWS CloudFormation console for stack status
- Amazon Connect console for deployed flows
- CDK outputs for flow ARNs

## Daily Workflow

```bash
# 1. Activate virtual environment
cd amazon-connect-flows-cdk-pure
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Make changes to configs or flows
vim config/connect_flows/dev/sales_flows_config.json

# 3. Validate changes
python scripts/validate_configs.py

# 4. Preview changes
cdk diff -c environment=dev

# 5. Deploy
cdk deploy --all -c environment=dev

# 6. Deactivate when done
deactivate
```

---

# Method 2: Integration into Existing CDK Project

Add this to your existing CDK project.

## Step 1: Extract Package

```bash
# Extract to a temporary location
tar -xzf amazon-connect-flows-cdk-pure.tar.gz
```

## Step 2: Copy Files to Your Project

```bash
# Navigate to your existing CDK project
cd my-existing-cdk-project

# Copy the stack
cp ../amazon-connect-flows-cdk-pure/stacks/connect_flow_stack.py ./stacks/

# Copy utilities
mkdir -p utils/connect_flows
cp -r ../amazon-connect-flows-cdk-pure/utils/connect_flows/* ./utils/connect_flows/

# Copy configuration
mkdir -p config/connect_flows
cp -r ../amazon-connect-flows-cdk-pure/config/connect_flows/* ./config/connect_flows/

# Copy flow files
mkdir -p flows
cp -r ../amazon-connect-flows-cdk-pure/flows/* ./flows/

# (Optional) Copy tests
cp -r ../amazon-connect-flows-cdk-pure/tests/unit/test_connect_flow_stack.py ./tests/unit/
cp -r ../amazon-connect-flows-cdk-pure/tests/unit/test_flow_updater.py ./tests/unit/
cp -r ../amazon-connect-flows-cdk-pure/tests/unit/test_config_loader.py ./tests/unit/

# (Optional) Copy validation scripts
mkdir -p scripts
cp ../amazon-connect-flows-cdk-pure/scripts/validate_*.py ./scripts/
```

## Step 3: Verify Your Project Structure

After copying, your project should look like:

```
my-existing-cdk-project/
├── app.py                          # Your existing app
├── stacks/
│   ├── your_existing_stack.py      # Your existing stacks
│   └── connect_flow_stack.py       # ← NEW
├── utils/
│   ├── your_existing_utils/        # Your existing utils
│   └── connect_flows/              # ← NEW
│       ├── __init__.py
│       ├── flow_updater.py
│       └── config_loader.py
├── config/
│   ├── your_existing_config/       # Your existing configs
│   └── connect_flows/              # ← NEW
│       ├── dev/
│       ├── staging/
│       └── prod/
├── flows/                          # ← NEW
│   ├── sales/
│   └── support/
└── requirements.txt                # Your existing requirements
```

## Step 4: Update Dependencies

Add to your `requirements.txt`:

```txt
# Amazon Connect Flows CDK dependencies
aws-cdk-lib>=2.120.0
constructs>=10.0.0,<11.0.0
boto3>=1.34.0
```

Then install:

```bash
# Activate your existing virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install new dependencies
pip install -r requirements.txt
```

## Step 5: Update Your app.py

Add the Connect flows stack to your existing `app.py`:

```python
#!/usr/bin/env python3
import aws_cdk as cdk

# Your existing imports
from stacks.your_existing_stack import YourExistingStack

# NEW: Import Connect flows stack
from stacks.connect_flow_stack import ConnectFlowStack

app = cdk.App()

# Your existing stacks
existing_stack = YourExistingStack(
    app,
    "YourExistingStack",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION")
    )
)

# NEW: Add Connect flows stack
connect_flows_stack = ConnectFlowStack(
    app,
    "ConnectFlows-dev",
    environment="dev",
    config_filename="sales_flows_config.json",
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION")
    )
)

app.synth()
```

## Step 6: Configure Connect Instance

Edit `config/connect_flows/dev/sales_flows_config.json`:

```json
{
  "instance_name": "your-connect-instance-name",
  "flows": [
    {
      "filename": "sales/sales_main_flow.json",
      "name": "SalesMainFlow",
      "type": "CONTACT_FLOW",
      "parameter_updates": {
        "block-id": {
          "Text": "$.Attributes.greeting"
        }
      }
    }
  ]
}
```

## Step 7: Add Your Flow Files

Copy your Connect flow JSON files to `flows/`:

```bash
# Copy your exported flows
cp ~/Downloads/my_connect_flow.json ./flows/sales/
```

## Step 8: Validate Integration

```bash
# Verify imports work
python -c "from stacks.connect_flow_stack import ConnectFlowStack; print('✓ Import successful')"

# Synthesize CloudFormation
cdk synth

# List all stacks (should include your new Connect stack)
cdk list
```

## Step 9: Deploy

```bash
# Deploy only the Connect flows stack
cdk deploy ConnectFlows-dev -c environment=dev

# Or deploy all stacks
cdk deploy --all
```

## Step 10: Verify Integration

Check that:
- ✅ Existing stacks still work
- ✅ Connect flows stack deploys successfully
- ✅ No dependency conflicts
- ✅ Flows appear in Amazon Connect console

---

# Configuration Guide

## Environment Variables

You can override config values with CDK context:

```bash
# Override instance name
cdk deploy --all -c environment=dev -c connectInstanceName=my-instance

# Override queue ARN
cdk deploy --all -c environment=dev -c queueArn=arn:aws:connect:...
```

## Multiple Stacks

Deploy different flow groups to separate stacks:

```python
# In app.py

# Sales flows stack
sales_stack = ConnectFlowStack(
    app,
    "ConnectFlows-Sales-dev",
    environment="dev",
    config_filename="sales_flows_config.json"
)

# Support flows stack
support_stack = ConnectFlowStack(
    app,
    "ConnectFlows-Support-dev",
    environment="dev",
    config_filename="support_flows_config.json"
)
```

## Environment-Specific Configs

Use different configs per environment:

```bash
config/connect_flows/
├── dev/
│   ├── sales_flows_config.json      # Dev instance
│   └── support_flows_config.json
├── staging/
│   ├── sales_flows_config.json      # Staging instance
│   └── support_flows_config.json
└── prod/
    ├── sales_flows_config.json      # Production instance
    └── support_flows_config.json
```

Deploy to different environments:

```bash
cdk deploy --all -c environment=dev      # Uses dev/ configs
cdk deploy --all -c environment=staging  # Uses staging/ configs
cdk deploy --all -c environment=prod     # Uses prod/ configs
```

---

# Testing

## Run Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_flow_updater.py

# Run with coverage
pytest --cov=stacks --cov=utils/connect_flows --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# Or navigate to htmlcov/index.html in browser
```

## Run Validation Scripts

```bash
# Validate all config files
python scripts/validate_configs.py

# Validate all flow files
python scripts/validate_flows.py
```

---

# Common Tasks

## Update Flow Parameters

```bash
# 1. Edit config file
vim config/connect_flows/dev/sales_flows_config.json

# Add or modify parameter_updates
{
  "parameter_updates": {
    "block-id-here": {
      "Text": "$.Attributes.newGreeting"
    }
  }
}

# 2. Validate
python scripts/validate_configs.py

# 3. Deploy
cdk deploy --all -c environment=dev
```

## Add New Flow

```bash
# 1. Export flow from Amazon Connect console
# Download flow JSON file

# 2. Copy to flows directory
cp ~/Downloads/new_flow.json ./flows/sales/

# 3. Add to config
vim config/connect_flows/dev/sales_flows_config.json

# Add new flow entry:
{
  "flows": [
    {
      "filename": "sales/new_flow.json",
      "name": "NewFlow",
      "type": "CONTACT_FLOW"
    }
  ]
}

# 4. Validate
python scripts/validate_flows.py
python scripts/validate_configs.py

# 5. Deploy
cdk deploy --all -c environment=dev
```

## Remove Flow

```bash
# 1. Remove from config
vim config/connect_flows/dev/sales_flows_config.json

# Remove the flow entry from "flows" array

# 2. Deploy (will remove from Connect)
cdk deploy --all -c environment=dev

# 3. (Optional) Delete flow file
rm flows/sales/old_flow.json
```

---

# Troubleshooting

## Virtual Environment Issues

**Problem:** `source: command not found`
```bash
# Solution: Use correct activation command for your shell
# Bash/Zsh:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1
```

**Problem:** Virtual environment not activating
```bash
# Remove and recreate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CDK Issues

**Problem:** `cdk: command not found`
```bash
# Install CDK CLI globally
npm install -g aws-cdk

# Verify
cdk --version
```

**Problem:** `This stack uses assets, so the toolkit stack must be deployed`
```bash
# Bootstrap CDK
cdk bootstrap
```

**Problem:** `Unable to resolve AWS account`
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-key
export AWS_DEFAULT_REGION=us-east-1
```

## Import Issues

**Problem:** `ModuleNotFoundError: No module named 'stacks'`
```bash
# Solution 1: Make sure you're in the right directory
cd amazon-connect-flows-cdk-pure

# Solution 2: Install in development mode
pip install -e .

# Solution 3: Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Problem:** `ModuleNotFoundError: No module named 'aws_cdk'`
```bash
# Activate virtual environment first
source .venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

## Configuration Issues

**Problem:** `Configuration file not found`
```bash
# Check file path
ls config/connect_flows/dev/

# Verify filename in app.py matches actual file
config_filename="sales_flows_config.json"  # Must match actual filename
```

**Problem:** `Instance not found`
```bash
# Verify instance name in config matches actual Connect instance
# Get instance name from AWS console:
# Amazon Connect → Instances → Instance alias
```

## Deployment Issues

**Problem:** `Stack already exists`
```bash
# Update existing stack instead
cdk deploy --all -c environment=dev

# Or destroy and recreate
cdk destroy ConnectFlows-dev
cdk deploy ConnectFlows-dev -c environment=dev
```

**Problem:** `Access denied`
```bash
# Verify IAM permissions
# Required permissions:
# - cloudformation:*
# - connect:*
# - lambda:* (if using Lambda functions)
# - iam:PassRole
```

---

# Quick Reference

## Standalone Setup

```bash
tar -xzf amazon-connect-flows-cdk-pure.tar.gz
cd amazon-connect-flows-cdk-pure
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Edit: config/connect_flows/dev/sales_flows_config.json
cdk bootstrap
cdk deploy --all -c environment=dev
```

## Integration Setup

```bash
cd my-project
cp -r amazon-connect-flows-cdk-pure/stacks/connect_flow_stack.py ./stacks/
cp -r amazon-connect-flows-cdk-pure/utils/connect_flows ./utils/
cp -r amazon-connect-flows-cdk-pure/config/connect_flows ./config/
cp -r amazon-connect-flows-cdk-pure/flows ./flows/
pip install -r requirements.txt
# Edit: app.py (add ConnectFlowStack)
# Edit: config/connect_flows/dev/sales_flows_config.json
cdk deploy --all
```

## Daily Commands

```bash
source .venv/bin/activate                    # Start
python scripts/validate_configs.py          # Validate
cdk diff -c environment=dev                 # Preview
cdk deploy --all -c environment=dev         # Deploy
deactivate                                  # Stop
```

---

# Summary

## For Standalone Use:
1. ✅ Extract package
2. ✅ Create virtual environment
3. ✅ Install dependencies
4. ✅ Configure Connect instance
5. ✅ Add flow files
6. ✅ Deploy

## For Integration:
1. ✅ Copy files to your project
2. ✅ Update dependencies
3. ✅ Update app.py
4. ✅ Configure Connect instance
5. ✅ Add flow files
6. ✅ Deploy

**Both methods are production-ready and fully supported!** 🚀
