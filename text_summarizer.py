import spacy
import streamlit as st
from collections import Counter

class TextSummarizer:
    def __init__(self):
        try:
            # Use st.cache_resource to load model only once
            self.nlp = self.load_model()
        except Exception as e:
            st.error(f"Error loading language model: {str(e)}")
            raise

    @st.cache_resource
    def load_model():
        """Load spaCy model with caching"""
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            st.warning("Downloading language model... This may take a moment.")
            spacy.cli.download("en_core_web_sm")
            return spacy.load("en_core_web_sm")

    def extract_key_information(self, text: str) -> str:
        """Extract important information using basic NLP"""
        if not text.strip():
            return "No text to analyze."
            
        try:
            # Basic sentence splitting
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            if not sentences:
                return "No complete sentences found."

            # Process with spaCy
            doc = self.nlp(text)
            
            # Simple scoring system
            scores = []
            for sent in doc.sents:
                score = 0
                # Named entities boost score
                score += len(list(sent.ents)) * 2
                
                # Count important words
                words = [token.text.lower() for token in sent 
                        if not token.is_stop and not token.is_punct]
                score += len(words) * 0.5
                
                # Bonus for longer meaningful sentences (but not too long)
                if 5 <= len(words) <= 20:
                    score += 1
                    
                scores.append((score, sent.text.strip()))

            # Get top 3 sentences
            top_sentences = sorted(scores, reverse=True)[:3]
            
            if not top_sentences:
                return "Could not identify key information."
                
            # Reconstruct in original order
            summary_sentences = [sent for _, sent in top_sentences]
            summary = " ".join(summary_sentences)
            
            return summary if summary else "No important information found."
            
        except Exception as e:
            st.error(f"Error in text processing: {str(e)}")
            return "Error processing text." 
