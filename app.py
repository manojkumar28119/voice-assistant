from fastapi import FastAPI, UploadFile, Form, BackgroundTasks, Header, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from transcribe import transcribe_audio
from speak import synthesize_speech
from llm import get_llm_response
import os
import shutil
import logging
import base64
from jose import jwt
from dotenv import load_dotenv
import requests

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL environment variable is not set")

_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        try:
            url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            _jwks_cache = response.json()
        except Exception as e:
            logger.error(f"Failed to fetch JWKS: {e}")
            raise HTTPException(status_code=500, detail="Authentication service unreachable")
    return _jwks_cache

def verify_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = authorization.split(" ")[1]
    jwks = get_jwks()
    
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next(
            k for k in jwks["keys"]
            if k["kid"] == unverified_header.get("kid")
        )
        payload = jwt.decode(
            token,
            key,
            algorithms=["ES256"],
            audience="authenticated"
        )
        return payload
    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
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
async def chat(background_tasks: BackgroundTasks, payload: dict = Depends(verify_user), audio: UploadFile = None, text: str = Form(None)):
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
    output_path = await synthesize_speech(reply)
    logger.info(f"Speech synthesis complete, saved to {output_path}")

    # Read the audio file and encode to base64
    with open(output_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

    if output_path:
        background_tasks.add_task(cleanup, audio_path, output_path)

    return JSONResponse(content={
        "text": reply,
        "audio": audio_base64,
        "media_type": "audio/mpeg"
    })
