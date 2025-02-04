import spacy
import streamlit as st
from collections import Counter

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
            
            # Score sentences based on important elements
            sentence_scores = {}
            for sent in doc.sents:
                score = 0
                # Count named entities
                score += len([ent for ent in sent.ents])
                # Count important POS tags
                pos_counts = Counter(token.pos_ for token in sent)
                score += pos_counts.get('NOUN', 0) * 0.5
                score += pos_counts.get('PROPN', 0) * 0.7
                score += pos_counts.get('VERB', 0) * 0.3
                
                sentence_scores[sent.text.strip()] = score
            
            # Select top scoring sentences
            important_sentences = sorted(
                [(score, sent) for sent, score in sentence_scores.items() if score > 0],
                reverse=True
            )
            
            # Take top 3 sentences or fewer if less available
            selected_sentences = [sent for _, sent in important_sentences[:3]]
            
            if selected_sentences:
                # Sort sentences by their original order
                original_sentences = [sent.text.strip() for sent in doc.sents]
                ordered_summary = [sent for sent in original_sentences if sent in selected_sentences]
                
                summary = " ".join(ordered_summary)
                return summary
            
            return "No important information found on this page."
            
        except Exception as e:
            st.error(f"Error in text processing: {str(e)}")
            return "" 
