from jose import jwt
import uvicorn
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,EmailStr
from fastapi.middleware.cors import CORSMiddleware

# Import your router
from config.settings import settings
from backend.api.routes import router as detection_router
from backend.db.database import get_db
from backend.utils.access_func import create_access_token, hash_password, verify_password

# Initialize FastAPI app
app = FastAPI(
    title="Smart HSRP Monitoring API",
    description="Helmet detection, HSRP classification, and OCR pipeline",
    version="1.0.0"
)

# Allow CORS for frontend / UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your router
app.include_router(detection_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Smart HSRP API is running"}

# Optional root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Smart HSRP Monitoring API"}

# Pydantic models
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    role: str

# API endpoints
@app.post("/signup", response_model=Token)
def signup(user: UserSignup, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    # Validate role
    if user.role not in ['admin', 'user']:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and insert user
    hashed_pw = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (%s, %s, %s) RETURNING id",
        (user.email, hashed_pw, user.role)
    )
    user_id = cursor.fetchone()['id']
    conn.commit()
    
    # Create token
    access_token = create_access_token({"sub": user.email, "role": user.role, "user_id": user_id})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
        email=user.email,
        role=user.role
    )

@app.post("/login", response_model=Token)
def login(user: UserLogin, conn=Depends(get_db)):
    cursor = conn.cursor()
    
    # Get user from database
    cursor.execute("SELECT id, email, password_hash, role FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    
    if not db_user or not verify_password(user.password, db_user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create token
    access_token = create_access_token({
        "sub": db_user['email'],
        "role": db_user['role'],
        "user_id": db_user['id']
    })
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=db_user['id'],
        email=db_user['email'],
        role=db_user['role']
    )

@app.get("/verify-token")
def verify_token(token: str, conn=Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("user_id")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            "valid": True,
            "email": email,
            "role": role,
            "user_id": user_id
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users")
def get_all_users(token: str, conn=Depends(get_db)):
    # Verify admin role
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        role = payload.get("role")
        if role != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, role, created_at FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    return {"users": users}

# Entry point
if __name__ == "__main__":
    # 2025-style high-performance uvicorn run
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Remove in production
        workers=1,    # Increase for multi-core CPUs
        log_level="info"
    )
