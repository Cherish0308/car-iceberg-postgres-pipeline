#!/usr/bin/env python3
"""
Run Lambda handler with real AWS S3 and Postgres
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import lambda_handler

if __name__ == "__main__":
    # Get S3 details from command line or use defaults
    bucket = sys.argv[1] if len(sys.argv) > 1 else "carproject-bucket"
    key = sys.argv[2] if len(sys.argv) > 2 else "c.json"
    
    event = {
        "bucket": bucket,
        "key": key
    }
    
    print(f"Running Lambda Handler with real infrastructure...")
    print(f"Bucket: {bucket}")
    print(f"Key: {key}")
    print("-" * 60)
    
    try:
        result = lambda_handler(event, {})
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: {result}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
