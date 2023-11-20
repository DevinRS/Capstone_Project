from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext



class AuthHandler():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBearer()
    SECRET = "SECRET_KEY"

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.SECRET, algorithm="HS256")
    
    def decode_token(self, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET, algorithms=["HS256"])
            return payload['sub']
        except JWTError:
            raise credentials_exception
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Depends(security)):
        return self.decode_token(auth.credentials)