from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import obat, transaksi, inventaris, sync, cabang
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIAT - Sistem Informasi Apotek Terdistribusi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(obat.router)
app.include_router(transaksi.router)
app.include_router(inventaris.router)
app.include_router(sync.router)
app.include_router(cabang.router)

@app.get("/")
def root():
    return {"message": "SIAT Backend berjalan!"}