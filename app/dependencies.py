from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .utils.security import decode_access_token

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Type aliases for cleaner code
DbSession = Annotated[Session, Depends(get_db)]
TokenStr = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(token: TokenStr, db: DbSession) -> User:
    """
    Get the current authenticated user from JWT token.
    Raises 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        print(f"❌ Token decode failed: {token[:50]}...")
        raise credentials_exception
    
    # Get user ID from token (convert from string to int)
    user_id_str = payload.get("sub")
    if user_id_str is None:
        print(f"❌ No 'sub' in token payload: {payload}")
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        print(f"❌ Invalid 'sub' format: {user_id_str}")
        raise credentials_exception
    
    print(f"✅ Token decoded successfully. User ID: {user_id}")
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print(f"❌ User not found in database: ID {user_id}")
        raise credentials_exception
    
    print(f"✅ User found: {user.email}")
    return user

# Type alias for current user dependency
CurrentUser = Annotated[User, Depends(get_current_user)]
