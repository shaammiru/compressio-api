from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from router import text, image, audio, video
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(text.router, prefix="/text", tags=["text"])
app.include_router(image.router, prefix="/image", tags=["image"])
app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(video.router, prefix="/video", tags=["video"])


@app.get("/favicon.ico")
async def favicon():
    return RedirectResponse("/static/favicon.png")
