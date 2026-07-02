from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Cabang(Base):
    __tablename__ = "cabang"
    id_cabang = Column(Integer, primary_key=True, index=True)
    nama_cabang = Column(String(100), nullable=False)
    alamat = Column(String(255))
    zona_waktu = Column(String(10), default="WIB")

class Obat(Base):
    __tablename__ = "obat"
    id_obat = Column(Integer, primary_key=True, index=True)
    nama_obat = Column(String(100), nullable=False)
    harga = Column(Integer, nullable=False)
    stok_minimal = Column(Integer, default=10)
    updated_at = Column(DateTime, server_default=func.now())

class Inventaris(Base):
    __tablename__ = "inventaris"
    id_inventaris = Column(Integer, primary_key=True, index=True)
    id_cabang = Column(Integer, ForeignKey("cabang.id_cabang"))
    id_obat = Column(Integer, ForeignKey("obat.id_obat"))
    jumlah_stok = Column(Integer, default=0)
    updated_at = Column(DateTime, server_default=func.now())

class Transaksi(Base):
    __tablename__ = "transaksi"
    id_transaksi = Column(Integer, primary_key=True, index=True)
    id_cabang = Column(Integer, ForeignKey("cabang.id_cabang"))
    id_obat = Column(Integer, ForeignKey("obat.id_obat"))
    jumlah = Column(Integer, nullable=False)
    total_harga = Column(Integer, nullable=False)
    tanggal = Column(DateTime, server_default=func.now())
    sync_status = Column(String(20), default="pending")

class SyncLog(Base):
    __tablename__ = "sync_log"
    id_log = Column(Integer, primary_key=True, index=True)
    id_cabang = Column(Integer, ForeignKey("cabang.id_cabang"))
    waktu_sync = Column(DateTime, server_default=func.now())
    status = Column(String(20))
    keterangan = Column(Text)

class User(Base):
    __tablename__ = "users"
    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # kasir / manajer
    id_cabang = Column(Integer, ForeignKey("cabang.id_cabang"), nullable=True)