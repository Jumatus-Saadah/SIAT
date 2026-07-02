from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/obat", tags=["Obat"])

@router.get("/")
def get_all_obat(db: Session = Depends(get_db)):
    return db.query(models.Obat).all()

@router.post("/")
def tambah_obat(obat: schemas.ObatCreate, db: Session = Depends(get_db)):
    new_obat = models.Obat(**obat.dict())
    db.add(new_obat)
    db.commit()
    db.refresh(new_obat)
    return new_obat

@router.delete("/{id_obat}")
def hapus_obat(id_obat: int, db: Session = Depends(get_db)):
    obat = db.query(models.Obat).filter(models.Obat.id_obat == id_obat).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    db.delete(obat)
    db.commit()
    return {"message": f"Obat {obat.nama_obat} berhasil dihapus"}