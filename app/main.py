from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views import user, auth 
app = FastAPI(
    title="FastAPI MongoDB Auth App",
    version="1.0.0",
    description="A FastAPI app using MongoDB Atlas with JWT auth and MVC structure.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB app is running."}
