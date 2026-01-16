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

def get_transcript(video_id):
    """Fetch transcript for a video ID"""
    try:
        # Instantiate the API and fetch transcript
        transcript_list = YouTubeTranscriptApi().fetch(video_id)
        
        # Combine all transcript segments into one text
        # Access 'text' attribute of FetchedTranscriptSnippet dataclass
        full_transcript = ' '.join([segment.text for segment in transcript_list])
        return full_transcript
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    # Read URLs from file
    try:
        with open('urls.txt', 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("ERROR: 'urls.txt' file not found!")
        print("Please create a file called 'urls.txt' with one YouTube URL per line.")
        sys.exit(1)
    
    if not urls:
        print("ERROR: 'urls.txt' is empty!")
        sys.exit(1)
    
    print(f"Found {len(urls)} URLs to process...")
    print("-" * 60)
    
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing: {url}")
        
        video_id = extract_video_id(url)
        
        if not video_id:
            print(f"  ❌ Invalid YouTube URL")
            results.append({
                'url': url,
                'video_id': None,
                'transcript': "ERROR: Invalid YouTube URL"
            })
            continue
        
        print(f"  Video ID: {video_id}")
        print(f"  Fetching transcript...")
        
        transcript = get_transcript(video_id)
        
        if transcript.startswith("ERROR:"):
            print(f"  ❌ {transcript}")
        else:
            print(f"  ✓ Transcript retrieved ({len(transcript)} characters)")
        
        results.append({
            'url': url,
            'video_id': video_id,
            'transcript': transcript
        })
    
    # Save results to file
    print("\n" + "=" * 60)
    print("Saving transcripts to 'transcripts.txt'...")
    
    with open('transcripts.txt', 'w', encoding='utf-8') as f:
        for i, result in enumerate(results, 1):
            f.write(f"{'=' * 60}\n")
            f.write(f"VIDEO {i}\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"URL: {result['url']}\n")
            f.write(f"Video ID: {result['video_id'] or 'N/A'}\n")
            f.write(f"\nTRANSCRIPT:\n")
            f.write(f"{result['transcript']}\n\n")
    
    print(f"✓ Done! Processed {len(results)} videos.")
    print(f"✓ Results saved to 'transcripts.txt'")
    
    # Print summary
    successful = sum(1 for r in results if not r['transcript'].startswith("ERROR:"))
    failed = len(results) - successful
    
    print("\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print("=" * 60)

if __name__ == "__main__":
    main()