from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CabangCreate(BaseModel):
    nama_cabang: str
    alamat: str
    zona_waktu: str = "WIB"

class ObatCreate(BaseModel):
    nama_obat: str
    harga: int
    stok_minimal: int = 10

class TransaksiCreate(BaseModel):
    id_cabang: int
    id_obat: int
    jumlah: int
    total_harga: int

class InventarisCreate(BaseModel):
    id_cabang: int
    id_obat: int
    jumlah_stok: int

class SyncRequest(BaseModel):
    id_cabang: int
    data_transaksi: list[TransaksiCreate]