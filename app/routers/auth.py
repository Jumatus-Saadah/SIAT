from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.auth import hash_password, verify_password, create_token
from pydantic import BaseModel

router = APIRouter(tags=["Autentikasi"])

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str  # kasir / manajer
    id_cabang: int = None

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username sudah dipakai")
    user = models.User(
        username=data.username,
        password=hash_password(data.password),
        role=data.role,
        id_cabang=data.id_cabang
    )
    db.add(user)
    db.commit()
    return {"message": "User berhasil didaftarkan"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    token = create_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}