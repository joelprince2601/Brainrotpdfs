import streamlit as st
import os
from pytube import YouTube
import streamlit.components.v1 as components
import re

class VideoProcessor:
    def __init__(self, video_url: str):
        self.video_url = video_url
        try:
            self.yt = YouTube(video_url)
        except Exception as e:
            raise Exception(f"Error loading YouTube video: {str(e)}")
    
    def _chunk_text(self, text: str, words_per_chunk=3):
        """Split text into chunks of approximately N words"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), words_per_chunk):
            chunk = ' '.join(words[i:i + words_per_chunk])
            chunks.append(chunk)
        return chunks

    def create_video_player(self, audio_path: str, text: str):
        """Create a custom video player with synchronized audio and word-by-word subtitles"""
        try:
            # Use streamlit's temp directory
            temp_dir = os.path.join(os.path.dirname(audio_path))
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            chunks = self._chunk_text(text)
            
            html_content = f"""
            <div style="position: relative;">
                <div style="position: relative; padding-bottom: 56.25%;">
                    <iframe
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                        src="https://www.youtube.com/embed/{self.yt.video_id}?enablejsapi=1"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                        id="youtube_player"
                    ></iframe>
                    <div id="subtitle_container" style="position: absolute; bottom: 50px; left: 0; right: 0; text-align: center; z-index: 1000;">
                        <div id="subtitles" style="
                            background: rgba(0, 0, 0, 0.7);
                            color: white;
                            padding: 10px;
                            margin: 0 auto;
                            max-width: 80%;
                            font-size: 24px;
                            border-radius: 5px;
                            display: none;
                            transition: opacity 0.3s;
                        "></div>
                    </div>
                </div>
                <audio id="tts_audio" preload="auto">
                    <source src="data:audio/mp3;base64,{self._get_audio_base64(audio_path)}" type="audio/mp3">
                </audio>
            </div>
            <script>
                var tag = document.createElement('script');
                tag.src = "https://www.youtube.com/iframe_api";
                var firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

                var player;
                var audio = document.getElementById('tts_audio');
                var subtitles = document.getElementById('subtitles');
                var isFirstPlay = true;
                var subtitleTimeout;
                var lastAudioTime = 0;
                var audioCheckInterval;
                
                const chunks = {chunks};
                let currentChunkIndex = 0;
                
                // Constants for timing (100 words per minute)
                const WORDS_PER_MINUTE = 100;
                const MS_PER_WORD = (60 * 1000) / WORDS_PER_MINUTE;

                function onYouTubeIframeAPIReady() {{
                    player = new YT.Player('youtube_player', {{
                        events: {{
                            'onStateChange': onPlayerStateChange,
                            'onReady': onPlayerReady
                        }}
                    }});
                }}

                function onPlayerReady(event) {{
                    audio.load();
                }}

                function showSubtitles(show) {{
                    subtitles.style.display = show ? 'block' : 'none';
                }}

                function updateSubtitles() {{
                    if (currentChunkIndex < chunks.length && player.getPlayerState() === YT.PlayerState.PLAYING) {{
                        const chunk = chunks[currentChunkIndex];
                        subtitles.textContent = chunk;
                        
                        // Calculate delay based on number of words at 100 wpm
                        const words = chunk.split(' ').length;
                        const delay = words * MS_PER_WORD;
                        
                        currentChunkIndex++;
                        subtitleTimeout = setTimeout(updateSubtitles, delay);
                    }}
                }}

                function startSubtitleSync() {{
                    updateSubtitles();
                }}

                function stopSubtitleSync() {{
                    clearTimeout(subtitleTimeout);
                }}

                function onPlayerStateChange(event) {{
                    if (event.data == YT.PlayerState.PLAYING) {{
                        if (isFirstPlay) {{
                            audio.currentTime = 0;
                            currentChunkIndex = 0;
                            showSubtitles(true);
                            audio.play().then(() => {{
                                startSubtitleSync();
                            }}).catch(function(error) {{
                                console.log("Audio play failed:", error);
                            }});
                            isFirstPlay = false;
                        }} else {{
                            showSubtitles(true);
                            audio.play().then(() => {{
                                startSubtitleSync();
                            }});
                        }}
                    }} else if (event.data == YT.PlayerState.PAUSED) {{
                        audio.pause();
                        stopSubtitleSync();
                    }} else if (event.data == YT.PlayerState.ENDED) {{
                        audio.pause();
                        audio.currentTime = 0;
                        showSubtitles(false);
                        isFirstPlay = true;
                        currentChunkIndex = 0;
                        stopSubtitleSync();
                    }}
                }}

                audio.addEventListener('error', function(e) {{
                    console.error('Error loading audio:', e);
                }});
            </script>
            """
            
            components.html(html_content, height=450)
            return True
            
        except Exception as e:
            st.error(f"Error creating video player: {str(e)}")
            return False

    def _get_audio_base64(self, audio_path: str) -> str:
        """Convert audio file to base64 string"""
        import base64
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            return base64.b64encode(audio_data).decode('utf-8') 