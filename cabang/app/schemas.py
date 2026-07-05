from pydantic import BaseModel

class ObatCreate(BaseModel):
    nama_obat: str
    harga: int
    stok_minimal: int = 10

class TransaksiCreate(BaseModel):
    id_obat: int
    jumlah: int
    total_harga: int