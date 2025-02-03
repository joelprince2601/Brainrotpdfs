import spacy
import streamlit as st

class TextSummarizer:
    def __init__(self):
        # Load English language model from spaCy
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("Language model not loaded. Please refresh the page.")
            raise
    
    def extract_key_information(self, text: str) -> str:
        """Extract important information using spaCy"""
        try:
            doc = self.nlp(text)
            
            # Extract named entities, noun phrases, and important sentences
            entities = [ent.text for ent in doc.ents]
            
            # Basic summarization by selecting sentences with entities
            important_sentences = []
            for sent in doc.sents:
                if any(ent.text in sent.text for ent in doc.ents):
                    important_sentences.append(sent.text)
            
            # Combine the summary
            summary = " ".join(important_sentences)
            return summary if summary else "No important information found on this page."
        except Exception as e:
            st.error(f"Error in text processing: {str(e)}")
            return "" 
