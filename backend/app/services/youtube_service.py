from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def search_youtube_videos(opening: str, max_results: int = 3):
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY manquante dans le fichier .env")

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        # Requête optimisée
        query = f"{opening} chess opening tutorial"

        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results
        )

        response = request.execute()

        videos = []

        for item in response.get("items", []):
            video_id = item["id"].get("videoId")

            if not video_id:
                continue

            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "embed_url": f"https://www.youtube.com/embed/{video_id}",
                "channel": item["snippet"]["channelTitle"]
            })

        return videos

    except Exception as e:
        print("YouTube API error:", e)
        return []