# voice-assistant/speak.py
from gtts import gTTS
import uuid
import os
import logging

logger = logging.getLogger(__name__)

def synthesize_speech(text: str) -> str:
    logger.info(f"Starting gTTS synthesis for text: '{text[:50]}...'")
    os.makedirs("responses", exist_ok=True)
    file_path = f"responses/{uuid.uuid4()}.wav"
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(file_path)
        logger.info(f"Speech saved to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error during gTTS synthesis: {e}")
        return ""
