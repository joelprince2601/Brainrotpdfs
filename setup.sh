#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    espeak \
    alsa-utils \
    libespeak1 \
    python3-espeak \
    libsndfile1 \
    portaudio19-dev \
    python3-all-dev

# Install Python dependencies without spaCy first
pip install --no-cache-dir -r <(grep -v "spacy" requirements.txt)

# Install spaCy and its model separately
pip install --no-cache-dir spacy
python -m spacy download en_core_web_sm || pip install --no-cache-dir https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.5.0/en_core_web_sm-3.5.0-py3-none-any.whl 
