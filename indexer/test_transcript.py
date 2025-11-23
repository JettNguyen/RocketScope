#!/usr/bin/env python3
"""
Test YouTube transcript API usage
"""

def test_transcript_api():
    try:
        # Try the static method approach first
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # Test video: a popular RL video that likely has transcripts
        test_video_id = "dQw4w9WgXcQ"  # Rick Roll (always has transcripts)
        
        print("🧪 Testing transcript API...")
        print(f"📹 Test video: {test_video_id}")
        
        # Check what methods are available
        print(f"📊 Available methods: {[m for m in dir(YouTubeTranscriptApi) if not m.startswith('_')]}")
        
        # Try different approaches
        approaches = [
            # Static method approach (common in newer versions)
            lambda vid: YouTubeTranscriptApi.get_transcript(vid, languages=['en']),
            # Alternative approach
            lambda vid: YouTubeTranscriptApi.list_transcripts(vid).find_transcript(['en']).fetch(),
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"\n🧪 Approach {i}:")
                result = approach(test_video_id)
                print(f"✅ Success! Got {len(result)} transcript entries")
                print(f"📝 Sample: {result[0] if result else 'Empty'}")
                return approach, True
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        return None, False
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return None, False

if __name__ == '__main__':
    test_transcript_api()