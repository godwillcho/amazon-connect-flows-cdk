#!/usr/bin/env python3
"""
Validate all flow JSON files.
"""
import sys
import json
from pathlib import Path


def validate_flow_file(flow_path: Path) -> bool:
    """Validate a single flow file."""
    try:
        with open(flow_path, 'r') as f:
            flow = json.load(f)
        
        # Check required keys
        if 'Actions' not in flow:
            print(f"❌ {flow_path}: Missing 'Actions' key")
            return False
        
        if 'Version' not in flow:
            print(f"⚠️  {flow_path}: Missing 'Version' key (optional but recommended)")
        
        print(f"✅ {flow_path}: Valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ {flow_path}: Invalid JSON - {str(e)}")
        return False
    except Exception as e:
        print(f"❌ {flow_path}: Error - {str(e)}")
        return False


def main():
    """Main validation function."""
    project_root = Path(__file__).parent.parent
    flows_dir = project_root / 'flows'
    
    if not flows_dir.exists():
        print(f"❌ Flows directory not found: {flows_dir}")
        sys.exit(1)
    
    all_valid = True
    flow_files = list(flows_dir.rglob('*.json'))
    
    if not flow_files:
        print("❌ No flow files found")
        sys.exit(1)
    
    print(f"Validating {len(flow_files)} flow files...\n")
    
    for flow_file in flow_files:
        if not validate_flow_file(flow_file):
            all_valid = False
    
    print()
    if all_valid:
        print("✅ All flow files are valid")
        sys.exit(0)
    else:
        print("❌ Some flow files have errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
