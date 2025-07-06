#!/usr/bin/env python3
"""
Simple command-line tool to check your portfolio website
Usage: python check_website.py [command]
Commands: check, open, test, status
"""

import sys
import subprocess
from tests.test_local import check_website, open_website, quick_check

def main():
    if len(sys.argv) < 2:
        print("🌐 Portfolio Website Checker")
        print("=" * 30)
        print("Commands:")
        print("  check    - Full website check + open browser")
        print("  open     - Just open website in browser")
        print("  test     - Quick test without opening browser")
        print("  status   - Check if server is running")
        print("  start    - Start the Flask server")
        print("\nExample: python check_website.py check")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        print("🔍 Running full website check...")
        check_website()
        
    elif command == "open":
        open_website()
        
    elif command == "test":
        print("🧪 Running quick test...")
        quick_check()
        
    elif command == "status":
        print("📊 Checking server status...")
        if quick_check():
            print("✅ Server is running and website is accessible!")
        else:
            print("❌ Server is not running or has issues")
            
    elif command == "start":
        print("🚀 Starting Flask server...")
        try:
            subprocess.run([sys.executable, "server.py"], check=True)
        except KeyboardInterrupt:
            print("\n⏹️ Server stopped by user")
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: check, open, test, status, start")

if __name__ == "__main__":
    main() 