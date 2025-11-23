#!/usr/bin/env python3
"""
YouTube API Key Setup Helper
"""

def show_api_setup_guide():
    print("🚀 YouTube Data API Setup Guide")
    print("=" * 50)
    
    print("\n📋 Step 1: Go to Google Cloud Console")
    print("   https://console.cloud.google.com/")
    
    print("\n📋 Step 2: Create/Select Project")
    print("   • Click 'Select a project' dropdown")
    print("   • Click 'NEW PROJECT'")
    print("   • Name: RocketScope (or any name)")
    print("   • Click 'CREATE'")
    
    print("\n📋 Step 3: Enable YouTube Data API")
    print("   • Go to 'APIs & Services' > 'Library'")
    print("   • Search for 'YouTube Data API v3'")
    print("   • Click on it and click 'ENABLE'")
    
    print("\n📋 Step 4: Create API Key")
    print("   • Go to 'APIs & Services' > 'Credentials'")
    print("   • Click '+ CREATE CREDENTIALS'")
    print("   • Select 'API key'")
    print("   • Copy the generated key")
    
    print("\n🔑 Valid API Key Format:")
    print("   • Should be ~39 characters long")
    print("   • Should start with 'AIza'")
    print("   • Example: AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567")
    
    print("\n❌ What you might have entered:")
    print("   • Channel ID (starts with UC...): UCuRS9KcqyRsRZSR2GLuwxAw")
    print("   • Video ID (11 chars): dQw4w9WgXcQ")
    print("   • These are NOT API keys!")
    
    print("\n💡 After getting your API key:")
    print("   export YOUTUBE_API_KEY='AIzaSy...'")
    print("   python3 test_api.py")
    
    print("\n🆓 Free Tier Limits:")
    print("   • 10,000 quota units per day")
    print("   • ~100-200 videos can be indexed daily")
    
if __name__ == '__main__':
    show_api_setup_guide()