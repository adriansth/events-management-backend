from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

async def verify_token(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if not cred.credentials or not cred.credentials.startswith("Bearer"):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")
    
    token = cred.credentials.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Token verification failed: {e}")