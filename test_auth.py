#!/usr/bin/env python3
"""
Test script to verify OAuth2 authentication with Asana.
Run this after setting up your Asana OAuth app and .env file.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.client import get_client


def main():
    print("=" * 60)
    print("Asana MCP - OAuth2 Authentication Test")
    print("=" * 60)
    print()
    
    try:
        # Get client instance
        client = get_client()
        
        # Check if already authenticated
        if client.is_authenticated():
            print("[OK] Already authenticated with cached token")
        else:
            print("No cached token found. Starting OAuth2 authentication...")
            if not client.authenticate_interactive():
                print("[FAILED] Authentication failed!")
                return
        
        # Test API call
        print("\nTesting API connection...")
        result = client.get_me()
        user = result.get("data", {})
        
        print()
        print("[OK] Successfully connected to Asana API!")
        print()
        print("User Profile:")
        print(f"  Name: {user.get('name', 'N/A')}")
        print(f"  Email: {user.get('email', 'N/A')}")
        print(f"  GID:   {user.get('gid', 'N/A')}")
        
        # Try to get workspaces
        workspaces = user.get("workspaces", [])
        if workspaces:
            print()
            print("Workspaces:")
            for ws in workspaces:
                print(f"  - {ws.get('name', 'N/A')} (GID: {ws.get('gid', 'N/A')})")
        
        print()
        print("=" * 60)
        print("Authentication test PASSED! You're ready to use the MCP server.")
        print("=" * 60)
        
    except ValueError as e:
        print(f"[ERROR] Configuration Error: {e}")
        print()
        print("Please set up your .env file with:")
        print("  ASANA_CLIENT_ID=your_client_id_here")
        print("  ASANA_CLIENT_SECRET=your_client_secret_here")
        print()
        print("Create an OAuth app at: https://app.asana.com/0/my-apps")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()

