from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.conversation import router as conversation_router

app = FastAPI(
    title="Personalized Networking Assistant API",
    description="AI-powered networking conversation starter generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router, prefix="/api")

@app.get("/")
async def health_check():
    return {"status": "healthy", "message": "Personalized Networking Assistant API is running"}