from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import transaksi, sync

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIAT - Server Cabang")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transaksi.router)
app.include_router(sync.router)

@app.get("/")
def root():
    return {"message": "SIAT Server Cabang berjalan!"}