"""
Configuration loader for Amazon Connect flows.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class ConfigurationLoader:
    """
    Loads and validates flow configuration files.
    """
    
    REQUIRED_CONFIG_KEYS = ['instance_name', 'flows']
    REQUIRED_FLOW_KEYS = ['filename', 'name', 'type']
    
    def __init__(self, config_dir: Path):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Path to the configuration directory
        
        Raises:
            ValueError: If config_dir doesn't exist
        """
        if not config_dir.exists():
            raise ValueError(f"Configuration directory not found: {config_dir}")
        
        self.config_dir = config_dir
    
    def load_config(self, config_filename: str) -> Dict[str, Any]:
        """
        Load and validate a configuration file.
        
        Args:
            config_filename: Name of the configuration file
        
        Returns:
            Validated configuration dictionary
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If configuration is invalid
        """
        config_path = self.config_dir / config_filename
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        logger.info(f"Loading configuration from {config_path}")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Validate configuration
        self._validate_config(config, config_filename)
        
        logger.info(f"Successfully loaded configuration with {len(config.get('flows', []))} flows")
        
        return config
    
    def _validate_config(self, config: Dict[str, Any], filename: str) -> None:
        """
        Validate the configuration structure.
        
        Args:
            config: Configuration dictionary to validate
            filename: Name of the config file (for error messages)
        
        Raises:
            ValueError: If configuration is invalid
        """
        # Check required top-level keys
        for key in self.REQUIRED_CONFIG_KEYS:
            if key not in config:
                raise ValueError(f"Missing required key '{key}' in {filename}")
        
        # Validate instance_name
        if not config['instance_name'] or not isinstance(config['instance_name'], str):
            raise ValueError(f"Invalid instance_name in {filename}")
        
        # Validate flows
        flows = config.get('flows', [])
        if not isinstance(flows, list):
            raise ValueError(f"'flows' must be a list in {filename}")
        
        # Validate each flow
        for idx, flow in enumerate(flows):
            self._validate_flow_config(flow, filename, idx)
    
    def _validate_flow_config(
        self, 
        flow: Dict[str, Any], 
        filename: str, 
        idx: int
    ) -> None:
        """
        Validate a single flow configuration.
        
        Args:
            flow: Flow configuration dictionary
            filename: Name of the config file (for error messages)
            idx: Index of the flow in the flows list
        
        Raises:
            ValueError: If flow configuration is invalid
        """
        # Check required keys
        for key in self.REQUIRED_FLOW_KEYS:
            if key not in flow:
                raise ValueError(
                    f"Missing required key '{key}' in flow {idx} of {filename}"
                )
        
        # Validate flow type
        valid_types = [
            'CONTACT_FLOW',
            'CUSTOMER_QUEUE',
            'CUSTOMER_HOLD',
            'CUSTOMER_WHISPER',
            'AGENT_HOLD',
            'AGENT_WHISPER',
            'TRANSFER',
            'QUEUE_TRANSFER'
        ]
        
        if flow['type'] not in valid_types:
            raise ValueError(
                f"Invalid flow type '{flow['type']}' in flow {idx} of {filename}. "
                f"Must be one of: {', '.join(valid_types)}"
            )
        
        # Validate parameter_updates if present
        if 'parameter_updates' in flow:
            if not isinstance(flow['parameter_updates'], dict):
                raise ValueError(
                    f"'parameter_updates' must be a dictionary in flow {idx} of {filename}"
                )
