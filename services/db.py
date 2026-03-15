# voice-assistant/services/db.py
import logging
from supabase import create_client, Client
from config import settings

logger = logging.getLogger(__name__)

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def get_history(conversation_id: str, limit: int = 10):
    try:
        response = supabase.table("messages") \
            .select("role, content") \
            .eq("conversation_id", conversation_id) \
            .order("created_at", desc=False) \
            .limit(limit) \
            .execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return []

def create_conversation(user_id: str):
    """Creates a new conversation record and returns the ID."""
    try:
        response = supabase.table("conversations").insert({
            "user_id": user_id
        }).execute()
        if response.data:
            return response.data[0]["id"]
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
    return None

def get_conversations(user_id: str):
    """Fetches all conversations for a specific user with message count and first message preview."""
    try:
        # Fetch conversations
        response = supabase.table("conversations") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()
        
        conversations = response.data
        
        # For each conversation, get count and first message
        for conv in conversations:
            messages_res = supabase.table("messages") \
                .select("content") \
                .eq("conversation_id", conv["id"]) \
                .order("created_at", desc=True) \
                .execute()
            
            messages = messages_res.data
            conv["message_count"] = len(messages)
            
            # The "first" message (earliest) is at the end of the desc list, 
            # or we can just fetch the earliest one separately.
            if messages:
                # Let's get the earliest message for the heading
                first_msg_res = supabase.table("messages") \
                    .select("content") \
                    .eq("conversation_id", conv["id"]) \
                    .order("created_at", desc=False) \
                    .limit(1) \
                    .execute()
                if first_msg_res.data:
                    conv["heading"] = first_msg_res.data[0]["content"]
                else:
                    conv["heading"] = "New Conversation"
            else:
                conv["heading"] = "New Conversation"
                
        return conversations
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        return []

def get_conversation_by_id(conversation_id: str, user_id: str):
    """Fetches a specific conversation by ID and ensures it belongs to the user."""
    try:
        # Get conversation details
        response = supabase.table("conversations") \
            .select("*") \
            .eq("id", conversation_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not response.data:
            return None
            
        conv = response.data[0]
        
        # Get messages for this conversation
        messages = supabase.table("messages") \
            .select("*") \
            .eq("conversation_id", conversation_id) \
            .order("created_at", desc=False) \
            .execute()
            
        conv["messages"] = messages.data
        return conv
    except Exception as e:
        logger.error(f"Error fetching conversation by ID: {e}")
        return None

def store_message(conversation_id: str, role: str, content: str, audio_base64: str = None, media_type: str = None):
    try:
        data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content
        }
        if audio_base64:
            data["audio_base64"] = audio_base64
        if media_type:
            data["media_type"] = media_type
            
        supabase.table("messages").insert(data).execute()
    except Exception as e:
        logger.error(f"Error storing message: {e}")
