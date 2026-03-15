---
title: Voice Assistant API
emoji: 🎙️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# Multimodal AI Voice Assistant

A lightweight **Multimodal** AI assistant built with **FastAPI**. It supports **Speech-to-Speech (S2S)**, **Text-to-Speech (T2S)**, **Speech-to-Text (S2T)**, and **Text-to-Text (T2T)** workflows using **Faster-Whisper**, **Groq (Llama 3)**, **Edge-TTS**, and **Supabase**.

## Features

-   **Multimodal Workflow**: Seamlessly switch between audio and text inputs/outputs.
-   **Conversation History**: Persistent storage of chats and messages in Supabase.
-   **Authentication**: Secure endpoints using Supabase JWT verification.
-   **Speech-to-Text**: Fast transcription using `faster-whisper`.
-   **LLM Intelligence**: Context-aware responses via Groq's `llama-3.3-70b-versatile`.
-   **Text-to-Speech**: High-quality neural voices using `edge-tts`.
-   **Refactored Architecture**: Modular service-based structure for better maintainability.

## Project Structure

-   [./app.py](./app.py): FastAPI application routes and core logic.
-   [./config.py](./config.py): Configuration management using Pydantic Settings.
-   [./security.py](./security.py): JWT authentication and security dependencies.
-   [./services/](./services/):
    -   `db.py`: Supabase database operations (history, storage).
    -   `llm.py`: Groq API integration with history support.
    -   `transcribe.py`: Whisper audio transcription.
    -   `speak.py`: Edge-TTS voice synthesis.
-   [./requirements.txt](./requirements.txt): Python dependencies.

## Setup Instructions

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
GROQ_API_KEY=your_groq_api_key
```

### 2. Database Setup
Run the following SQL in your Supabase SQL Editor:
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    audio_base64 TEXT,
    media_type TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### 3. Install & Run
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## API Usage

### 1. Chat
- **Endpoint:** `POST /chat`
- **Auth:** `Bearer <Supabase_JWT>`
- **Body (Form-Data):** `audio` (file) or `text` (string), `conversation_id` (optional).
- **Response:** JSON containing `text`, `audio` (Base64), and `conversation_id`.

### 2. List Conversations
- **Endpoint:** `GET /conversations`
- **Auth:** `Bearer <Supabase_JWT>`
- **Response:** List of user conversations with message counts and headings.

### 3. Get Conversation
- **Endpoint:** `GET /conversations/{id}`
- **Auth:** `Bearer <Supabase_JWT>`
- **Response:** Conversation details with full message history.
