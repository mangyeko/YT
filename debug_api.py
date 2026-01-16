from youtube_transcript_api import YouTubeTranscriptApi
print("Dir of YouTubeTranscriptApi:", dir(YouTubeTranscriptApi))
try:
    print("get_transcript:", YouTubeTranscriptApi.get_transcript)
except AttributeError as e:
    print("Error:", e)
