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
        padding: 1rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3rem;
    }
    .logo {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d2d2d;
    }
    .nav-links {
        display: flex;
        gap: 1.5rem;
        color: #5d5d5d;
        font-size: 0.9rem;
    }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    h1 {
        font-size: 2.5rem !important;
        color: #2d2d2d !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        font-size: 1rem;
        color: #6d6d6d;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Main Card Container */
    .main-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 3rem;
    }
    
    /* Input Group Styling */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 0.8rem 1.2rem !important;
        background: #fafafa !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #c99b5a !important;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #c99b5a !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        border: none !important;
        height: 3.2rem !important;
        margin-top: 1px !important;
    }
    .stButton > button:hover {
        background-color: #b88a49 !important;
        box-shadow: 0 4px 12px rgba(201, 155, 90, 0.3) !important;
    }
    
    /* Radio Buttons / Format Selector */
    .stHorizontalBlock [data-testid="stWidgetLabel"] {
        display: none;
    }
    [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0;
    }
    
    /* Feature Icons - Reference style */
    .feature-item {
        text-align: center;
        margin-top: 2rem;
    }
    .feature-icon-wrapper {
        width: 50px;
        height: 50px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.8rem;
        font-size: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    .feature-item h3 {
        font-size: 1rem !important;
        color: #2d2d2d !important;
        font-weight: 600 !important;
        margin-bottom: 0.3rem !important;
    }
    .feature-item p {
        font-size: 0.85rem !important;
        color: #6d6d6d !important;
        line-height: 1.4 !important;
    }
    
    /* Footer Note */
    .note {
        text-align: center;
        font-size: 0.85rem;
        color: #8d8d8d;
        margin-top: 1.5rem;
    }

    /* Streamlit Overrides */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.4);
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Navigation
st.markdown("""
    <div class="nav-container">
        <div class="logo">CaptionGrab</div>
        <div class="nav-links">
            <span>Home</span>
            <span>How it works</span>
            <span>FAQ</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-container">
        <h1>Download YouTube Shorts Captions</h1>
        <p class="subtitle">Extract captions and subtitles from any YouTube Shorts video instantly. Free, fast, and simple.</p>
    </div>
""", unsafe_allow_html=True)

# Main Card Wrapper
st.markdown('<div class="main-card">', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input("YouTube URL", placeholder="Paste YouTube Shorts URL here...", label_visibility="collapsed")

with col2:
    download_clicked = st.button("Get Captions")

# Format selection
format_type = st.radio(
    "Select Format",
    options=["SRT", "TXT", "VTT"],
    horizontal=True,
    index=0
)

st.markdown('<p class="note">Supports all YouTube Shorts videos with available captions</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Logic execution
if download_clicked:
    if url_input:
        video_id = yt.extract_video_id(url_input)
        if video_id:
            with st.spinner(f"Fetching..."):
                transcript = yt.get_transcript(video_id, format_type.lower())
                
                if transcript.startswith("ERROR:"):
                    st.error(transcript)
                else:
                    st.success("✓ Transcript retrieved!")
                    with st.expander("Preview"):
                        st.text_area("Content", transcript, height=200)
                    
                    file_ext = format_type.lower()
                    st.download_button(
                        label=f"Download {format_type}",
                        data=transcript,
                        file_name=f"transcript_{video_id}.{file_ext}",
                        mime="text/plain"
                    )
        else:
            st.error("Invalid YouTube URL")
    else:
        st.warning("Please paste a URL")

# Features section - Using the minimal circular icon style
st.markdown("<br><br>", unsafe_allow_html=True)
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon-wrapper">⚡</div>
            <h3>Instant Download</h3>
            <p>Get your captions in seconds without any signup required</p>
        </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon-wrapper">🎯</div>
            <h3>Multiple Formats</h3>
            <p>Download in SRT, TXT, or VTT format based on your needs</p>
        </div>
    """, unsafe_allow_html=True)

with f_col3:
    st.markdown("""
        <div class="feature-item">
            <div class="feature-icon-wrapper">🔒</div>
            <h3>Safe & Private</h3>
            <p>No data stored, completely private and secure processing</p>
        </div>
    """, unsafe_allow_html=True)

# Bulk mode - subtle expander at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("Advanced: Bulk Processing"):
    bulk_urls = st.text_area("Bulk URLs (one per line)", height=150)
    if st.button("Process Bulk"):
        urls = [u.strip() for u in bulk_urls.split("\n") if u.strip()]
        if urls:
            results = yt.process_urls(urls, format_type.lower())
            combined = "\n\n".join([f"--- {r['url']} ---\n{r['transcript']}" for r in results])
            st.download_button("Download All", combined, file_name="bulk_transcripts.txt")
