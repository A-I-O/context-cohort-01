# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import magazine, plan, subscription, user
from .routers import magazines, plans, subscriptions, users

# Create database tables
magazine.Base.metadata.create_all(bind=engine)
plan.Base.metadata.create_all(bind=engine)
subscription.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Magazine Subscription Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(magazines.router, prefix="/api/magazines", tags=["magazines"])
app.include_router(plans.router, prefix="/api/plans", tags=["plans"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["subscriptions"])

@app.get("/")
async def root():
    return {"message": "Welcome to Magazine Subscription Service"}

# src/main.py

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(magazines.router, prefix="/magazines", tags=["magazines"])
app.include_router(plans.router, prefix="/plans", tags=["plans"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
