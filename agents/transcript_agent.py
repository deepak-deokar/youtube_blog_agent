from youtube_transcript_api import YouTubeTranscriptApi

def extract_transcript(video_url: str) -> str:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        return f"[Error fetching transcript] {e}"