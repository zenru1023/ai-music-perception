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
    # TODO: 키워드 추가
]