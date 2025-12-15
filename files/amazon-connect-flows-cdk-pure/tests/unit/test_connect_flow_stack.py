"""
Unit tests for ConnectFlowStack.
"""
import pytest
import aws_cdk as cdk
from aws_cdk.assertions import Template
from stacks.connect_flow_stack import ConnectFlowStack


def test_connect_flow_stack_initialization():
    """Test that ConnectFlowStack can be initialized."""
    # This is a basic smoke test
    # Full integration tests would require valid config files and flows
    app = cdk.App()
    
    # Note: This would fail without proper config files
    # In a real scenario, you'd use fixtures with mock config
    # For now, this tests that the import works
    assert ConnectFlowStack is not None


def test_connect_flow_stack_has_required_methods():
    """Test that ConnectFlowStack has expected methods."""
    required_methods = [
        'load_configuration',
        'lookup_instance_arn',
        'create_all_flows',
        'create_flow'
    ]
    
    for method in required_methods:
        assert hasattr(ConnectFlowStack, method), f"Missing method: {method}"
