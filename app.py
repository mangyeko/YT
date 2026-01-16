import streamlit as st
import youtube_transcript_generator as yt
import base64

# Page configurations
st.set_page_config(
    page_title="CaptionGrab - Download YouTube Shorts Captions",
    page_icon="⚡",
    layout="centered"
)

# Custom CSS for "CaptionGrab" aesthetic
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #E5D4B8;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 0, 0, 0.02) 1px, transparent 1px),
            radial-gradient(circle at 80% 80%, rgba(0, 0, 0, 0.02) 1px, transparent 1px);
        background-size: 4px 4px, 6px 6px;
    }
    
    /* Navigation Simulation */
    .nav-container {
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        margin: -4rem -4rem 2rem -4rem;
    }
    .logo {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d2d2d;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        margin-bottom: 3rem;
    }
    h1 {
        font-size: 2.5rem !important;
        color: #2d2d2d !important;
        font-weight: 700 !important;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #6d6d6d;
        line-height: 1.6;
    }
    
    /* Input Card */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 1rem 1.5rem !important;
        background: #fafafa !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #c99b5a !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background-color: #b88a49 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(201, 155, 90, 0.3) !important;
    }
    
    /* Features */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        height: 100%;
    }
    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    /* Footer Note */
    .note {
        text-align: center;
        font-size: 0.9rem;
        color: #7d7d7d;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
    <div class="nav-container">
        <div class="logo">CaptionGrab</div>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-container">
        <h1>Download YouTube Shorts Captions</h1>
        <p class="subtitle">Extract captions and subtitles from any YouTube Shorts video instantly. Free, fast, and simple.</p>
    </div>
""", unsafe_allow_html=True)

# Main Card
with st.container():
    col1, col2 = st.columns([4, 1])
    
    with col1:
        url_input = st.text_input("YouTube URL", placeholder="Paste YouTube Shorts URL here...", label_visibility="collapsed")
    
    with col2:
        download_clicked = st.button("Get Captions")

    # Format selection in Streamlit style but consistent with design
    format_type = st.radio(
        "Select Format",
        options=["SRT", "TXT", "VTT"],
        horizontal=True,
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown('<p class="note">Supports all YouTube Shorts videos with available captions</p>', unsafe_allow_html=True)

# Logic
if download_clicked:
    if url_input:
        video_id = yt.extract_video_id(url_input)
        if video_id:
            with st.spinner(f"Fetching {format_type} for Video ID: {video_id}..."):
                transcript = yt.get_transcript(video_id, format_type.lower())
                
                if transcript.startswith("ERROR:"):
                    st.error(transcript)
                else:
                    st.success("✓ Transcript retrieved!")
                    
                    # Preview
                    with st.expander("Preview Transcript"):
                        st.text_area("Content", transcript, height=200)
                    
                    # Download button
                    file_ext = format_type.lower()
                    filename = f"transcript_{video_id}.{file_ext}"
                    st.download_button(
                        label=f"Download {format_type} File",
                        data=transcript,
                        file_name=filename,
                        mime="text/plain" if file_ext == "txt" else "text/vtt" if file_ext == "vtt" else "application/x-subrip"
                    )
        else:
            st.error("Invalid YouTube URL. Please check the link and try again.")
    else:
        st.warning("Please paste a YouTube URL first.")

# Features section
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Instant Download</h3>
            <p>Get your captions in seconds without any signup required</p>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Multiple Formats</h3>
            <p>Download in SRT, TXT, or VTT format based on your needs</p>
        </div>
    """, unsafe_allow_html=True)

with f_col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Safe & Private</h3>
            <p>No data stored, completely private and secure processing</p>
        </div>
    """, unsafe_allow_html=True)

# Bulk mode expander
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("Advanced: Bulk Processing"):
    st.info("Paste multiple URLs (one per line) to fetch all at once.")
    bulk_urls = st.text_area("Bulk URLs", placeholder="https://youtube.com/shorts/...\nhttps://youtube.com/watch?v=...", height=150)
    if st.button("Process Bulk"):
        urls = [u.strip() for u in bulk_urls.split("\n") if u.strip()]
        if urls:
            bulk_results = yt.process_urls(urls, format_type.lower())
            
            combined_text = ""
            for i, res in enumerate(bulk_results, 1):
                combined_text += f"{'='*30}\nVIDEO {i}: {res['url']}\n{'='*30}\n{res['transcript']}\n\n"
            
            st.text_area("Results", combined_text, height=300)
            st.download_button("Download All Results (TXT)", combined_text, file_name="bulk_transcripts.txt")
        else:
            st.warning("No URLs found in the text area.")
