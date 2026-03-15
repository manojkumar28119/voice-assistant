# voice-assistant/services/transcribe.py
from faster_whisper import WhisperModel
import logging
from config import settings

logger = logging.getLogger(__name__)

model = WhisperModel(settings.WHISPER_MODEL)

def transcribe_audio(file_path: str) -> str:
    logger.info(f"Starting Whisper transcription for: {file_path}")
    segments, info = model.transcribe(file_path)
    result = " ".join([segment.text for segment in segments])
    logger.info("Whisper transcription complete")
    return result
