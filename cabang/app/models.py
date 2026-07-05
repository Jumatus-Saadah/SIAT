from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Transaksi(Base):
    __tablename__ = "transaksi"
    id_transaksi = Column(Integer, primary_key=True, index=True)
    id_obat = Column(Integer, nullable=False)
    jumlah = Column(Integer, nullable=False)
    total_harga = Column(Integer, nullable=False)
    tanggal = Column(DateTime, server_default=func.now())
    sync_status = Column(String(20), default="pending")