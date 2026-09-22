import uvicorn
import socket
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.api import api_router
from contextlib import asynccontextmanager
from app.config.config import settings
from app.utils.first_user import create_super_admin, create_sumit_user

# Create uploads directory if it doesn't exist
os.makedirs("app/uploads", exist_ok=True)
os.makedirs("app/uploads/gallery", exist_ok=True)
os.makedirs("app/uploads/gallery/images", exist_ok=True)
os.makedirs("app/uploads/gallery/videos", exist_ok=True)
os.makedirs("app/uploads/teachers", exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create super admin user if not exists
    create_super_admin()
    # Create sumit user if not exists
    create_sumit_user()
    
    ip = get_local_ip()
    port = 8000

    print("🚀 FastAPI started")
    print(f"👉 Local   : http://127.0.0.1:{port}/docs")
    print(f"👉 Network : http://{ip}:{port}/docs")

    yield

    print("🛑 Web Server Stopped")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Configure CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],  # Angular default port
    allow_origins=[
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://academy-front-five.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (uploaded images)
app.mount("/app/uploads", StaticFiles(directory="app/uploads"), name="uploads")

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
