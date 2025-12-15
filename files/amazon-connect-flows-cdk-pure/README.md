# Amazon Connect Flows CDK

AWS CDK stack for deploying Amazon Connect contact flows with environment-based configuration.

## Installation

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete setup instructions.**

### Quick Standalone Setup

```bash
# Extract and setup
tar -xzf amazon-connect-flows-cdk-pure.tar.gz
cd amazon-connect-flows-cdk-pure

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux: .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure and deploy
# Edit: config/connect_flows/dev/sales_flows_config.json
cdk bootstrap  # First time only
cdk deploy --all -c environment=dev
```

### Quick Integration Setup

```bash
# Copy to your existing CDK project
cd my-existing-cdk-project
cp -r path/to/stacks/connect_flow_stack.py ./stacks/
cp -r path/to/utils/connect_flows ./utils/
cp -r path/to/config/connect_flows ./config/
cp -r path/to/flows ./flows/

# Update your app.py and deploy
```

## Usage

### In Your app.py

```python
from stacks.connect_flow_stack import ConnectFlowStack

# Create stack
ConnectFlowStack(
    app,
    "ConnectFlows-dev",
    environment="dev",
    config_filename="sales_flows_config.json"
)
```

### Configure

Edit `config/connect_flows/dev/sales_flows_config.json`:

```json
{
  "instance_name": "your-connect-instance",
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

### Deploy

```bash
cdk deploy --all -c environment=dev
```

## Structure

```
├── stacks/                     # CDK stacks
│   └── connect_flow_stack.py
├── utils/                      # Utilities
│   └── connect_flows/
│       ├── flow_updater.py
│       └── config_loader.py
├── config/                     # Configuration
│   └── connect_flows/
│       ├── dev/
│       ├── staging/
│       └── prod/
├── flows/                      # Flow JSON files
│   ├── sales/
│   └── support/
├── tests/                      # Tests
└── scripts/                    # Validation scripts
```

## Features

- Environment-based configuration (dev, staging, prod)
- Automated parameter updates for flows
- Type-safe Python with full type hints
- Validation scripts for configs and flows

## Requirements

- Python 3.8+
- AWS CDK 2.120.0+
- AWS credentials configured

## License

MIT License
