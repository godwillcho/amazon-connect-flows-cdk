#!/usr/bin/env python3
"""
CDK application for deploying Amazon Connect flows.
"""
import os
import logging

import aws_cdk as cdk

from stacks import ConnectFlowStack

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = cdk.App()

# Get environment from context or default to 'dev'
environment = app.node.try_get_context("environment") or os.getenv("ENVIRONMENT", "dev")

# Get AWS account and region
account = os.getenv('CDK_DEFAULT_ACCOUNT')
region = os.getenv('CDK_DEFAULT_REGION', 'us-east-1')

logger.info(f"Deploying to environment: {environment}")
logger.info(f"Account: {account}, Region: {region}")

# Define CDK environment
env = cdk.Environment(account=account, region=region)

# Sales flows stack
sales_stack = ConnectFlowStack(
    app,
    f"SalesFlowsStack-{environment}",
    environment=environment,
    config_filename="sales_flows_config.json",
    env=env,
    description=f"Amazon Connect Sales flows for {environment} environment"
)

# Support flows stack
support_stack = ConnectFlowStack(
    app,
    f"SupportFlowsStack-{environment}",
    environment=environment,
    config_filename="support_flows_config.json",
    env=env,
    description=f"Amazon Connect Support flows for {environment} environment"
)

app.synth()
