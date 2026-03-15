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
            {
                "role": "system",
                "content": """
        You are a friendly voice assistant.

        Rules:
        - Keep responses short and natural for spoken conversation.
        - Do not make assumptions about the user.
        - If a message is unclear, ask a simple clarification question.
        - Do not over-analyze the user's message.
        - Respond directly to what the user said.
        - Avoid markdown or special formatting.
        """
            }
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
