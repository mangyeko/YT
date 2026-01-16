"""
YouTube Shorts Bulk Transcript Generator
Save this as: youtube_transcript_generator.py

Install required library first:
pip install youtube-transcript-api

Usage:
1. Create a file called 'urls.txt' with one YouTube URL per line
2. Run: python youtube_transcript_generator.py
3. Transcripts will be saved to 'transcripts.txt'
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re
import sys
from datetime import timedelta

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_raw_transcript(video_id):
    """Fetch raw transcript segments for a video ID"""
    try:
        return YouTubeTranscriptApi().fetch(video_id)
    except Exception as e:
        return f"ERROR: {str(e)}"

def format_time(seconds):
    """Format seconds into HH:MM:SS,mmm or HH:MM:SS.mmm"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return hours, minutes, secs, millis

def format_srt(transcript_list):
    """Convert transcript list to SRT format"""
    srt_output = []
    for i, segment in enumerate(transcript_list, 1):
        # Handle both dictionary and object access
        start = segment['start'] if isinstance(segment, dict) else segment.start
        duration = segment['duration'] if isinstance(segment, dict) else segment.duration
        text = segment['text'] if isinstance(segment, dict) else segment.text
        
        start_h, start_m, start_s, start_ms = format_time(start)
        end_h, end_m, end_s, end_ms = format_time(start + duration)
        
        srt_output.append(f"{i}")
        srt_output.append(f"{start_h:02}:{start_m:02}:{start_s:02},{start_ms:03} --> {end_h:02}:{end_m:02}:{end_s:02},{end_ms:03}")
        srt_output.append(text)
        srt_output.append("")
    return "\n".join(srt_output)

def format_vtt(transcript_list):
    """Convert transcript list to VTT format"""
    vtt_output = ["WEBVTT", ""]
    for segment in transcript_list:
        # Handle both dictionary and object access
        start = segment['start'] if isinstance(segment, dict) else segment.start
        duration = segment['duration'] if isinstance(segment, dict) else segment.duration
        text = segment['text'] if isinstance(segment, dict) else segment.text
        
        start_h, start_m, start_s, start_ms = format_time(start)
        end_h, end_m, end_s, end_ms = format_time(start + duration)
        
        vtt_output.append(f"{start_h:02}:{start_m:02}:{start_s:02}.{start_ms:03} --> {end_h:02}:{end_m:02}:{end_s:02}.{end_ms:03}")
        vtt_output.append(text)
        vtt_output.append("")
    return "\n".join(vtt_output)

def format_txt(transcript_list):
    """Convert transcript list to plain text"""
    # Handle both dictionary and object access
    return ' '.join([s['text'] if isinstance(s, dict) else s.text for s in transcript_list])

def get_transcript(video_id, format_type='txt'):
    """Fetch and format transcript"""
    raw_transcript = fetch_raw_transcript(video_id)
    if isinstance(raw_transcript, str) and raw_transcript.startswith("ERROR:"):
        return raw_transcript
    
    if format_type == 'srt':
        return format_srt(raw_transcript)
    elif format_type == 'vtt':
        return format_vtt(raw_transcript)
    else:
        return format_txt(raw_transcript)

def process_urls(urls, format_type='txt'):
    """Process a list of URLs and return results"""
    results = []
    for i, url in enumerate(urls, 1):
        video_id = extract_video_id(url)
        if not video_id:
            results.append({'url': url, 'video_id': None, 'transcript': "ERROR: Invalid YouTube URL"})
            continue
        
        transcript = get_transcript(video_id, format_type)
        results.append({'url': url, 'video_id': video_id, 'transcript': transcript})
    return results

def main():
    # CLI Usage
    try:
        with open('urls.txt', 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("ERROR: 'urls.txt' file not found!")
        sys.exit(1)
    
    if not urls:
        print("ERROR: 'urls.txt' is empty!")
        sys.exit(1)
    
    print(f"Found {len(urls)} URLs to process...")
    results = process_urls(urls)
    
    with open('transcripts.txt', 'w', encoding='utf-8') as f:
        for i, result in enumerate(results, 1):
            f.write(f"{'=' * 60}\nVIDEO {i}\n{'=' * 60}\nURL: {result['url']}\nTranscript:\n{result['transcript']}\n\n")
    
    print(f"✓ Done! Results saved to 'transcripts.txt'")

if __name__ == "__main__":
    main()