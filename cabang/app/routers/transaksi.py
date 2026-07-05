from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/transaksi", tags=["Transaksi Cabang"])

@router.get("/")
def get_all_transaksi(db: Session = Depends(get_db)):
    return db.query(models.Transaksi).all()

@router.post("/")
def buat_transaksi(transaksi: schemas.TransaksiCreate, db: Session = Depends(get_db)):
    new_trx = models.Transaksi(**transaksi.dict(), sync_status="pending")
    db.add(new_trx)
    db.commit()
    db.refresh(new_trx)
    return new_trx