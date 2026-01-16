# YouTube Shorts Bulk Transcript Generator

A simple Python utility to extract transcripts from YouTube Shorts (and regular YouTube videos) in bulk.

## Features
- Extracts video IDs from various YouTube URL formats.
- Fetches transcripts using the `youtube-transcript-api`.
- Supports bulk processing from a text file.
- Saves results into a clean, readable text file.

## Setup

1. **Clone the repository** (or download the files).
2. **Setup a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a file named `urls.txt` and add one YouTube URL per line.
2. Run the generator:
   ```bash
   python youtube_transcript_generator.py
   ```
3. Check `transcripts.txt` for the output.

## Project Structure
- `youtube_transcript_generator.py`: The main script.
- `urls.txt`: Input file for URLs.
- `transcripts.txt`: Output file for transcripts.
- `requirements.txt`: Python dependencies.
