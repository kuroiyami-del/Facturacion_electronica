from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, clients, invoices, products, dashboard

# Crear todas las tablas al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Facturación Electrónica Colombia",
    description="Backend para facturación electrónica según normativa DIAN",
    version="1.0.0",
)

# CORS — permite que React (en localhost:5173 o 3000) hable con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(invoices.router)
app.include_router(products.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "API Facturación Electrónica activa", "docs": "/docs"}
