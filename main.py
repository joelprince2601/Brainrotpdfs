import streamlit as st
import tempfile
import os
import time
import subprocess
import sys
from pathlib import Path
from pdf_extractor import PDFExtractor
from text_summarizer import TextSummarizer
from audio_processor import AudioProcessor
from video_processor import VideoProcessor

# Must be the first Streamlit command
st.set_page_config(page_title="PDF Processor with AI", page_icon="📚")

# Create data directory if it doesn't exist
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

@st.cache_resource
def load_spacy_model():
    """Load spaCy model with caching"""
    try:
        import spacy
        return spacy.load("en_core_web_sm")
    except OSError:
        st.info("Downloading language model... This may take a moment.")
        import spacy.cli
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")
    except Exception as e:
        st.error(f"Error loading language model: {str(e)}")
        return None

@st.cache_data
def get_temp_file_path(prefix, suffix):
    """Generate a temporary file path in the data directory"""
    timestamp = int(time.time() * 1000)
    return str(DATA_DIR / f"{prefix}_{timestamp}{suffix}")

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = time.time()
    for file in DATA_DIR.glob("*"):
        if file.name == ".gitkeep":
            continue
        if current_time - file.stat().st_mtime > 3600:  # 1 hour
            try:
                file.unlink()
            except Exception as e:
                st.warning(f"Could not remove old file {file}: {str(e)}")

def main():
    # Clean up old files
    cleanup_old_files()
    
    # Load spaCy model at startup
    try:
        nlp = load_spacy_model()
    except Exception as e:
        st.error(f"Error loading language model: {str(e)}")
        return

    st.title("PDF Processor with AI")
    st.write("""
    This application processes PDF documents using AI to:
    1. Extract text from PDF
    2. Identify important information using spaCy
    3. Generate audio summaries with video
    """)
    
    # Initialize processors
    pdf_extractor = PDFExtractor()
    text_summarizer = TextSummarizer()
    audio_processor = AudioProcessor()
    video_processor = VideoProcessor("https://www.youtube.com/watch?v=u7kdVe8q5zs")
    
    # File uploader
    uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_pdf is not None:
        # Save uploaded PDF to data directory
        pdf_path = get_temp_file_path("uploaded", ".pdf")
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.getvalue())
        
        try:
            # Process PDF
            page_texts = pdf_extractor.extract_text_from_pdf(pdf_path)
            
            # Process each page
            for page_num, text in page_texts.items():
                with st.expander(f"Page {page_num}"):
                    try:
                        # Show original text
                        st.write("**Original Text:**")
                        st.text(text[:500] + "..." if len(text) > 500 else text)
                        
                        # Generate summary
                        summary = text_summarizer.extract_key_information(text)
                        if not summary:
                            st.warning("No summary could be generated for this page")
                            continue
                        
                        st.write("**Summary:**")
                        st.write(summary)
                        
                        # Create files with unique names in data directory
                        audio_path = get_temp_file_path(f"summary_page_{page_num}", ".mp3")
                        
                        try:
                            # Generate audio
                            with st.spinner("Generating audio..."):
                                if audio_processor.save_audio(summary, audio_path):
                                    with st.spinner("Creating video player..."):
                                        if video_processor.create_video_player(audio_path, summary):
                                            st.success("Processing complete!")
                                        else:
                                            st.error("Failed to create video player")
                                else:
                                    st.error("Failed to generate audio")
                        except Exception as e:
                            st.error(f"Error processing audio/video: {str(e)}")
                            if os.path.exists(audio_path):
                                os.unlink(audio_path)
                    
                    except Exception as e:
                        st.error(f"Error processing page {page_num}: {str(e)}")
                        continue
        
        finally:
            # Clean up the uploaded PDF
            try:
                if os.path.exists(pdf_path):
                    os.unlink(pdf_path)
            except Exception as e:
                st.warning(f"Could not remove temporary PDF file: {str(e)}")

if __name__ == "__main__":
    main() 
