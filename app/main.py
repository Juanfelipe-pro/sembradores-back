from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, devocionales, usuarios, favoritos, progreso, planes, pagos, push, oauth

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"app": settings.APP_NAME, "status": "running", "version": "2.0"}

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(oauth.router, prefix="/api/oauth", tags=["oauth"])
app.include_router(devocionales.router, prefix="/api/devocionales", tags=["devocionales"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["usuarios"])
app.include_router(favoritos.router, prefix="/api/favoritos", tags=["favoritos"])
app.include_router(progreso.router, prefix="/api/progreso", tags=["progreso"])
app.include_router(planes.router, prefix="/api/planes", tags=["planes"])
app.include_router(pagos.router, prefix="/api/pagos", tags=["pagos"])
app.include_router(push.router, prefix="/api/push", tags=["push"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)