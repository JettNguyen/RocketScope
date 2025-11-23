"""
List of Rocket League pro players, community figures, and friends to track.
Add names, common nicknames, and alternate spellings.
"""

# Pro players and notable figures
PRO_PLAYERS = [
    # NA Players
    'Firstkiller',
    'First',  # nickname
    'Squishy',
    'SquishyMuffinz',
    'Garrett',
    'GarrettG',
    'jstn',
    'Justin',
    'Arsenal',
    'Mist',
    'Daniel',
    'Beastmode',
    'Dreaz',
    'Comm',
    'Retals',
    'Torment',
    'Rapid',
    'Lionblaze',
    'Percy',
    'Roll Dizz',
    'Chrome',
    'Memory',
    'Allushin',
    'Majicbear',
    'Chronic',
    'Aqua',
    'Oath',
    'Gyro',
    'Fig',
    
    # EU Players
    'Zen',
    'Vatira',
    'Joyo',
    'Monkey Moon',
    'Kaydop',
    'Fairy Peak',
    'Alpha54',
    'Seikoo',
    'Aztral',
    'AppJack',
    'Archie',
    'Kash',
    'Joreuz',
    'Scrub Killa',
    'Scrub',
    'Exotiik',
    'Atow',
    'Rizex',
    'Noly',
    'RelatingWave',
    'Radosin',
    'Itachi',
    'Catalysm',
    'Crr',
    'rise',
    'Kassio',
    'Acronik',
    'arju',
    'Oaly',
    'Yukeo',
    
    # OCE Players
    'Bananahead',
    'Torsos',
    'CJCJ',
    'Drippay',
    'Fever',
    'Express',
    'Amphis',
    'Decka',
    'Le Duck',
    'Superlachie',
    
    # SAM Players
    'Yanxnz',
    'Lostt',
    'Caard',
    'AztromicK',
    'Reysbull',
    'Kv1',
    'Math',
    'Taco',
    'Drufinho',
    'nxghtt',
    
    # MENA Players
    'Ahmad',
    'oKhaliD',
    'trk511',
    'Senzo',
    'ams',
    'Twiz',
    'Kiileerrz',
    
    # APAC Players
    'Maru',
    'ReaLize',
    'Tenhow',
    'Burn',
    'LCT',
    
    # SSA Players
    'Snowyy',
    'SkillSteal',
    
    # Notable Figures / Content Creators / Coaches
    'Sizz',
    'Rizzo',
    'Leth',
    'Lethamyr',
    'SunlessKhan',
    'Sunless',
    'Musty',
    'Flakes',
    'Kronovi',
    'Turbopolsa',
    'Turbo',
    'Gibbs',
    'Jorby',
    'Achieves',
    'Wavepunk',
    'Lawler',
    'Stumpy',
    'Johnny',
    'JohnnyBoi',
    'Dazerin',
    'Turtle',
    'Corelli',
    'Gregan',
]

# 🎯 FRIENDS LIST - Import from separate config file for easy management
try:
    from friends_config import MY_FRIENDS
    FRIENDS = MY_FRIENDS
    print(f"✅ Loaded {len(FRIENDS)} friends from config")
except ImportError:
    # Fallback to example friends if config file doesn't exist
    FRIENDS = [
        'Larry',
        'Hammy Crackers',
        'Hammy',
        'Jett',
        # Add more friends here or create friends_config.py
    ]
    print(f"⚠️  Using example friends list. Create friends_config.py to customize!")

# Combine all players to track
ALL_PLAYERS = PRO_PLAYERS + FRIENDS