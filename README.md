# RocketScope

A tool for tracking player mentions across Rocket League YouTube videos. Searches through video transcripts to find when specific players are mentioned, with timestamps linking directly to YouTube.

## Features

- Index multiple YouTube channels for player mentions
- Search through video transcripts automatically  
- Track both professional players and personal friends
- Direct links to YouTube timestamps
- Caching system to avoid reprocessing videos
- Web interface for easy searching

## Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- YouTube Data API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/RocketScope.git
cd RocketScope
```

2. Install Python dependencies:
```bash
cd indexer
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

4. Get a YouTube API key:
   - Go to Google Cloud Console
   - Create a project and enable YouTube Data API v3
   - Create an API key

5. Set your API key:
```bash
export YOUTUBE_API_KEY="your_api_key_here"
```

## Usage

### Adding Friends to Track

Edit `indexer/friends_config.py` and add your friends' gamertags:

```python
MY_FRIENDS = [
    'YourFriendGamertag',
    'AnotherFriend',
    'NickName123',
]
```

### Running the Indexer

```bash
cd indexer
python3 index_channel.py
```

### Starting the Web Interface

```bash
cd frontend  
npm run dev
```

Open http://localhost:5173 to search for player mentions.

## Configuration

### Adding YouTube Channels

Edit the `CHANNELS` dictionary in `index_channel.py`:

```python
CHANNELS = {
    'Channel Name': 'CHANNEL_ID_HERE',
}
```

### Caching

The indexer caches processed videos to avoid reprocessing. Cache files are stored in `indexer/cache/`.

To clear cache and reprocess all videos:
```bash
rm -rf indexer/cache/
```

## Project Structure

```
RocketScope/
├── indexer/           # Python scripts for processing videos
│   ├── index_channel.py    # Main indexer
│   ├── players.py          # List of players to track
│   ├── friends_config.py   # Personal friends configuration
│   └── requirements.txt    # Python dependencies
└── frontend/          # React web interface
    ├── src/
    │   ├── App.jsx         # Main application
    │   └── index.css       # Styling
    └── package.json        # Node dependencies
```

## License

MIT License