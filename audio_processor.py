import pyttsx3
import os
from typing import Optional

class AudioProcessor:
    def __init__(self):
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        # Configure TTS settings
        self.tts_engine.setProperty('rate', 150)    # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices and set a good quality one
        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            # Prefer a female voice if available
            if "female" in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        else:
            # Otherwise use the first available voice
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
    
    def save_audio(self, text: str, output_path: str) -> bool:
        """Save text as audio file with improved quality"""
        try:
            # Add some pause between sentences for better clarity
            processed_text = '. '.join(sent.strip() for sent in text.split('.') if sent.strip())
            
            self.tts_engine.save_to_file(processed_text, output_path)
            self.tts_engine.runAndWait()
            
            # Verify the file was created and has content
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return True
            return False
        except Exception as e:
            print(f"Error creating audio: {str(e)}")
            return False 