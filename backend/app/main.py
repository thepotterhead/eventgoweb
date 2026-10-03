import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from .api import api_router

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
FRONTEND_PUBLIC_DIR = os.path.join(BASE_DIR, "frontend", "public")

app = FastAPI(
    title="Funobotz Personalized STEM Learning Chatbot API",
    description="Grounded, personalized STEM learning chatbot backend for Funobotz Paper Robotics.",
    version="1.0.0"
)

# Enable CORS for local dev and embeddable widget access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Serve main application single-page app
@app.get("/")
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)

# Serve widget.js Web Component
@app.get("/widget.js")
def read_widget():
    widget_path = os.path.join(FRONTEND_PUBLIC_DIR, "widget.js")
    return FileResponse(widget_path, media_type="application/javascript")

# Serve /demo/embed.html store integration page
@app.get("/demo/embed.html")
def read_embed_demo():
    embed_path = os.path.join(FRONTEND_PUBLIC_DIR, "demo", "embed.html")
    return FileResponse(embed_path, media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
