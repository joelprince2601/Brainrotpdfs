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

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm 