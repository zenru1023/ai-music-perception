import os
import csv
import json
from typing import TypedDict
from datetime import datetime, timezone

from config import VIDEO_IDS_FILE, YOUTUBE_RAW_DIR, RESULTS_DIR


class VideoStatus(TypedDict):
    video_id: str
    collected: bool
    comment_count: int


class CollectionStatus(TypedDict):
    generated_at: str
    total_videos: int
    collected: int
    not_collected: int
    total_comments: int
    videos: list[VideoStatus]


def load_video_ids() -> list[str]:
    if not os.path.exists(VIDEO_IDS_FILE):
        return []

    with open(VIDEO_IDS_FILE, encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


def count_comments(video_id: str) -> int:
    path = f"{YOUTUBE_RAW_DIR}/yt_{video_id}.csv"
    if not os.path.exists(path):
        return 0

    with open(path, encoding="utf-8-sig") as f:
        return sum(1 for row in csv.DictReader(f))


def build_status() -> CollectionStatus:
    video_ids = load_video_ids()

    videos: list[VideoStatus] = []
    for video_id in video_ids:
        comment_count = count_comments(video_id)
        videos.append({
            "video_id": video_id,
            "collected": comment_count > 0,
            "comment_count": comment_count
        })

    collected = sum(1 for v in videos if v["collected"])

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_videos": len(videos),
        "collected": collected,
        "not_collected": len(videos) - collected,
        "total_comments": sum(v["comment_count"] for v in videos),
        "videos": videos
    }


def main() -> None:
    status = build_status()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = f"{RESULTS_DIR}/collection_status.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

    print(f"Generated: {output_path}")
    print(f"  Total   : {status['total_videos']} videos")
    print(f"  Collected   : {status['collected']}")
    print(f"  Not collected: {status['not_collected']}")
    print(f"  Total comments: {status['total_comments']}")


if __name__ == "__main__":
    main()