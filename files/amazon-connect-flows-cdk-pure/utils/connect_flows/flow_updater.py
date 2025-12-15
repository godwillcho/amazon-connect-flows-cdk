"""
Flow parameter updater utility for Amazon Connect flows.
"""
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class FlowParameterUpdater:
    """
    A utility class to update Amazon Connect flow parameters by block identifier.
    """
    
    def __init__(self, flow_content: Dict[str, Any]):
        """
        Initialize the updater with flow content.
        
        Args:
            flow_content: The parsed JSON content of the Connect flow
        
        Raises:
            ValueError: If flow_content is invalid
        """
        if not isinstance(flow_content, dict):
            raise ValueError("flow_content must be a dictionary")
        
        if 'Actions' not in flow_content:
            raise ValueError("flow_content must contain 'Actions' key")
        
        self.flow_content = flow_content
        self.updated_blocks: List[str] = []
        self.failed_updates: List[str] = []
    
    def update_block_parameters(
        self, 
        identifier: str, 
        parameters: Dict[str, Any],
        merge: bool = True
    ) -> 'FlowParameterUpdater':
        """
        Update parameters for a specific block by its identifier.
        
        Args:
            identifier: The unique identifier of the block to update
            parameters: Dictionary of parameters to update
            merge: If True, merge with existing parameters. If False, replace entirely.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValueError: If identifier or parameters are invalid
        """
        if not identifier:
            raise ValueError("identifier cannot be empty")
        
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dictionary")
        
        block_found = False
        
        for action in self.flow_content.get('Actions', []):
            if action.get('Identifier') == identifier:
                block_found = True
                
                if 'Parameters' not in action:
                    action['Parameters'] = {}
                
                if merge:
                    action['Parameters'].update(parameters)
                else:
                    action['Parameters'] = parameters
                
                self.updated_blocks.append(identifier)
                logger.info(f"Updated block {identifier}")
                break
        
        if not block_found:
            self.failed_updates.append(identifier)
            logger.warning(f"Block with identifier '{identifier}' not found in flow")
        
        return self
    
    def update_multiple_blocks(
        self, 
        updates: Dict[str, Dict[str, Any]],
        merge: bool = True
    ) -> 'FlowParameterUpdater':
        """
        Update multiple blocks at once.
        
        Args:
            updates: Dictionary mapping block identifiers to their parameter updates
            merge: If True, merge with existing parameters. If False, replace entirely.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValueError: If updates is invalid
        """
        if not isinstance(updates, dict):
            raise ValueError("updates must be a dictionary")
        
        for identifier, parameters in updates.items():
            self.update_block_parameters(identifier, parameters, merge)
        
        return self
    
    def validate_updates(self) -> Dict[str, Any]:
        """
        Validate the updates and return a summary.
        
        Returns:
            Dictionary containing update statistics
        """
        return {
            'total_blocks': len(self.flow_content.get('Actions', [])),
            'updated_blocks': len(self.updated_blocks),
            'failed_updates': len(self.failed_updates),
            'updated_identifiers': self.updated_blocks,
            'failed_identifiers': self.failed_updates
        }
    
    def get_content_json(self, indent: Optional[int] = None) -> str:
        """
        Get the updated flow content as a JSON string.
        
        Args:
            indent: Number of spaces for indentation (None for compact)
        
        Returns:
            The modified flow content as a JSON string
        """
        return json.dumps(self.flow_content, indent=indent)
    
    def get_content(self) -> Dict[str, Any]:
        """
        Get the updated flow content as a dictionary.
        
        Returns:
            The modified flow content
        """
        return self.flow_content
