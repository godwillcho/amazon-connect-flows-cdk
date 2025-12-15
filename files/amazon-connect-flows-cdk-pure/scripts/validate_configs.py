#!/usr/bin/env python3
"""
Validate all configuration files.
"""
import sys
import json
from pathlib import Path


def validate_config_file(config_path: Path) -> bool:
    """Validate a single configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check required keys
        required_keys = ['instance_name', 'flows']
        for key in required_keys:
            if key not in config:
                print(f"❌ {config_path}: Missing required key '{key}'")
                return False
        
        # Validate flows
        for idx, flow in enumerate(config.get('flows', [])):
            required_flow_keys = ['filename', 'name', 'type']
            for key in required_flow_keys:
                if key not in flow:
                    print(f"❌ {config_path}: Flow {idx} missing required key '{key}'")
                    return False
        
        print(f"✅ {config_path}: Valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ {config_path}: Invalid JSON - {str(e)}")
        return False
    except Exception as e:
        print(f"❌ {config_path}: Error - {str(e)}")
        return False


def main():
    """Main validation function."""
    project_root = Path(__file__).parent.parent
    config_dir = project_root / 'config' / 'connect_flows'
    
    if not config_dir.exists():
        print(f"❌ Connect flows config directory not found: {config_dir}")
        sys.exit(1)
    
    all_valid = True
    config_files = list(config_dir.rglob('*.json'))
    
    if not config_files:
        print("❌ No configuration files found")
        sys.exit(1)
    
    print(f"Validating {len(config_files)} configuration files...\n")
    
    for config_file in config_files:
        if not validate_config_file(config_file):
            all_valid = False
    
    print()
    if all_valid:
        print("✅ All configuration files are valid")
        sys.exit(0)
    else:
        print("❌ Some configuration files have errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
