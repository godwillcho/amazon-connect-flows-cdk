"""
Unit tests for FlowParameterUpdater.
"""
import pytest
from utils.connect_flows.flow_updater import FlowParameterUpdater


def test_flow_updater_initialization():
    """Test FlowParameterUpdater initialization."""
    flow_content = {
        "Version": "2019-10-30",
        "Actions": []
    }
    
    updater = FlowParameterUpdater(flow_content)
    assert updater.flow_content == flow_content
    assert updater.updated_blocks == []
    assert updater.failed_updates == []


def test_flow_updater_invalid_content():
    """Test FlowParameterUpdater with invalid content."""
    with pytest.raises(ValueError):
        FlowParameterUpdater({})
    
    with pytest.raises(ValueError):
        FlowParameterUpdater("invalid")


def test_update_block_parameters():
    """Test updating block parameters."""
    flow_content = {
        "Version": "2019-10-30",
        "Actions": [
            {
                "Identifier": "test-id",
                "Type": "MessageParticipant",
                "Parameters": {
                    "Text": "Old text"
                }
            }
        ]
    }
    
    updater = FlowParameterUpdater(flow_content)
    updater.update_block_parameters("test-id", {"Text": "New text"})
    
    assert flow_content["Actions"][0]["Parameters"]["Text"] == "New text"
    assert "test-id" in updater.updated_blocks


def test_update_nonexistent_block():
    """Test updating a block that doesn't exist."""
    flow_content = {
        "Version": "2019-10-30",
        "Actions": []
    }
    
    updater = FlowParameterUpdater(flow_content)
    updater.update_block_parameters("nonexistent-id", {"Text": "Test"})
    
    assert "nonexistent-id" in updater.failed_updates
    assert len(updater.updated_blocks) == 0


def test_validate_updates():
    """Test validation of updates."""
    flow_content = {
        "Version": "2019-10-30",
        "Actions": [
            {
                "Identifier": "test-id",
                "Type": "MessageParticipant",
                "Parameters": {}
            }
        ]
    }
    
    updater = FlowParameterUpdater(flow_content)
    updater.update_block_parameters("test-id", {"Text": "Test"})
    updater.update_block_parameters("nonexistent", {"Text": "Test"})
    
    validation = updater.validate_updates()
    
    assert validation["total_blocks"] == 1
    assert validation["updated_blocks"] == 1
    assert validation["failed_updates"] == 1


def test_update_multiple_blocks():
    """Test updating multiple blocks at once."""
    flow_content = {
        "Version": "2019-10-30",
        "Actions": [
            {
                "Identifier": "block-1",
                "Type": "MessageParticipant",
                "Parameters": {"Text": "Old 1"}
            },
            {
                "Identifier": "block-2",
                "Type": "MessageParticipant",
                "Parameters": {"Text": "Old 2"}
            }
        ]
    }
    
    updater = FlowParameterUpdater(flow_content)
    updater.update_multiple_blocks({
        "block-1": {"Text": "New 1"},
        "block-2": {"Text": "New 2"}
    })
    
    assert flow_content["Actions"][0]["Parameters"]["Text"] == "New 1"
    assert flow_content["Actions"][1]["Parameters"]["Text"] == "New 2"
    assert len(updater.updated_blocks) == 2


def test_get_content_json():
    """Test getting content as JSON string."""
    flow_content = {
        "Version": "2019-10-30",
        "Actions": []
    }
    
    updater = FlowParameterUpdater(flow_content)
    json_str = updater.get_content_json()
    
    assert isinstance(json_str, str)
    assert "Version" in json_str
    assert "Actions" in json_str
