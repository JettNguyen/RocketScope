#!/usr/bin/env python3
"""
YouTube Channel Indexer for Rocket League Player Mentions
Indexes YouTube channels to find mentions of specific players in video transcripts.
"""

import os
import json
import re
from pathlib import Path
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from players import ALL_PLAYERS

# Configuration
API_KEY = os.environ.get('YOUTUBE_API_KEY')
OUTPUT_PATH = Path(__file__).parent.parent / 'frontend' / 'public' / 'data' / 'mentions.json'

CHANNELS = {
    'Retals': 'UCRLM6B6rGXDSJawUH_mHHPw',  # Correct Retals channel ID
    # Add more channels here:
    # 'SquishyMuffinz': 'UCjsY2MoYLPRCyUlmFoI2Yqg',
}

def get_channel_videos(youtube, channel_id, max_results=500):
    """Fetch all video IDs from a channel."""
    videos = []
    next_page = None
    
    print(f"Searching for videos in channel: {channel_id}")
    
    while len(videos) < max_results:
        try:
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=min(50, max_results - len(videos)),
                order='date',
                type='video',
                pageToken=next_page
            )
            response = request.execute()
            
            print(f"Found {len(response.get('items', []))} videos in response")
            
            if 'items' not in response:
                print(f"Warning: No items in API response. Keys: {list(response.keys())}")
                break
                
            for item in response['items']:
                videos.append({
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'date': item['snippet']['publishedAt'][:10],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url']
                })
            
            next_page = response.get('nextPageToken')
            if not next_page:
                break
            
            print(f"  Fetched {len(videos)} videos...")
        except Exception as e:
            print(f"Error in search: {e}")
            break
    
    return videos

def get_transcript(video_id):
    """Get transcript with timestamps for a video."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        # Try to find an English transcript (manual or auto-generated)
        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        return transcript.fetch()
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"    Error getting transcript: {e}")
        return None

def find_mentions(transcript, players):
    """Find all player mentions in a transcript."""
    mentions = {}
    
    # Build regex patterns for each player (word boundaries)
    patterns = {p: re.compile(rf'\b{re.escape(p)}\b', re.IGNORECASE) for p in players}
    
    for entry in transcript:
        text = entry.text  # Use attribute instead of dictionary access
        for player, pattern in patterns.items():
            if pattern.search(text):
                if player not in mentions:
                    mentions[player] = []
                
                secs = int(entry.start)  # Use attribute instead of dictionary access
                mins, secs = divmod(secs, 60)
                hours, mins = divmod(mins, 60)
                
                if hours > 0:
                    timestamp = f"{hours}:{mins:02d}:{secs:02d}"
                else:
                    timestamp = f"{mins}:{secs:02d}"
                
                mentions[player].append({
                    'time': timestamp,
                    'seconds': int(entry.start),
                    'text': text
                })
    
    return mentions

def index_channel(youtube, name, channel_id):
    """Index all videos from a channel."""
    print(f"\nIndexing channel: {name}")
    
    videos = get_channel_videos(youtube, channel_id)
    print(f"  Found {len(videos)} videos")
    
    indexed = []
    for i, video in enumerate(videos):
        print(f"  [{i+1}/{len(videos)}] {video['title'][:50]}...")
        
        transcript = get_transcript(video['id'])
        if not transcript:
            print(f"    No transcript available")
            continue
        
        mentions = find_mentions(transcript, ALL_PLAYERS)
        if mentions:
            total = sum(len(m) for m in mentions.values())
            print(f"    Found {total} mentions of {len(mentions)} players")
            indexed.append({
                'videoId': video['id'],
                'title': video['title'],
                'date': video['date'],
                'thumbnail': video['thumbnail'],
                'channel': name,
                'mentions': mentions
            })
        else:
            print(f"    No player mentions found")
    
    return indexed

def main():
    if not API_KEY:
        print("Error: Set YOUTUBE_API_KEY environment variable")
        print("   export YOUTUBE_API_KEY='your_key_here'")
        return
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    all_data = {
        'lastUpdated': None,
        'channels': list(CHANNELS.keys()),
        'players': ALL_PLAYERS,
        'videos': []
    }
    
    for name, channel_id in CHANNELS.items():
        videos = index_channel(youtube, name, channel_id)
        all_data['videos'].extend(videos)
    
    # Sort by date (newest first)
    all_data['videos'].sort(key=lambda x: x['date'], reverse=True)
    
    # Add timestamp
    from datetime import datetime
    all_data['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
    
    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone! Indexed {len(all_data['videos'])} videos")
    print(f"Output: {OUTPUT_PATH}")
    
    # Stats
    all_players = set()
    total_mentions = 0
    for video in all_data['videos']:
        for player, mentions in video['mentions'].items():
            all_players.add(player)
            total_mentions += len(mentions)
    
    print(f"Players mentioned: {len(all_players)}")
    print(f"Total mentions: {total_mentions}")

if __name__ == '__main__':
    main()