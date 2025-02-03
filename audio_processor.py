import pyttsx3
import os
import streamlit as st
from typing import Optional

class AudioProcessor:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
        except Exception as e:
            st.error(f"Error initializing text-to-speech: {str(e)}")
            self.engine = None
    
    def save_audio(self, text, output_path):
        """Save text as audio file"""
        try:
            if self.engine is None:
                self.engine = pyttsx3.init(driverName='espeak')  # Fallback to espeak
            
            # Configure the engine
            self.engine.setProperty('rate', 150)    # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume (0-1)
            
            # Save to file
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            return os.path.exists(output_path)
            
        except Exception as e:
            st.error(f"Error generating audio: {str(e)}")
            return False

    def save_audio_improved(self, text: str, output_path: str) -> bool:
        """Save text as audio file with improved quality"""
        try:
            # Add some pause between sentences for better clarity
            processed_text = '. '.join(sent.strip() for sent in text.split('.') if sent.strip())
            
            self.engine.save_to_file(processed_text, output_path)
            self.engine.runAndWait()
            
            # Verify the file was created and has content
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return True
            return False
        except Exception as e:
            print(f"Error creating audio: {str(e)}")
            return False 
