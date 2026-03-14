---
title: Voice Assistant API
emoji: 🎙️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# Speech-to-Speech AI Voice Assistant

A lightweight **Speech-to-Speech (S2S)** voice assistant built with **FastAPI**, **Faster-Whisper** for speech-to-text, **Groq (Llama 3)** for natural language processing, and **gTTS** for text-to-speech.

## Features

-   **Speech-to-Speech Workflow**: Takes audio input and returns a synthesized voice response.
-   **Speech-to-Text**: Fast and accurate transcription using the `faster-whisper` base model.
-   **LLM Integration**: Intelligent responses powered by Groq's `llama-3.3-70b-versatile` model.
-   **Text-to-Speech**: Natural-sounding speech synthesis using Google Text-to-Speech (`gTTS`).
-   **REST API**: Simple FastAPI endpoint that handles both audio and text inputs.

## Project Structure

-   [./app.py](./app.py): Main FastAPI application and API routes.
-   [./transcribe.py](./transcribe.py): Logic for transcribing audio files using Whisper.
-   [./llm.py](./llm.py): Logic for interacting with the Groq API.
-   [./speak.py](./speak.py): Logic for converting text responses back to audio.
-   [./requirements.txt](./requirements.txt): Python dependencies.

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd voice-assistant
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Application

Start the FastAPI server using Uvicorn:
```bash
uvicorn app:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

## API Usage

### Chat Endpoint
**Endpoint:** `POST /chat`

**Parameters:**
- `audio`: (Optional) An audio file (e.g., `.wav`, `.mp3`) to be transcribed.
- `text`: (Optional) Direct text input if audio is not provided.

**Response:**
Returns an audio file (`.wav`) containing the assistant's voice response.

**Example with `curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -F "audio=@/path/to/your/audio.wav" \
  --output response.wav
```


