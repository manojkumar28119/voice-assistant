# voice-assistant/services/speak.py
import edge_tts
import uuid
import os
import logging
from config import settings

logger = logging.getLogger(__name__)

async def synthesize_speech(text: str) -> str:
    logger.info(f"--- SYNTHESIS START ---")
    os.makedirs(settings.RESPONSES_DIR, exist_ok=True)
    
    file_path = f"{settings.RESPONSES_DIR}/{uuid.uuid4()}.mp3"
    try:
        communicate = edge_tts.Communicate(text, settings.TTS_VOICE)
        await communicate.save(file_path)
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            logger.info(f"Edge-TTS synthesis SUCCESS: {file_path}")
            return file_path
        else:
            raise Exception("Generated file is empty or missing")
            
    except Exception as e:
        logger.error(f"Edge-TTS synthesis failed: {e}")
        raise e
