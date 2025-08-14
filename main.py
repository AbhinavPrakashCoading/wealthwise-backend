from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import engine, Base
from .core.config import get_settings
from .routers import auth as auth_router
from .routers import groups as groups_router
from .routers import payments as payments_router
from .routers import integrations as integrations_router
from .routers import wealth as wealth_router

Base.metadata.create_all(bind=engine)

settings = get_settings()
app = FastAPI(title="WealthWise API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(groups_router.router)
app.include_router(payments_router.router)
app.include_router(integrations_router.router)
app.include_router(wealth_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}
