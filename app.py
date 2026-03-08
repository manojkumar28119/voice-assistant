from fastapi import FastAPI, UploadFile, Form, BackgroundTasks
from fastapi.responses import FileResponse
from transcribe import transcribe_audio
from speak import synthesize_speech
from llm import get_llm_response
import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

def cleanup(*file_paths: str):
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Deleted temporary file: {path}")
            except Exception as e:
                logger.error(f"Error deleting file {path}: {e}")

@app.post("/chat")
async def chat(background_tasks: BackgroundTasks, audio: UploadFile = None, text: str = Form(None)):
    logger.info("Received request to /chat")
    if not audio and not text:
        logger.warning("No audio or text provided in the request")
        return {"error": "No audio or text provided"}

    audio_path = None
    if audio:
        logger.info(f"Processing audio file: {audio.filename}")
        os.makedirs("temp", exist_ok=True)
        audio_path = f"temp/{audio.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        logger.info(f"Audio file saved to {audio_path}, starting transcription...")
        user_input = transcribe_audio(audio_path)
        logger.info(f"Transcription complete: '{user_input}'")
    else:
        logger.info(f"Processing text input: '{text}'")
        user_input = text

    logger.info("Requesting response from LLM...")
    reply = get_llm_response(user_input)
    logger.info(f"LLM reply: '{reply}'")

    logger.info("Synthesizing speech...")
    output_path = synthesize_speech(reply)
    logger.info(f"Speech synthesis complete, saved to {output_path}")

    if output_path:
        background_tasks.add_task(cleanup, audio_path, output_path)

    return FileResponse(output_path, media_type="audio/wav")
