# voice-assistant/speak.py
import edge_tts
# from gtts import gTTS
import uuid
import os
import logging

logger = logging.getLogger(__name__)

# Edge-TTS Config (High Quality Free Voice)
VOICE = "en-IN-NeerjaNeural"

async def synthesize_speech(text: str) -> str:
    logger.info(f"--- SYNTHESIS START ---")
    logger.info(f"Attempting to use Edge-TTS with Voice: {VOICE}")
    os.makedirs("responses", exist_ok=True)
    
    # --- Edge-TTS Logic (Active) ---
    file_path = f"responses/{uuid.uuid4()}.mp3"
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(file_path)
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            logger.info(f"Edge-TTS synthesis SUCCESS: {file_path}")
            return file_path
        else:
            raise Exception("Generated file is empty or missing")
            
    except Exception as e:
        logger.error(f"FATAL: Edge-TTS synthesis failed: {e}")
        raise e  # Stop the request so we can see the error in the logs

    # --- gTTS Logic (Commented Out) ---
    # file_path = f"responses/{uuid.uuid4()}.wav"
    # try:
    #     tts = gTTS(text=text, lang='en')
    #     tts.save(file_path)
    #     logger.info(f"gTTS synthesis complete: {file_path}")
    #     return file_path
    # except Exception as e:
    #     logger.error(f"Error during gTTS synthesis: {e}")
    #     return ""

