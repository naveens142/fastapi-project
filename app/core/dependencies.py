from fastapi import Header, Depends, HTTPException, FastAPI
from app.core.config import settings
from app.core.security import verify_token

def get_api_key(api_key: str = Header(...)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=404, detail=f"invalid key Input Key:{api_key} expected key:{settings.API_KEY}")
    

def get_current_user(token: str = Header(...)):
        payload = verify_token(token)
        if not payload:
             raise HTTPException(status_code=401, detail="Invalid JWT Token")
        return payload
