from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from app.database import create_tables
from app.routes import auth, mannequin, garment

# Crear directoris necessaris
os.makedirs("static/images", exist_ok=True)

# Crear taules de la base de dades
create_tables()

# Inicialitzar FastAPI
app = FastAPI(
    title="FittSee MVP API",
    description="API per provar roba sobre maniquins personalitzats",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producció, especificar dominis concrets
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Muntar fitxers estàtics
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incloure rutes
app.include_router(auth.router)
app.include_router(mannequin.router)
app.include_router(garment.router)

# Ruta de benvinguda
@app.get("/")
def read_root():
    return {
        "message": "Welcome to FittSee MVP API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "mannequin": "/mannequin", 
            "garment": "/garment",
            "docs": "/docs",
            "static_files": "/static"
        }
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "fittsee-api"}

# Exception handler global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)