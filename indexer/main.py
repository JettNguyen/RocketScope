#!/usr/bin/env python3
"""
YouTube Channel Indexer with Caching
Processes YouTube channels to find player mentions in video transcripts.
"""

import os
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from players import ALL_PLAYERS, PRO_PLAYERS, FRIENDS

# Configuration
API_KEY = os.environ.get('YOUTUBE_API_KEY')
OUTPUT_PATH = Path(__file__).parent.parent / 'frontend' / 'public' / 'data' / 'mentions.json'
CACHE_PATH = Path(__file__).parent / 'cache' / 'video_cache.json'

CHANNELS = {
    'Retals': 'UCRLM6B6rGXDSJawUH_mHHPw',
}

def load_cache():
    """Load video processing cache."""
    try:
        if CACHE_PATH.exists():
            with open(CACHE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Cache load error: {e}")
    
    return {
        'processed_videos': {},
        'last_check': {},
        'stats': {'total_processed': 0, 'cache_hits': 0, 'new_videos': 0}
    }

def save_cache(cache_data):
    """Save video processing cache."""
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_PATH, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Cache save error: {e}")

def get_video_hash(video):
    """Generate hash for video to detect changes."""
    content = f"{video['title']}-{video['date']}"
    return hashlib.md5(content.encode()).hexdigest()

def get_channel_videos(youtube, channel_id, max_results=500, days_back=30):
    """Fetch videos from channel."""
    videos = []
    next_page = None
    
    date_filter = None
    if days_back:
        date_filter = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%dT00:00:00Z')
    
    print(f"Searching for videos in channel: {channel_id}")
    if date_filter:
        print(f"Looking for videos after: {date_filter[:10]}")
    
    while len(videos) < max_results:
        try:
            request_params = {
                'part': 'snippet',
                'channelId': channel_id,
                'maxResults': min(50, max_results - len(videos)),
                'order': 'date',
                'type': 'video',
                'pageToken': next_page
            }
            
            if date_filter:
                request_params['publishedAfter'] = date_filter
            
            request = youtube.search().list(**request_params)
            response = request.execute()
            
            print(f"Found {len(response.get('items', []))} videos in response")
            
            if 'items' not in response:
                print(f"Warning: No items in response. Keys: {list(response.keys())}")
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
            
            print(f"Fetched {len(videos)} videos...")
        except Exception as e:
            print(f"Error in search: {e}")
            break
    
    return videos

def get_transcript(video_id):
    """Get transcript with timestamps for a video."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        return transcript.fetch()
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        if "IP" in str(e) and "blocked" in str(e):
            print("Rate limited - skipping video")
        else:
            print(f"Error getting transcript: {e}")
        return None

def find_mentions(transcript, players):
    """Find all player mentions in a transcript."""
    mentions = {}
    
    patterns = {p: re.compile(rf'\\b{re.escape(p)}\\b', re.IGNORECASE) for p in players}
    
    for entry in transcript:
        text = entry.text
        for player, pattern in patterns.items():
            if pattern.search(text):
                if player not in mentions:
                    mentions[player] = []
                
                secs = int(entry.start)
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

def index_channel_with_cache(youtube, name, channel_id, cache):
    """Index channel videos using cache."""
    print(f"\\nIndexing channel: {name}")
    
    videos = get_channel_videos(youtube, channel_id)
    print(f"Found {len(videos)} videos")
    
    indexed = []
    new_count = 0
    cache_hits = 0
    
    for i, video in enumerate(videos):
        print(f"[{i+1}/{len(videos)}] {video['title'][:50]}...")
        
        video_hash = get_video_hash(video)
        video_id = video['id']
        
        # Check cache
        if (video_id in cache['processed_videos'] and 
            cache['processed_videos'][video_id]['hash'] == video_hash):
            
            cached_mentions = cache['processed_videos'][video_id]['mentions']
            if cached_mentions:
                cache_hits += 1
                total = sum(len(m) for m in cached_mentions.values())
                print(f"    Cached: {total} mentions of {len(cached_mentions)} players")
                indexed.append({
                    'videoId': video['id'],
                    'title': video['title'],
                    'date': video['date'],
                    'thumbnail': video['thumbnail'],
                    'channel': name,
                    'mentions': cached_mentions
                })
            else:
                print("    Cached: No mentions")
            continue
        
        # Process new video
        new_count += 1
        transcript = get_transcript(video['id'])
        if not transcript:
            print("    No transcript available")
            cache['processed_videos'][video_id] = {
                'hash': video_hash,
                'mentions': {},
                'processed_date': datetime.utcnow().isoformat()
            }
            continue
        
        mentions = find_mentions(transcript, ALL_PLAYERS)
        
        # Cache the result
        cache['processed_videos'][video_id] = {
            'hash': video_hash,
            'mentions': mentions,
            'processed_date': datetime.utcnow().isoformat()
        }
        
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
            print("    No player mentions found")
    
    print(f"Cache hits: {cache_hits}, New videos: {new_count}")
    cache['stats']['cache_hits'] += cache_hits
    cache['stats']['new_videos'] += new_count
    
    return indexed

def main():
    if not API_KEY:
        print("Error: Set YOUTUBE_API_KEY environment variable")
        print("   export YOUTUBE_API_KEY='your_key_here'")
        return
    
    print("Starting indexer with caching")
    
    cache = load_cache()
    print(f"Cache loaded: {len(cache['processed_videos'])} videos cached")
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    all_data = {
        'lastUpdated': None,
        'channels': list(CHANNELS.keys()),
        'players': ALL_PLAYERS,
        'videos': [],
        'stats': {
            'pro_players': len(PRO_PLAYERS),
            'friends': len(FRIENDS),
            'total_tracked': len(ALL_PLAYERS)
        }
    }
    
    for name, channel_id in CHANNELS.items():
        videos = index_channel_with_cache(youtube, name, channel_id, cache)
        all_data['videos'].extend(videos)
    
    all_data['videos'].sort(key=lambda x: x['date'], reverse=True)
    all_data['lastUpdated'] = datetime.utcnow().isoformat() + 'Z'
    
    cache['stats']['total_processed'] = len(cache['processed_videos'])
    cache['last_check'][str(CHANNELS)] = datetime.utcnow().isoformat()
    
    save_cache(cache)
    
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"\\nDone! Indexed {len(all_data['videos'])} videos")
    print(f"Output: {OUTPUT_PATH}")
    
    friend_mentions = set()
    pro_mentions = set()
    total_mentions = 0
    
    for video in all_data['videos']:
        for player, mentions in video['mentions'].items():
            total_mentions += len(mentions)
            if player in FRIENDS:
                friend_mentions.add(player)
            else:
                pro_mentions.add(player)
    
    print(f"Pro players mentioned: {len(pro_mentions)}")
    print(f"Friends mentioned: {len(friend_mentions)}")
    print(f"Total mentions: {total_mentions}")

if __name__ == '__main__':
    main()