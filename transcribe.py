# voice-assistant/transcribe.py
from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)

model = WhisperModel("base")

def transcribe_audio(file_path: str) -> str:
    logger.info(f"Starting Whisper transcription for file: {file_path}")
    segments, info = model.transcribe(file_path)
    logger.info(f"Detected language: {info.language} with probability {info.language_probability:.2f}")
    result = " ".join([segment.text for segment in segments])
    logger.info("Whisper transcription complete")
    return result
