from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import requests
import os

router = APIRouter(prefix="/sync", tags=["Sinkronisasi Cabang"])

PUSAT_URL = os.getenv("PUSAT_URL", "http://localhost:8000")
ID_CABANG = int(os.getenv("ID_CABANG", "1"))

@router.post("/")
def sinkronisasi(db: Session = Depends(get_db)):
    pending = db.query(models.Transaksi).filter(
        models.Transaksi.sync_status == "pending"
    ).all()

    if not pending:
        return {"message": "Tidak ada data yang perlu disinkronkan"}

    data_kirim = []
    for trx in pending:
        data_kirim.append({
            "id_cabang": ID_CABANG,
            "id_obat": trx.id_obat,
            "jumlah": trx.jumlah,
            "total_harga": trx.total_harga
        })

    try:
        response = requests.post(
            f"{PUSAT_URL}/sync/",
            json={"id_cabang": ID_CABANG, "data_transaksi": data_kirim}
        )
        if response.status_code == 200:
            for trx in pending:
                trx.sync_status = "synced"
            db.commit()
            return {"message": f"{len(pending)} transaksi berhasil dikirim ke pusat"}
        else:
            return {"message": "Gagal kirim ke pusat", "detail": response.text}
    except Exception as e:
        return {"message": "Server pusat tidak bisa diakses", "error": str(e)}