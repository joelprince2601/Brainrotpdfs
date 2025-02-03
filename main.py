import streamlit as st
import tempfile
import os
import time
import spacy
import subprocess
from pdf_extractor import PDFExtractor
from text_summarizer import TextSummarizer
from audio_processor import AudioProcessor
from video_processor import VideoProcessor
from brainrotslang import BrainRotProcessor

@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.warning("Installing spaCy model... This may take a moment.")
        try:
            import en_core_web_sm
            return en_core_web_sm.load()
        except ImportError:
            st.error("Failed to load spaCy model. Please contact support.")
            return None

def main():
    st.set_page_config(page_title="PDF Processor with AI", page_icon="📚")
    
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
    brain_rot_processor = BrainRotProcessor()
    
    # Use this in your main function
    nlp = load_spacy_model()
    
    if nlp is None:
        st.error("Could not initialize the language model. Some features may not work.")
        return
    
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
                            # Process text through brain rot language processor
                            processed_summary = brain_rot_processor.process_text(summary)
                            if processed_summary != summary:
                                st.info("Brain rot language detected and processed! 🧠")
                                st.write("**Processed Summary:**")
                                st.write(processed_summary)
                            
                            # Generate audio
                            st.write("Generating audio...")
                            if audio_processor.save_audio(processed_summary, audio_path):
                                st.write("Creating video player...")
                                if video_processor.create_video_player(audio_path, processed_summary):
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
