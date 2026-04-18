import os
import time
import csv
import random
import argparse
from typing import List, Set, Any, TypedDict
from datetime import datetime, timezone
from googleapiclient.discovery import build
from dotenv import load_dotenv

from utils.logger import info, error
from config import (
    VIDEO_IDS_FILE,
    YOUTUBE_RAW_DIR,
    MAX_RESULTS_PER_KEYWORD,
    MAX_COMMENTS_PER_VIDEO,
    YOUTUBE_KEYWORDS,
    YOUTUBE_FILTER_KEYWORDS
)

load_dotenv()


class Comment(TypedDict):
    video_id: str
    comment: str


def get_youtube_client() -> Any:
    return build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))


def load_video_ids() -> List[str]:
    if not os.path.exists(VIDEO_IDS_FILE):
        return []
    
    with open(VIDEO_IDS_FILE, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def save_new_ids(new_ids: List[str]) -> None:
    if not new_ids:
        return
    
    os.makedirs(os.path.dirname(VIDEO_IDS_FILE), exist_ok=True)
    
    with open(VIDEO_IDS_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"\n# [Auto-Search] {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}\n"
        )
        for video in new_ids:
            f.write(f"{video}\n")

def search_videos(
        youtube: Any,
        keywords: List[str],
        existing_ids: Set[str]
) -> List[str]:
    discorverd_ids: List[str] = []

    info("=== Searching for new video IDs ===")
    
    for i, kw in enumerate(keywords, 1):
        info(f"[{i}/{len(keywords)}] Searching: {kw}")
        
        try:
            res = youtube.search().list(
                part="snippet",
                q=kw,
                type="video",
                relevanceLanguage="en",
                maxResults=MAX_RESULTS_PER_KEYWORD
            ).execute()
            
            new_vids = [
                item["id"]["videoId"]
                for item in res.get("items", [])
                if item["id"].get("videoId")
                and item["id"]["videoId"] not in existing_ids
                and item["id"]["videoId"] not in discorverd_ids
                and not any(
                    fk in item["snippet"]["title"].lower()
                    for fk in YOUTUBE_FILTER_KEYWORDS
                )
            ]

            discorverd_ids.extend(new_vids)
            info(f"  → {len(new_vids)} new videos found for '{kw}'")
        except Exception as e:
            error(f"Search error: {e}")
        
        time.sleep(random.uniform(1.0, 1.5)) # To avoid hitting rate limits
        
    return discorverd_ids


def fetch_comments(youtube: Any, video_id: str) -> List[Comment]:
    comments: List[Comment] = []
    next_page_token = None

    while len(comments) < MAX_COMMENTS_PER_VIDEO:
        try:
            res = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            ).execute()
            
            batch = res.get("items", [])

            valid_batch = []
            for item in batch:
                text = item["snippet"]["topLevelComment"]["snippet"].get("textDisplay", "")
                if text:
                    valid_batch.append(text)
            
            remaining = MAX_COMMENTS_PER_VIDEO - len(comments)
        
            for text in valid_batch[:remaining]:
                comments.append({
                    "video_id": video_id,
                    "comment": text
                })
            
            if len(comments) >= MAX_COMMENTS_PER_VIDEO:
                break
                    
            next_page_token = res.get("nextPageToken")
            if not next_page_token:
                break

            time.sleep(0.2)

        except Exception as e:
            error(f"Fetch error: ({video_id}): {e}")
            break
    
    return comments


def save_to_csv(video_id: str, data: List[Comment]) -> None:
    if not data:
        info(f"{video_id}: no data")
        return
    
    os.makedirs(YOUTUBE_RAW_DIR, exist_ok=True)
    path = f"{YOUTUBE_RAW_DIR}/yt_{video_id}.csv"
    
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["video_id", "comment"])
        writer.writeheader()
        writer.writerows(data)

    info(f"{video_id}: {len(data)} comments saved")


def is_collected(video_id: str) -> bool:
    if not os.path.exists(YOUTUBE_RAW_DIR):
        return False
    
    return any(f.startswith(f"yt_{video_id}") for f in os.listdir(YOUTUBE_RAW_DIR))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YouTube comment collector")
    
    parser.add_argument(
        "--skip-search",
        action="store_true",
        help="Skip searching for new video IDs and use existing list"
    )
    
    parser.add_argument(
        "--search-only",
        action="store_true",
        help="Only search for new video IDs without collecting comments"
    )
    
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    youtube = get_youtube_client()
    
    existing_ids: Set[str] = set(load_video_ids())
    
    if not args.skip_search:
        new_ids = search_videos(youtube, YOUTUBE_KEYWORDS, existing_ids)
        save_new_ids(new_ids)
    else:
        info("Skipping video search step")
        
    if args.search_only:
        info("Search-only mode: skipping comment collection")
        return
        
    all_ids = load_video_ids()
    info(f"=== Collecting comments (Total videos: {len(all_ids)}) ===")
    
    for i, vid in enumerate(all_ids, 1):
        if is_collected(vid):
            continue
            
        info(f"[{i}/{len(all_ids)}] Processing: {vid}")
        
        comments = fetch_comments(youtube, vid)
        save_to_csv(vid, comments)
        
        time.sleep(0.5)
    
    info(f"Done. Data saved in {YOUTUBE_RAW_DIR}/")


if __name__ == "__main__":
    main()