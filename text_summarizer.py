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
            
            # Extract sentences with named entities or important noun phrases
            important_sentences = []
            for sent in doc.sents:
                # Check for named entities
                has_entities = len(list(sent.ents)) > 0
                
                # Check for noun chunks (important phrases)
                has_noun_chunks = any(chunk.root.pos_ in ['NOUN', 'PROPN'] for chunk in sent.noun_chunks)
                
                if has_entities or has_noun_chunks:
                    important_sentences.append(sent.text.strip())
            
            # Combine the summary
            if important_sentences:
                summary = " ".join(important_sentences)
                # Ensure the summary isn't too long
                if len(summary) > 1000:
                    summary = " ".join(important_sentences[:3]) + "..."
                return summary
            return "No important information found on this page."
            
        except Exception as e:
            st.error(f"Error in text processing: {str(e)}")
            return "" 
