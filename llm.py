 # voice-assistant/llm.py
from groq import Groq
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

# OpenAI Config (Commented Out)
# from openai import OpenAI
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Groq Config (Free Alternative)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_response(prompt: str) -> str:
    logger.info("Sending prompt to Groq (Llama-3)...")
    try:
        # Example using Groq
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a friendly, helpful, and concise voice assistant. Your responses should be natural, conversational, and easy to understand when spoken aloud. Avoid using markdown formatting like bolding or bullet points in your output, as they won't translate well to speech. Keep your answers brief and to the point."},
                {"role": "user", "content": prompt}
            ]
        )
        logger.info("Received response from Groq")
        return response.choices[0].message.content

        # Original OpenAI logic (Commented Out)
        # response = openai_client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error calling LLM API: {e}")
        return "Sorry, I encountered an error while processing your request."
