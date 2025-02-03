import spacy
from random import choice

# Load a small English NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Dictionary of slang words and their conversational meanings
slang_dict = {
    "rizz": "charisma or smooth-talking ability.",
    "gyatt": "an exclamation of admiration.",
    "skibidi": "a meme phrase with no fixed meaning.",
    "sigma": "a lone wolf or independent person.",
    "alpha": "a dominant leader type.",
    "beta": "a submissive or less confident person.",
    "ratio": "when a reply gets more engagement than the original post.",
    "L": "a loss or failure.",
    "sus": "suspicious or sketchy.",
    "based": "true, independent opinion.",
    "cap": "a lie or false statement.",
    "mid": "mediocre or average quality.",
    "fumbled the bag": "messed up a big opportunity.",
    "glazing": "excessively praising someone.",
    "NPC": "a person who acts like a background character.",
    "copium": "coping with disappointment."
}

# Predefined conversational responses
response_templates = {
    "rizz": ["You got that rizz or nah?", "Bro, if your rizz was currency, would you be broke?"],
    "gyatt": ["GYATT! You just made me jump!", "Bro just said GYATT like his life depended on it."],
    "L": ["That's a fat L, my guy.", "Hold this L with grace."],
    "ratio": ["Ratio + didn't ask + stay mad.", "You just got ratioed harder than Twitter arguments."],
    "sus": ["You're acting kinda sus, not gonna lie.", "This is looking real Among Us right now."],
    "cap": ["That's cap, ain't no way.", "No cap? Or you capping?"],
    "fumbled the bag": ["Bro fumbled the bag so hard, even AI couldn't recover it.", "Don't worry, there's always a second half."],
    "NPC": ["Bro moving like an NPC in real life.", "NPC dialogue detected."],
    "glazing": ["Bro is glazing too hard 💀.", "Stop glazing him, he's not the GOAT."],
    "mid": ["Mid. Just mid.", "Certified mid-tier take."]
}

def process_text(user_input):
    """Processes input, detects slang, and generates a response."""
    doc = nlp(user_input.lower())

    for token in doc:
        if token.text in slang_dict:
            return choice(response_templates.get(token.text, [f"'{token.text}' means {slang_dict[token.text]}"]))

    return "I didn't catch any slang, but I'm vibing with what you said."

class BrainRotProcessor:
    def __init__(self):
        self.replacements = {
            "hello": "hewwo",
            "please": "pwease",
            "you": "uwu",
            "the": "da",
            "this": "dis",
            "that": "dat",
            "thanks": "tankies",
            "thank you": "tank uwu",
            "what": "wat",
            "with": "wif",
            "my": "mah",
            "i": "me",
            "am": "iz",
            "are": "r",
            # Add more replacements as needed
        }
        self.slang_processor = process_text  # Add access to slang processor
    
    def process_text(self, text):
        """
        Process text through both brain rot and slang processors
        """
        # First check for slang
        slang_response = self.slang_processor(text)
        if slang_response != "I didn't catch any slang, but I'm vibing with what you said.":
            return slang_response
            
        # Then process brain rot replacements
        should_replace = any(word in text.lower() for word in self.replacements.keys())
        
        if not should_replace:
            return text
            
        processed_text = text
        for normal_word, brain_rot_word in self.replacements.items():
            processed_text = self._replace_preserving_case(processed_text, normal_word, brain_rot_word)
            
        return processed_text
    
    def _replace_preserving_case(self, text, old_word, new_word):
        """
        Replace words while preserving the original case
        """
        def replace_match(match):
            matched_text = match.group(0)
            if matched_text.isupper():
                return new_word.upper()
            if matched_text.istitle():
                return new_word.title()
            return new_word.lower()
        
        import re
        pattern = re.compile(r'\b' + re.escape(old_word) + r'\b', re.IGNORECASE)
        return pattern.sub(replace_match, text)
