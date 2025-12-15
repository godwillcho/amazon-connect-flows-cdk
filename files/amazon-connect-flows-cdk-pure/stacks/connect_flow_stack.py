"""
CDK Stack for deploying Amazon Connect flows.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import boto3
from aws_cdk import (
    Stack,
    aws_connect as connect,
    CfnOutput,
    Tags
)
from constructs import Construct

from utils.connect_flows.flow_updater import FlowParameterUpdater
from utils.connect_flows.config_loader import ConfigurationLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConnectFlowStack(Stack):
    """
    CDK Stack for deploying Amazon Connect flows using configuration files.
    All parameter values are contact attributes.
    """
    
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        environment: str,
        config_filename: str,
        **kwargs
    ) -> None:
        """
        Initialize the Connect Flow Stack.
        
        Args:
            scope: CDK app scope
            construct_id: Unique identifier for this stack
            environment: Environment name (dev, staging, prod)
            config_filename: Name of the configuration file
            **kwargs: Additional stack arguments
        """
        super().__init__(scope, construct_id, **kwargs)
        
        self.environment = environment
        
        # Get project root directory
        project_root = Path(__file__).parent.parent
        
        # Define directory paths
        self.flows_dir = project_root / 'flows'
        self.config_dir = project_root / 'config' / 'connect_flows' / environment
        self.config_filename = config_filename
        
        # Validate directories exist
        self._validate_directories()
        
        # Load configuration
        self.config_loader = ConfigurationLoader(self.config_dir)
        self.load_configuration()
        
        # Lookup instance ARN from instance name
        self.lookup_instance_arn()
        
        # Add stack tags
        self._add_stack_tags()
        
        # Create all flows based on configuration
        self.create_all_flows()
    
    def _validate_directories(self) -> None:
        """
        Validate that required directories exist.
        
        Raises:
            FileNotFoundError: If required directories don't exist
        """
        if not self.flows_dir.exists():
            raise FileNotFoundError(f"Flows directory not found: {self.flows_dir}")
        
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")
    
    def _add_stack_tags(self) -> None:
        """Add tags to all resources in the stack."""
        Tags.of(self).add("Environment", self.environment)
        Tags.of(self).add("ManagedBy", "CDK")
        Tags.of(self).add("Application", "AmazonConnect")
    
    def load_configuration(self) -> None:
        """
        Load flow configuration from the specified config file.
        """
        try:
            config = self.config_loader.load_config(self.config_filename)
            
            # Extract configuration values
            self.instance_name = config.get('instance_name')
            self.queue_arn = config.get('queue_arn')
            self.flow_configs = config.get('flows', [])
            
            # Allow CDK context to override configuration file values
            self.instance_name = self.node.try_get_context("connectInstanceName") or self.instance_name
            self.queue_arn = self.node.try_get_context("queueArn") or self.queue_arn
            
            logger.info(f"Loaded configuration for {len(self.flow_configs)} flows from {self.config_filename}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            raise
    
    def lookup_instance_arn(self) -> None:
        """
        Lookup the Connect instance ARN using the instance alias/name.
        
        In production, this should use boto3 to lookup the actual instance ID.
        For now, we construct the ARN using the instance alias.
        """
        try:
            # TODO: In production, use boto3 to lookup actual instance ID
            # connect_client = boto3.client('connect', region_name=self.region)
            # response = connect_client.list_instances()
            # Find instance by alias and get actual instance ID
            
            # For now, construct ARN using instance alias
            self.instance_arn = f"arn:aws:connect:{self.region}:{self.account}:instance/{self.instance_name}"
            
            logger.info(f"Using Connect instance ARN: {self.instance_arn}")
            
        except Exception as e:
            logger.error(f"Failed to lookup instance ARN: {str(e)}")
            raise
    
    def create_all_flows(self) -> None:
        """
        Create all flows based on configuration.
        Flows with parameter_updates will be updated, others loaded directly.
        """
        for config in self.flow_configs:
            try:
                self.create_flow(config)
            except Exception as e:
                logger.error(f"Error creating flow {config.get('name', 'Unknown')}: {str(e)}")
                raise
    
    def create_flow(self, config: Dict[str, Any]) -> connect.CfnContactFlow:
        """
        Create a flow from configuration.
        
        Args:
            config: Flow configuration dictionary
        
        Returns:
            Created CfnContactFlow
        
        Raises:
            FileNotFoundError: If flow file doesn't exist
            Exception: If flow creation fails
        """
        # Load flow content
        flow_path = self.flows_dir / config['filename']
        
        if not flow_path.exists():
            raise FileNotFoundError(f"Flow file not found: {flow_path}")
        
        logger.info(f"Loading flow from {flow_path}")
        
        with open(flow_path, 'r') as f:
            flow_content = json.load(f)
        
        # Check if this flow needs parameter updates
        if 'parameter_updates' in config and config['parameter_updates']:
            # Use parameter updates directly (all values are contact attributes)
            parameter_updates = config['parameter_updates']
            
            # Update parameters
            updater = FlowParameterUpdater(flow_content)
            updater.update_multiple_blocks(parameter_updates)
            
            # Validate
            validation = updater.validate_updates()
            logger.info(f"✓ {config['name']}: Updated {validation['updated_blocks']} blocks")
            
            if validation['failed_updates'] > 0:
                logger.warning(
                    f"Failed to update {validation['failed_updates']} blocks in {config['name']}"
                )
                logger.warning(f"Failed identifiers: {validation['failed_identifiers']}")
            
            flow_content_json = updater.get_content_json()
        else:
            # No updates needed, use flow as-is
            flow_content_json = json.dumps(flow_content)
            logger.info(f"✓ {config['name']}: Loaded directly without updates")
        
        # Create the contact flow
        flow = connect.CfnContactFlow(
            self,
            config['name'],
            instance_arn=self.instance_arn,
            name=config['name'],
            type=config['type'],
            content=flow_content_json,
            description=config.get('description', ''),
            state="ACTIVE",
            tags=[
                {
                    'key': 'Environment',
                    'value': self.environment
                },
                {
                    'key': 'FlowType',
                    'value': config['type']
                }
            ]
        )
        
        # Create output
        CfnOutput(
            self,
            f"{config['name']}Arn",
            value=flow.attr_contact_flow_arn,
            description=f"ARN of {config['name']}",
            export_name=f"{self.stack_name}-{config['name']}-Arn"
        )
        
        logger.info(f"Successfully created flow: {config['name']}")
        
        return flow
