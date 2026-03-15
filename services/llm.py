# voice-assistant/services/llm.py
import logging
from groq import Groq
from config import settings

logger = logging.getLogger(__name__)

groq_client = Groq(api_key=settings.GROQ_API_KEY)

def get_llm_response(prompt: str, history: list = None) -> str:
    logger.info("Sending prompt to Groq...")
    try:
        messages = [
            {"role": "system", "content": "You are a friendly, helpful, and concise voice assistant. Your responses should be natural and conversational. Avoid markdown formatting."}
        ]
        
        if history:
            for msg in history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": prompt})

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return "Sorry, I encountered an error."
