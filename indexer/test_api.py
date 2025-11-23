#!/usr/bin/env python3
"""
Debug script to test YouTube API connection
"""

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def test_api_key():
    api_key = os.environ.get('YOUTUBE_API_KEY')
    
    print(f"🔑 API Key found: {'YES' if api_key else 'NO'}")
    if api_key:
        print(f"🔑 API Key length: {len(api_key)}")
        print(f"🔑 API Key starts with: {api_key[:10]}...")
    else:
        print("❌ No API key found in environment variables")
        print("💡 Set it with: export YOUTUBE_API_KEY='your_key_here'")
        return False
    
    # Test the API key by making a simple request
    try:
        print("\n🧪 Testing API key...")
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Test with Retals channel ID
        channel_id = 'UCuRS9KcqyRsRZSR2GLuwxAw'
        print(f"🧪 Testing channel ID: {channel_id}")
        
        # Simple request to get channel info
        request = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()
        
        if 'items' in response and response['items']:
            channel = response['items'][0]
            print(f"✅ API key works! Channel: {channel['snippet']['title']}")
            print(f"📊 Subscriber count: {channel['statistics']['subscriberCount']}")
            print(f"📺 Video count: {channel['statistics']['videoCount']}")
            
            # Now test video search
            print(f"\n🔍 Testing video search...")
            search_request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=5,
                order='date',
                type='video'
            )
            search_response = search_request.execute()
            
            print(f"📹 Found {len(search_response['items'])} recent videos:")
            for i, item in enumerate(search_response['items'], 1):
                print(f"  {i}. {item['snippet']['title'][:60]}...")
            
            return True
        else:
            print("❌ Channel not found - check channel ID")
            return False
            
    except HttpError as e:
        print(f"❌ API Error: {e}")
        if e.resp.status == 403:
            print("💡 This might be an API key permissions issue")
            print("   Make sure YouTube Data API v3 is enabled in Google Cloud Console")
        elif e.resp.status == 400:
            print("💡 Invalid API key format")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    test_api_key()