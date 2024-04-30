import pytube
from youtube_transcript_api import YouTubeTranscriptApi

# Replace with the YouTube video URL
# video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_url = "https://www.youtube.com/watch?v=6Py-tIEiXKw&list=PLaMu-SDt_RB4Ly0xb0qsQVpLwRQcjtOb-"

# Create a YouTube object
yt = pytube.YouTube(video_url)

# Get the video's captions
captions = yt.captions.get_by_language_code("en")

# Use youtube-transcript-api to extract the transcript
transcript_api = YouTubeTranscriptApi()
transcript = transcript_api.get_transcript(yt.video_id, languages=["en"])

# Print the transcript
for line in transcript:
    print(line)
