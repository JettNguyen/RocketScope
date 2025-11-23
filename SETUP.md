# RocketScope - YouTube API Setup Guide

## Getting Your YouTube API Key

To fetch real data from YouTube channels, you'll need a YouTube Data API key from Google Cloud Console.

### Step 1: Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Click "Create Project" if you don't have one
   - Project name: `RocketScope` (or any name you prefer)
   - Click "Create"

### Step 2: Enable YouTube Data API
1. In your project, go to "APIs & Services" > "Library"
2. Search for "YouTube Data API v3"
3. Click on it and click "Enable"

### Step 3: Create API Key
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy the generated API key
4. (Optional) Click "Restrict Key" to secure it:
   - Under "API restrictions", select "Restrict key"
   - Choose "YouTube Data API v3"
   - Save

### Step 4: Set Environment Variable
Set your API key as an environment variable:

```bash
# For current session:
export YOUTUBE_API_KEY="your_api_key_here"

# To make it permanent, add to your shell profile:
echo 'export YOUTUBE_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 5: Run the Indexer
```bash
cd indexer
python3 index_channel.py
```

## Adding More Channels

Edit `CHANNELS` in `index_channel.py`:

```python
CHANNELS = {
    'Retals': 'UCuRS9KcqyRsRZSR2GLuwxAw',
    'SquishyMuffinz': 'UCjsY2MoYLPRCyUlmFoI2Yqg',
    'SunlessKhan': 'UCd534c_ehOvrLVL2v7Nl61w',
    # Add more channels...
}
```

To find a channel ID:
1. Go to the channel's YouTube page
2. View page source (Ctrl+U)
3. Search for "channelId" or "externalId"

## Running the Full App

1. **Generate/Update Data:**
   ```bash
   cd indexer
   python3 index_channel.py  # With real API key
   # OR
   python3 demo_data_generator.py  # For testing
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser:**
   Visit http://localhost:5173/

## Troubleshooting

### "Found 0 videos"
- Check that `YOUTUBE_API_KEY` is set correctly
- Verify the channel ID is correct
- Ensure the channel has public videos

### Import/Module Errors
- Make sure you're using the right Python version
- Install requirements: `pip3 install -r requirements.txt`

### API Quota Exceeded
- YouTube API has daily quotas (free tier: 10,000 units/day)
- Each video search/transcript costs quota units
- Consider limiting `max_results` in `get_channel_videos()`