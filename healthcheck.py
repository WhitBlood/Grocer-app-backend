#!/usr/bin/env python3
"""
Health check script for Docker container.
Returns exit code 0 if healthy, 1 if unhealthy.
"""
import sys
import requests

def check_health():
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        
        if response.status_code != 200:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
        
        data = response.json()
        
        if data.get('status') != 'healthy':
            print(f"❌ Service unhealthy: {data.get('status')}")
            return False
        
        if data.get('database') != 'connected':
            print(f"❌ Database not connected: {data.get('database')}")
            return False
        
        print(f"✅ Health check passed: {data}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)
