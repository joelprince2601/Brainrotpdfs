import streamlit as st

class TextSummarizer:
    def __init__(self):
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            st.error(f"Error loading language model: {str(e)}")
            self.nlp = None
    
    def extract_key_information(self, text: str) -> str:
        """Extract important information using spaCy"""
        if self.nlp is None:
            return text  # Return original text if model isn't available
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
            st.warning(f"Error in text processing: {str(e)}")
            return text
        
