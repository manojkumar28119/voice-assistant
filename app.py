# voice-assistant/app.py
from fastapi import FastAPI, UploadFile, Form, BackgroundTasks, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import shutil
import logging
import base64
from config import settings
from security import verify_user
from services.transcribe import transcribe_audio
from services.speak import synthesize_speech
from services.llm import get_llm_response
from services.db import get_history, store_message, create_conversation, get_conversations, get_conversation_by_id

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Voice Assistant API")

def cleanup(*file_paths: str):
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Deleted temporary file: {path}")
            except Exception as e:
                logger.error(f"Error deleting file {path}: {e}")

@app.post("/chat")
async def chat(
    background_tasks: BackgroundTasks,
    user_payload: dict = Depends(verify_user),
    audio: UploadFile = None,
    text: str = Form(None),
    conversation_id: str = Form(None)
):
    logger.info("Received request to /chat")
    if not audio and not text:
        raise HTTPException(status_code=400, detail="No audio or text provided")

    audio_path = None
    if audio:
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
        audio_path = f"{settings.TEMP_DIR}/{audio.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        user_input = transcribe_audio(audio_path)
    else:
        user_input = text

    # Handle Conversation History and Message Storage
    if not conversation_id:
        # Create new conversation if ID not provided
        user_id = user_payload.get("sub")
        conversation_id = create_conversation(user_id)
        history = []
    else:
        history = get_history(conversation_id)
        
    if conversation_id:
        store_message(conversation_id, "user", user_input)

    # Get Response from LLM
    reply = get_llm_response(user_input, history)

    # Synthesize Response Speech
    output_path = await synthesize_speech(reply)

    # Encode Audio to Base64
    with open(output_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

    if conversation_id:
        store_message(conversation_id, "assistant", reply, audio_base64, "audio/mpeg")

    # Cleanup Background Task
    background_tasks.add_task(cleanup, audio_path, output_path)
    return {
        "text": reply,
        "audio": audio_base64,
        "media_type": "audio/mpeg",
        "conversation_id": conversation_id
    }

@app.get("/conversations")
async def list_conversations(user_payload: dict = Depends(verify_user)):
    user_id = user_payload.get("sub")
    conversations = get_conversations(user_id)
    return conversations

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, user_payload: dict = Depends(verify_user)):
    user_id = user_payload.get("sub")
    conversation = get_conversation_by_id(conversation_id, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
