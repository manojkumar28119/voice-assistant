# voice-assistant/security.py
import logging
import requests
from fastapi import Header, HTTPException, Depends
from jose import jwt
from config import settings

logger = logging.getLogger(__name__)

_jwks_cache = None

def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        try:
            url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
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
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise ValueError("Invalid scheme")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
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
