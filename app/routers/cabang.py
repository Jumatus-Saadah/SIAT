from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/cabang", tags=["Cabang"])

@router.get("/")
def get_all_cabang(db: Session = Depends(get_db)):
    return db.query(models.Cabang).all()

@router.post("/")
def tambah_cabang(cabang: schemas.CabangCreate, db: Session = Depends(get_db)):
    new_cabang = models.Cabang(**cabang.dict())
    db.add(new_cabang)
    db.commit()
    db.refresh(new_cabang)
    return new_cabang

@router.delete("/{id_cabang}")
def hapus_cabang(id_cabang: int, db: Session = Depends(get_db)):
    cabang = db.query(models.Cabang).filter(models.Cabang.id_cabang == id_cabang).first()
    if not cabang:
        raise HTTPException(status_code=404, detail="Cabang tidak ditemukan")
    db.delete(cabang)
    db.commit()
    return {"message": f"Cabang {cabang.nama_cabang} berhasil dihapus"}