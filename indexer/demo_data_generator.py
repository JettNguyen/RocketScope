#!/usr/bin/env python3
"""
Demo data generator for RocketScope
Generates sample data to test the app without needing YouTube API
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from players import PRO_PLAYERS

OUTPUT_PATH = Path(__file__).parent.parent / 'frontend' / 'public' / 'data' / 'mentions.json'

def generate_sample_data():
    """Generate sample mention data for testing"""
    
    # Sample video data with realistic mentions
    sample_videos = [
        {
            'videoId': 'dQw4w9WgXcQ',
            'title': 'Retals Reviews the BEST Rocket League Plays of 2024',
            'date': '2024-11-20',
            'thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
            'channel': 'Retals',
            'mentions': {
                'Firstkiller': [
                    {'time': '2:15', 'seconds': 135, 'text': 'Firstkiller with an insane double tap!'},
                    {'time': '8:42', 'seconds': 522, 'text': 'You can see how Firstkiller positions himself here'}
                ],
                'Zen': [
                    {'time': '5:30', 'seconds': 330, 'text': 'Zen is absolutely cracked at mechanics'},
                    {'time': '12:05', 'seconds': 725, 'text': 'This is why Zen is considered the best'}
                ]
            }
        },
        {
            'videoId': 'jNQXAC9IVRw',
            'title': 'Ranking Every Pro Player in RLCS 2024',
            'date': '2024-11-18',
            'thumbnail': 'https://img.youtube.com/vi/jNQXAC9IVRw/mqdefault.jpg',
            'channel': 'Retals',
            'mentions': {
                'Vatira': [
                    {'time': '1:45', 'seconds': 105, 'text': 'Vatira has to be S tier, no question'},
                    {'time': '15:20', 'seconds': 920, 'text': 'When Vatira is on form, nobody can stop him'}
                ],
                'Squishy': [
                    {'time': '3:10', 'seconds': 190, 'text': 'Squishy is still incredibly consistent'},
                    {'time': '7:55', 'seconds': 475, 'text': 'You have to respect Squishy\'s game sense'}
                ],
                'jstn': [
                    {'time': '11:30', 'seconds': 690, 'text': 'jstn with the mechanical prowess'}
                ]
            }
        },
        {
            'videoId': 'M7lc1UVf-VE',
            'title': 'React to RLCS World Championship Finals',
            'date': '2024-11-15',
            'thumbnail': 'https://img.youtube.com/vi/M7lc1UVf-VE/mqdefault.jpg',
            'channel': 'Retals',
            'mentions': {
                'Firstkiller': [
                    {'time': '0:45', 'seconds': 45, 'text': 'Firstkiller starting off strong in game one'},
                    {'time': '25:12', 'seconds': 1512, 'text': 'Firstkiller clutches up when it matters most'}
                ],
                'Arsenal': [
                    {'time': '18:30', 'seconds': 1110, 'text': 'Arsenal with the perfect setup play'},
                    {'time': '22:45', 'seconds': 1365, 'text': 'Arsenal reading the play perfectly'}
                ],
                'Daniel': [
                    {'time': '14:20', 'seconds': 860, 'text': 'Daniel going for the risky play'}
                ]
            }
        },
        {
            'videoId': 'y6120QOlsfU',
            'title': 'Why These Rocket League Players are UNDERRATED',
            'date': '2024-11-12',
            'thumbnail': 'https://img.youtube.com/vi/y6120QOlsfU/mqdefault.jpg',
            'channel': 'Retals',
            'mentions': {
                'Comm': [
                    {'time': '4:25', 'seconds': 265, 'text': 'Comm is so underrated in my opinion'},
                    {'time': '16:40', 'seconds': 1000, 'text': 'Comm has improved so much this season'}
                ],
                'Beastmode': [
                    {'time': '9:15', 'seconds': 555, 'text': 'Beastmode deserves more recognition'},
                    {'time': '20:30', 'seconds': 1230, 'text': 'Beastmode with the solid defensive play'}
                ],
                'Retals': [
                    {'time': '13:50', 'seconds': 830, 'text': 'I think Retals is pretty good too, obviously'}
                ]
            }
        }
    ]
    
    # Create the data structure
    data = {
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'channels': ['Retals'],
        'players': PRO_PLAYERS[:10],  # Include first 10 players
        'videos': sample_videos
    }
    
    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the sample data
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated sample data!")
    print(f"📁 Output: {OUTPUT_PATH}")
    print(f"📺 Videos: {len(sample_videos)}")
    
    # Calculate stats
    total_mentions = sum(len(mentions) for video in sample_videos for mentions in video['mentions'].values())
    unique_players = set()
    for video in sample_videos:
        unique_players.update(video['mentions'].keys())
    
    print(f"👥 Players mentioned: {len(unique_players)}")
    print(f"💬 Total mentions: {total_mentions}")
    
if __name__ == '__main__':
    generate_sample_data()