from datetime import datetime, timedelta, timezone
from typing import Literal
import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Auth Service", version="0.1.0")
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_MINUTES = 60

Role = Literal["Admin", "Agent", "Viewer"]

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    tenant_id: str
    role: Role = "Viewer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    tenant_id: str

class TenantCreate(BaseModel):
    tenant_id: str
    organization_name: str

# Initial in-memory stores (replace with PostgreSQL repositories).
users: dict[str, dict] = {}
tenants: dict[str, dict] = {}

def create_access_token(user: dict) -> str:
    payload = {
        "sub": user["email"],
        "tenant_id": user["tenant_id"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_principal(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

@app.post("/api/auth/tenants")
def create_tenant(data: TenantCreate):
    if data.tenant_id in tenants:
        raise HTTPException(status_code=409, detail="Tenant already exists")
    tenants[data.tenant_id] = data.model_dump()
    return {"tenant": tenants[data.tenant_id]}

@app.post("/api/auth/signup")
def signup(data: UserSignup):
    key = f"{data.tenant_id}:{data.email.lower()}"
    if key in users:
        raise HTTPException(status_code=409, detail="User already exists")
    if data.tenant_id not in tenants:
        raise HTTPException(status_code=404, detail="Tenant not found")

    users[key] = {
        "email": data.email.lower(),
        "tenant_id": data.tenant_id,
        "full_name": data.full_name,
        "role": data.role,
        "hashed_password": pwd_context.hash(data.password),
    }
    token = create_access_token(users[key])
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/auth/login")
def login(data: UserLogin):
    key = f"{data.tenant_id}:{data.email.lower()}"
    user = users.get(key)
    if not user or not pwd_context.verify(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/auth/me")
def me(principal=Depends(get_current_principal)):
    return principal

@app.get('/health')
def health():
    return {"status": "ok", "service": "auth"}
