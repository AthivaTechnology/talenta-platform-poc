from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api import auth, clients, tickettailor, dashboard, site, checkout

app = FastAPI(
    title="Talenta Admin API",
    description="Multi-tenant ticketing platform backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(tickettailor.router)
app.include_router(dashboard.router)
app.include_router(site.router)
app.include_router(checkout.router)


@app.get("/", tags=["Health"])
def root():
    # Check for critical environment variables without exposing their values
    diagnostics = {
        "status": "ok",
        "service": "Talenta Backend",
        "environment": {
            "DATABASE_URL": "Set" if settings.DATABASE_URL and "localhost" not in settings.DATABASE_URL else "MISSING or LOCALHOST",
            "STRIPE_KEY": "Set" if settings.STRIPE_SECRET_KEY else "MISSING",
            "SECRET_KEY": "Set" if settings.SECRET_KEY and "your-super-secret" not in settings.SECRET_KEY else "DEFAULT or MISSING",
            "APP_ENV": settings.APP_ENV
        }
    }
    
    # If any critical config is missing, return a warning
    if "MISSING" in str(diagnostics["environment"]) or "LOCALHOST" in str(diagnostics["environment"]):
        diagnostics["status"] = "warning"
        diagnostics["message"] = "Some environment variables are missing or incorrectly set for production."
        
    return diagnostics
