import streamlit as st
import youtube_transcript_generator as yt
import base64

# Page configurations
st.set_page_config(
    page_title="CaptionGrab",
    page_icon="⚡",
    layout="centered"
)

# Custom CSS - Clean, Native, Robust
st.markdown("""
    <style>
    /* 1. Global Reset & Colors */
    .stApp {
        background-color: #E5D4B8;
        background-image: radial-gradient(#d4c5a9 1px, transparent 1px);
        background-size: 20px 20px;
        color: #2d2d2d;
    }
    
    /* 2. Hide Streamlit Bloat */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}

    /* 7. Feature Cards Grid System */
    .feature-grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* 3 Equal Columns */
        gap: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        height: 100%; /* Force fill height */
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        transition: transform 0.2s;
        border: 1px solid rgba(255,255,255,0.5);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    
    /* 8. Layout Constraints (Wide Mode Taming) */
    /* Center the main inputs and limit width */
    div[data-testid="stVerticalBlock"] > div.stVerticalBlock {
        max-width: 800px; /* Keep inputs tidy */
        margin: 0 auto;
    }
    /* Let the nav bar stretch */
    .nav-container {
        max-width: 100%;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    .icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        display: inline-block;
        background: #f8f5f0;
        width: 60px;
        height: 60px;
        line-height: 60px;
        border-radius: 50%;
    }

    /* 3. Typography */
    h1 {
        color: #2d2d2d !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800 !important;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        text-align: center;
        color: #665c4a;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 3rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* 4. Inputs (The "Card" look applied to the widget itself) */
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        padding: 1.5rem !important;
        font-size: 1rem !important;
        color: #333 !important;
        transition: all 0.2s ease;
    }
    .stTextArea textarea:focus {
        border-color: #c99b5a !important;
        box-shadow: 0 10px 15px -3px rgba(201, 155, 90, 0.1), 0 4px 6px -2px rgba(201, 155, 90, 0.05) !important;
        transform: translateY(-2px);
    }

    /* 5. Custom Radio Buttons (Pill/Card style) */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.5) !important;
        border: 2px solid transparent !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        cursor: pointer;
        transition: all 0.2s;
        min-width: 100px;
        justify-content: center;
    }
    div[role="radiogroup"] label:hover {
        background: white !important;
        transform: translateY(-2px);
    }
    /* Selected State */
    div[role="radiogroup"] label[data-checked="true"] {
        background: white !important;
        border-color: #c99b5a !important;
        color: #c99b5a !important;
        box-shadow: 0 4px 12px rgba(201, 155, 90, 0.2);
    }
    /* Radio Text */
    div[role="radiogroup"] p {
        font-weight: 600;
        margin: 0;
        font-size: 1rem;
        color: #333 !important; /* Force dark text */
    }

    /* Error/Success Messages - Custom Theme */
    div[data-testid="stAlert"] {
        background-color: white;
        color: #2d2d2d;
        border: 1px solid rgba(0,0,0,0.05);
        border-left: 5px solid #c99b5a; /* Gold accent */
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    div[data-testid="stAlert"] p {
        font-size: 1rem;
    }
    /* Hide the default icons if possible or let them be */
    
    /* Code/Preview Blocks */
    code {
        color: #2d2d2d !important;
        background-color: #f8f5f0 !important; /* Light beige matching radio */
        font-family: 'Consolas', 'Monaco', monospace;
    }
    .stCodeBlock {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Expander Styling */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border-radius: 12px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    div[data-testid="stExpander"] summary {
        color: #2d2d2d !important;
        font-weight: 600 !important;
    }
    div[data-testid="stExpander"] summary:hover {
        color: #c99b5a !important;
    }

    /* 6. Primary Button & Download Button */
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        background: #c99b5a !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border: none !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #b88a49 !important;
        box-shadow: 0 10px 15px -3px rgba(201, 155, 90, 0.3);
        transform: translateY(-2px);
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: translateY(0);
    }
    </style>
""", unsafe_allow_html=True)

# --- Header / Nav ---
st.markdown("""
    <div class="nav-container" style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 0; margin-bottom: 3rem; border-bottom: 1px solid rgba(0,0,0,0.05);">
        <div class="logo" style="font-weight: 700; font-size: 1.2rem; color: #2d2d2d;">CaptionGrab</div>
        <div class="nav-links" style="display: flex; gap: 2rem;">
            <span style="color: #666; cursor: pointer; font-size: 0.95rem;">Home</span>
            <span style="color: #666; cursor: pointer; font-size: 0.95rem;">How it works</span>
            <span style="color: #666; cursor: pointer; font-size: 0.95rem;">FAQ</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1>Download YouTube Shorts Captions</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Extract captions from any YouTube Shorts video instantly. <br>FAST &middot; FREE &middot; SECURE</p>', unsafe_allow_html=True)

# --- Main Interaction Area ---
input_container = st.container()

with input_container:
    # Text Area - Minimal Style
    urls_input = st.text_area(
        "Enter YouTube URL(s)",
        placeholder="Paste YouTube Shorts URL here...",
        height=120,
        label_visibility="collapsed"
    )

    # Format Selection - Centered
    col_space_1, col_radio, col_space_2 = st.columns([1, 4, 1])
    with col_radio:
        format_type = st.radio(
            "Format",
            options=["SRT", "TXT", "VTT"],
            horizontal=True,
            label_visibility="collapsed",
        )

    # Big Action Button - Centered
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1]) # 2 is middle column width
    with b_col2:
        generate_clicked = st.button("Generate Captions")

    if generate_clicked:
        if not urls_input.strip():
            st.warning("Please paste at least one YouTube URL to get started.")
        else:
            urls = [line.strip() for line in urls_input.split('\n') if line.strip()]
            selected_format = format_type.lower()
            
            # --- LOGIC ---
            if len(urls) == 1:
                # SINGLE MODE
                video_id = yt.extract_video_id(urls[0])
                if video_id:
                    with st.spinner("Talking to YouTube..."):
                        transcript = yt.get_transcript(video_id, selected_format)
                        if transcript.startswith("ERROR:"):
                            st.error(transcript)
                        else:
                            st.success(f"Success! {format_type} ready.")
                            # Preview in an expander to keep UI clean
                            with st.expander("Preview Caption", expanded=False):
                                st.code(transcript, language='text' if selected_format!='srt' else None)
                            
                            st.download_button(
                                label=f"Download {format_type} File",
                                data=transcript,
                                file_name=f"caption_{video_id}.{selected_format}",
                                mime="text/plain"
                            )
                else:
                    st.error("That link doesn't look like a valid YouTube Short.")
            
            else:
                # BULK MODE
                with st.spinner(f"Processing {len(urls)} videos..."):
                    results = yt.process_urls(urls, selected_format)
                    
                    # Count successes
                    valid_results = [r for r in results if not r['transcript'].startswith("ERROR:")]
                    
                    if valid_results:
                        st.success(f"Done! {len(valid_results)}/{len(urls)} captions captured.")
                        
                        combined = ""
                        for r in valid_results:
                            combined += f"--- SOURCE: {r['url']} ---\n{r['transcript']}\n\n"
                        
                        st.download_button(
                            label=f"Download All ({len(valid_results)} files)",
                            data=combined,
                            file_name=f"bulk_captions_{selected_format}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("Could not retrieve captions for any of the provided URLs.")


# --- Feature Grid (HTML/CSS for perfect sizing) ---
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid-container">
    <div class="feature-card">
        <div class="icon">⚡</div>
        <h3>Instant</h3>
        <p class="f-text">Get accurate captions in milliseconds.</p>
    </div>
    <div class="feature-card">
        <div class="icon">📄</div>
        <h3>Flexible</h3>
        <p class="f-text">SRT, VTT, or plain text formats.</p>
    </div>
    <div class="feature-card">
        <div class="icon">🛡️</div>
        <h3>Secure</h3>
        <p class="f-text">We don't store your data.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
