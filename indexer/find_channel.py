#!/usr/bin/env python3
"""
Find correct channel ID for Retals
"""

import os
from googleapiclient.discovery import build

def find_retals_channel():
    api_key = os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Search for Retals channel
    print("🔍 Searching for 'Retals' channels...")
    
    try:
        search_request = youtube.search().list(
            part='snippet',
            q='Retals Rocket League',
            type='channel',
            maxResults=10
        )
        response = search_request.execute()
        
        print(f"📊 Found {len(response.get('items', []))} channels:")
        
        for i, item in enumerate(response.get('items', []), 1):
            snippet = item['snippet']
            channel_id = snippet['channelId'] if 'channelId' in snippet else item['id']['channelId']
            print(f"\n{i}. {snippet['title']}")
            print(f"   ID: {channel_id}")
            print(f"   Description: {snippet['description'][:100]}...")
            
            # Test this channel for videos
            print(f"   🧪 Testing for videos...")
            video_search = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=5,
                type='video'
            )
            video_response = video_search.execute()
            video_count = len(video_response.get('items', []))
            print(f"   📹 Recent videos: {video_count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    find_retals_channel()