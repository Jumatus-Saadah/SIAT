from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/sync", tags=["Sinkronisasi"])

@router.post("/")
def sinkronisasi(data: schemas.SyncRequest, db: Session = Depends(get_db)):
    berhasil = 0
    for trx in data.data_transaksi:
        new_trx = models.Transaksi(**trx.dict(), sync_status="synced")
        db.add(new_trx)
        berhasil += 1
    log = models.SyncLog(id_cabang=data.id_cabang, status="success", keterangan=f"{berhasil} transaksi berhasil disinkronkan")
    db.add(log)
    db.commit()
    return {"message": f"{berhasil} transaksi berhasil disinkronkan"}