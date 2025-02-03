import streamlit as st
import tempfile
import os
import time
import subprocess
import sys
from pdf_extractor import PDFExtractor
from text_summarizer import TextSummarizer
from audio_processor import AudioProcessor
from video_processor import VideoProcessor

# Must be the first Streamlit command
st.set_page_config(page_title="PDF Processor with AI", page_icon="📚")

@st.cache_resource
def load_spacy_model():
    """Load spaCy model with caching"""
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        # Download the model if it's not installed
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
    return nlp

def main():
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
        # Save uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_tmp:
            pdf_tmp.write(uploaded_pdf.getvalue())
            pdf_path = pdf_tmp.name
        
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
                        
                        # Create files with unique names
                        timestamp = int(time.time() * 1000)
                        audio_path = f"summary_page_{page_num}_{timestamp}.mp3"
                        video_path = f"video_with_audio_page_{page_num}_{timestamp}.mp4"
                        
                        try:
                            # Generate audio
                            st.write("Generating audio...")
                            if audio_processor.save_audio(summary, audio_path):
                                st.write("Creating video player...")
                                if video_processor.create_video_player(audio_path, summary):
                                    st.success("Processing complete!")
                                else:
                                    st.error("Failed to create video player")
                            else:
                                st.error("Failed to generate audio")
                        finally:
                            # Cleanup with improved file handling
                            for file_path in [audio_path, video_path]:
                                for retry in range(3):  # Try up to 3 times
                                    try:
                                        if os.path.exists(file_path):
                                            # Force close any handles
                                            import psutil
                                            for proc in psutil.process_iter():
                                                try:
                                                    for item in proc.open_files():
                                                        if item.path == os.path.abspath(file_path):
                                                            proc.kill()
                                                except:
                                                    continue
                                            
                                            os.remove(file_path)
                                            break  # Success, exit retry loop
                                    except Exception as e:
                                        if retry == 2:  # Last attempt
                                            st.warning(f"Could not remove temporary file {file_path}: {str(e)}")
                                        else:
                                            time.sleep(1)  # Wait before retry
                    
                    except Exception as e:
                        st.error(f"Error processing page {page_num}: {str(e)}")
                        continue
        
        finally:
            # Clean up PDF
            if os.path.exists(pdf_path):
                os.unlink(pdf_path)

if __name__ == "__main__":
    main() 
