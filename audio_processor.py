import pyttsx3
import os
from typing import Optional
import streamlit as st
import time

class AudioProcessor:
    def __init__(self):
        try:
            # Initialize text-to-speech engine with error handling
            self.tts_engine = pyttsx3.init()
            # Configure TTS settings
            self.tts_engine.setProperty('rate', 150)    # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # Get available voices and set a good quality one
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a female voice
                female_voice = next((voice for voice in voices if "female" in voice.name.lower()), None)
                if female_voice:
                    self.tts_engine.setProperty('voice', female_voice.id)
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
        except Exception as e:
            st.error(f"Error initializing TTS engine: {str(e)}")
            raise
    
    def save_audio(self, text: str, output_path: str) -> bool:
        """Save text as audio file with improved quality and error handling"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Add some pause between sentences for better clarity
                processed_text = '. '.join(sent.strip() for sent in text.split('.') if sent.strip())
                
                # Save to a temporary file first
                temp_path = f"{output_path}.temp"
                self.tts_engine.save_to_file(processed_text, temp_path)
                self.tts_engine.runAndWait()
                
                # Verify the file was created and has content
                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                    # Move to final location
                    if os.path.exists(output_path):
                        os.remove(output_path)
                    os.rename(temp_path, output_path)
                    return True
                
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                    
                return False
                
            except Exception as e:
                st.error(f"Error creating audio (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                return False
            finally:
                # Cleanup temp file if it exists
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass 
