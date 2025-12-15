"""
Unit tests for ConfigurationLoader.
"""
import pytest
import json
from pathlib import Path
from utils.connect_flows.config_loader import ConfigurationLoader


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def valid_config():
    """Return a valid configuration."""
    return {
        "instance_name": "test-instance",
        "queue_arn": "arn:aws:connect:us-east-1:123456789012:instance/test/queue/test",
        "flows": [
            {
                "filename": "test.json",
                "name": "TestFlow",
                "type": "CONTACT_FLOW",
                "description": "Test flow"
            }
        ]
    }


def test_config_loader_initialization(temp_config_dir):
    """Test ConfigurationLoader initialization."""
    loader = ConfigurationLoader(temp_config_dir)
    assert loader.config_dir == temp_config_dir


def test_config_loader_invalid_directory():
    """Test ConfigurationLoader with invalid directory."""
    with pytest.raises(ValueError):
        ConfigurationLoader(Path("/nonexistent/directory"))


def test_load_valid_config(temp_config_dir, valid_config):
    """Test loading a valid configuration."""
    config_file = temp_config_dir / "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(valid_config, f)
    
    loader = ConfigurationLoader(temp_config_dir)
    loaded_config = loader.load_config("test_config.json")
    
    assert loaded_config == valid_config


def test_load_missing_config(temp_config_dir):
    """Test loading a missing configuration file."""
    loader = ConfigurationLoader(temp_config_dir)
    
    with pytest.raises(FileNotFoundError):
        loader.load_config("nonexistent.json")


def test_validate_config_missing_keys(temp_config_dir):
    """Test validation with missing required keys."""
    invalid_config = {
        "instance_name": "test"
        # Missing 'flows' key
    }
    
    config_file = temp_config_dir / "invalid_config.json"
    with open(config_file, 'w') as f:
        json.dump(invalid_config, f)
    
    loader = ConfigurationLoader(temp_config_dir)
    
    with pytest.raises(ValueError):
        loader.load_config("invalid_config.json")


def test_validate_flow_invalid_type(temp_config_dir):
    """Test validation with invalid flow type."""
    invalid_config = {
        "instance_name": "test",
        "flows": [
            {
                "filename": "test.json",
                "name": "TestFlow",
                "type": "INVALID_TYPE"
            }
        ]
    }
    
    config_file = temp_config_dir / "invalid_config.json"
    with open(config_file, 'w') as f:
        json.dump(invalid_config, f)
    
    loader = ConfigurationLoader(temp_config_dir)
    
    with pytest.raises(ValueError):
        loader.load_config("invalid_config.json")


def test_validate_flow_missing_required_keys(temp_config_dir):
    """Test validation with missing flow required keys."""
    invalid_config = {
        "instance_name": "test",
        "flows": [
            {
                "filename": "test.json",
                "name": "TestFlow"
                # Missing 'type' key
            }
        ]
    }
    
    config_file = temp_config_dir / "invalid_config.json"
    with open(config_file, 'w') as f:
        json.dump(invalid_config, f)
    
    loader = ConfigurationLoader(temp_config_dir)
    
    with pytest.raises(ValueError):
        loader.load_config("invalid_config.json")
