from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/inventaris", tags=["Inventaris"])

@router.get("/stok-global")
def cek_stok_global(nama_obat: str, db: Session = Depends(get_db)):
    obat = db.query(models.Obat).filter(models.Obat.nama_obat.ilike(f"%{nama_obat}%")).first()
    if not obat:
        return {"message": "Obat tidak ditemukan"}
    stok = db.query(models.Inventaris, models.Cabang)\
        .join(models.Cabang, models.Inventaris.id_cabang == models.Cabang.id_cabang)\
        .filter(models.Inventaris.id_obat == obat.id_obat).all()
    return [{"cabang": s.Cabang.nama_cabang, "alamat": s.Cabang.alamat, "stok": s.Inventaris.jumlah_stok} for s in stok]

@router.post("/")
def tambah_inventaris(inv: schemas.InventarisCreate, db: Session = Depends(get_db)):
    new_inv = models.Inventaris(**inv.dict())
    db.add(new_inv)
    db.commit()
    db.refresh(new_inv)
    return new_inv