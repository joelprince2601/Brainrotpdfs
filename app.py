import streamlit as st
from text_summarizer import summarize_text
from audio_processor import process_audio
import tempfile
import os

st.set_page_config(
    page_title="Audio & Text Processing App",
    page_icon="🎯",
    layout="wide"
)

st.title("Audio & Text Processing Application")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Text Summarization", "Audio Processing"])

with tab1:
    st.header("Text Summarization")
    text_input = st.text_area("Enter the text you want to summarize:", height=200)
    if st.button("Summarize"):
        if text_input:
            summary = summarize_text(text_input)
            st.success("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter some text to summarize.")

with tab2:
    st.header("Audio Processing")
    uploaded_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3'])
    
    if uploaded_file:
        # Create a temporary file to save the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name
        
        if st.button("Process Audio"):
            try:
                processed_audio = process_audio(audio_path)
                st.success("Audio processed successfully!")
                st.audio(processed_audio)
            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")
            
            # Clean up temporary file
            os.unlink(audio_path) 