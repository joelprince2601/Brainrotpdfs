import streamlit as st
import pdfplumber
import spacy
import pyttsx3
import tempfile
from pathlib import Path
from typing import List, Dict
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import time

# Check if video exists
VIDEO_PATH = "videoplayback.mp4"
if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video file '{VIDEO_PATH}' not found in the current directory")

class PDFProcessor:
    def __init__(self):
        # Load English language model from spaCy
        self.nlp = spacy.load("en_core_web_sm")
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        """Extract text from PDF file page by page"""
        page_texts = {}
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    page_texts[page_num] = text.strip()
        
        return page_texts
    
    def extract_key_information(self, text: str) -> str:
        """Extract important information using spaCy"""
        doc = self.nlp(text)
        
        # Extract named entities, noun phrases, and important sentences
        entities = [ent.text for ent in doc.ents]
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        # Basic summarization by selecting sentences with entities or important nouns
        important_sentences = []
        for sent in doc.sents:
            if any(ent.text in sent.text for ent in doc.ents):
                important_sentences.append(sent.text)
        
        # Combine the summary
        summary = " ".join(important_sentences)
        return summary if summary else "No important information found on this page."
    
    def save_audio(self, text: str, output_path: str):
        """Save text as audio file"""
        self.tts_engine.save_to_file(text, output_path)
        self.tts_engine.runAndWait()

    def create_video_with_audio(self, audio_path: str, output_path: str):
        """Combine video with TTS audio"""
        video = None
        audio = None
        final_video = None
        temp_output = None
        
        try:
            video = VideoFileClip(VIDEO_PATH)
            audio = AudioFileClip(audio_path)
            
            # If audio is shorter than video, create a looped version manually
            if audio.duration < video.duration:
                from moviepy.audio.AudioClip import concatenate_audioclips
                
                # Calculate how many times we need to loop the audio
                num_repeats = int(video.duration / audio.duration) + 1
                
                # Create a list of audio clips
                audio_list = []
                remaining_duration = video.duration
                
                while remaining_duration > 0:
                    if remaining_duration >= audio.duration:
                        # Add full audio clip
                        audio_list.append(AudioFileClip(audio_path))
                        remaining_duration -= audio.duration
                    else:
                        # Add partial audio clip for the last piece
                        partial_clip = AudioFileClip(audio_path).set_end(remaining_duration)
                        audio_list.append(partial_clip)
                        remaining_duration = 0
                
                # Concatenate all audio clips
                final_audio = concatenate_audioclips(audio_list)
                
                # Clean up the individual clips
                for clip in audio_list:
                    if clip != audio:  # Don't close the original audio yet
                        clip.close()
                
            else:
                # If audio is longer, just trim it
                final_audio = audio.set_end(video.duration)
            
            # Set the audio to the video
            final_video = video.set_audio(final_audio)
            
            # Write the final video file with progress bar
            st.write("Processing video...")
            progress_bar = st.progress(0)
            
            def write_progress(t):
                progress_bar.progress(min(t/video.duration, 1.0))
            
            # Use temporary file for processing
            temp_output = tempfile.mktemp(suffix='.mp4')
            
            final_video.write_videofile(
                temp_output,
                codec='libx264',
                audio_codec='aac',
                progress_bar=False,
                callback=write_progress,
                fps=video.fps
            )
            
            # Close all resources before moving the file
            if final_video:
                final_video.close()
            if video:
                video.close()
            if audio:
                audio.close()
            if final_audio and final_audio != audio:
                final_audio.close()
            
            # Move the completed file to its final location
            import shutil
            if os.path.exists(temp_output):
                if os.path.exists(output_path):
                    os.remove(output_path)
                shutil.move(temp_output, output_path)
            
            # Clear progress bar
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            raise
            
        finally:
            # Clean up all resources
            try:
                if final_video:
                    final_video.close()
                if video:
                    video.close()
                if audio:
                    audio.close()
                if 'final_audio' in locals() and final_audio and final_audio != audio:
                    final_audio.close()
                
                # Remove temporary output file if it exists
                if temp_output and os.path.exists(temp_output):
                    try:
                        os.remove(temp_output)
                    except:
                        pass
                    
            except Exception as cleanup_error:
                st.warning(f"Error during cleanup: {str(cleanup_error)}")

def main():
    st.set_page_config(page_title="PDF Processor with AI", page_icon="📚")
    
    st.title("PDF Processor with AI")
    st.write("""
    This application processes PDF documents using AI to:
    1. Extract text from PDF
    2. Identify important information using spaCy
    3. Generate audio summaries with video
    """)
    
    # Initialize processor
    processor = PDFProcessor()
    
    # File uploader for PDF only
    uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_pdf is not None:
        # Create temporary file for PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_tmp:
            pdf_tmp.write(uploaded_pdf.getvalue())
            pdf_path = pdf_tmp.name
        
        try:
            # Extract text page by page
            page_texts = processor.extract_text_from_pdf(pdf_path)
            
            # Process each page
            for page_num, text in page_texts.items():
                with st.expander(f"Page {page_num}"):
                    try:
                        st.write("**Original Text:**")
                        st.text(text[:500] + "..." if len(text) > 500 else text)
                        
                        # Extract key information
                        summary = processor.extract_key_information(text)
                        if not summary:
                            st.warning("No summary could be generated for this page")
                            continue
                        
                        st.write("**Summary:**")
                        st.write(summary)
                        
                        # Create unique filenames using timestamp
                        timestamp = int(time.time() * 1000)
                        audio_path = f"summary_page_{page_num}_{timestamp}.mp3"
                        output_video_path = f"video_with_audio_page_{page_num}_{timestamp}.mp4"
                        
                        try:
                            # Create audio file
                            processor.save_audio(summary, audio_path)
                            if not os.path.exists(audio_path):
                                raise Exception("Audio file was not created")
                            
                            # Create video with audio
                            processor.create_video_with_audio(audio_path, output_video_path)
                            if os.path.exists(output_video_path):
                                st.video(output_video_path)
                            else:
                                raise Exception("Video file was not created")
                                
                        finally:
                            # Clean up temporary files with improved retry mechanism
                            for file_path in [audio_path, output_video_path]:
                                for attempt in range(3):  # Try up to 3 times
                                    try:
                                        if os.path.exists(file_path):
                                            # Force close any open handles
                                            try:
                                                with open(file_path, 'a'):
                                                    pass
                                            except:
                                                pass
                                            
                                            try:
                                                os.remove(file_path)
                                                break  # If successful, break the retry loop
                                            except PermissionError:
                                                if attempt < 2:  # Don't sleep on last attempt
                                                    time.sleep(2)  # Wait longer between attempts
                                    except Exception as e:
                                        if attempt == 2:  # Only warn on last attempt
                                            st.warning(f"Could not remove temporary file {file_path}")
                            
                    except Exception as e:
                        st.error(f"Error processing page {page_num}: {str(e)}")
                        continue
            
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
        finally:
            # Clean up temporary PDF file
            os.unlink(pdf_path)

if __name__ == "__main__":
    main() 