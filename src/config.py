from typing import List

# === Directory 구조 ===
DATA_DIR: str = "data"

RAW_DIR: str = f"{DATA_DIR}/raw"
PROCESSED_DIR: str = f"{DATA_DIR}/processed"

YOUTUBE_RAW_DIR: str = f"{RAW_DIR}/youtube"

RESULTS_DIR: str = "results"

# === 주요 파일 === 
VIDEO_IDS_FILE: str = f"{DATA_DIR}/video_list.txt"

# === YouTube 수집 설정 ===
MAX_RESULTS_PER_KEYWORD: int = 100
MAX_COMMENTS_PER_VIDEO: int = 1000

# YouTube Search Keywords
YOUTUBE_KEYWORDS: List[str] = [ 
    "AI music reaction",
    "AI generated music opinion",
    "AI music is scary",
    "AI music is amazing",
    "AI music is bad",
    "AI music is ruined music industry",
    "AI vs human music",
    "AI music vs real music",
    "can AI replace musicians",
    "AI music vs artists debate",
    "AI song controversy",
    "AI music copyright issues",
    "AI music ethical concerns"
]

YOUTUBE_FILTER_KEYWORDS: List[str] = [
    "tutorial", "how to", "how-to", "guide",
    "course", "lesson", "learn", "make", "creating",
    "generate", "generator tutorial", "lofi", "beats",
    "chill", "study", "sleep", "background music",
    "playlist", "mix", "1 hour", "10 hours", "loop",
    "official", "mv", "music video", "lyrics", "promo",
    "teaser", "trailer", "out now", "stream now", "ai song",
    "ai generated song", "made by ai", "full song", "cover", "remix"
]