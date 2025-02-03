import streamlit as st
from text_summarizer import summarize_text
from audio_processor import process_audio
import tempfile
import os

# Configure page settings
st.set_page_config(
    page_title="Audio & Text Processing App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for better UI
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("Audio & Text Processing Application")
    
    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Text Summarization", "Audio Processing"])

    with tab1:
        st.header("Text Summarization")
        text_input = st.text_area("Enter the text you want to summarize:", height=200)
        
        if st.button("Summarize"):
            if not text_input.strip():
                st.warning("Please enter some text to summarize.")
                return
                
            with st.spinner("Generating summary..."):
                try:
                    summary = summarize_text(text_input)
                    st.success("Summary generated successfully!")
                    st.write(summary)
                except Exception as e:
                    st.error(f"An error occurred while summarizing: {str(e)}")

    with tab2:
        st.header("Audio Processing")
        uploaded_file = st.file_uploader(
            "Upload an audio file (WAV or MP3)", 
            type=['wav', 'mp3']
        )
        
        if uploaded_file:
            st.audio(uploaded_file, format='audio/wav')
            
            if st.button("Process Audio"):
                with st.spinner("Processing audio..."):
                    try:
                        # Create a temporary file to save the uploaded audio
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            audio_path = tmp_file.name
                        
                        processed_audio = process_audio(audio_path)
                        st.success("Audio processed successfully!")
                        st.audio(processed_audio)
                        
                        # Clean up temporary file
                        os.unlink(audio_path)
                    except Exception as e:
                        st.error(f"Error processing audio: {str(e)}")

if __name__ == "__main__":
    main() 
