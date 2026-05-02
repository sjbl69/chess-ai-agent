from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def search_youtube_videos(opening: str, max_results: int = 3):
    if not YOUTUBE_API_KEY:
        print("Clé API manquante")
        return []

    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

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
            video_id = item["id"]["videoId"]

            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        return videos

    except Exception as e:
        print("Erreur YouTube:", e)
        return []