from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agent import InstagramAgent
from app.utils.image_creator import create_image_from_text

import os
import uuid

app = FastAPI()
agent = InstagramAgent()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_TOKEN = "Agent007"

@app.get("/")
def get_index():
    return FileResponse('static/index.html')

@app.post("/post_to_instagram/")
async def post_to_instagram(
    username: str = Form(...),
    password: str = Form(...),
    text: str = Form(...),
    caption: str = Form(...),
    token: str = Form(...)
):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        print("[INFO] Received submission with text:", text)

        if not text:
            print("[ERROR] No text received!")
            return {"status": "error", "message": "No text provided"}

        temp_filename = f"{UPLOAD_DIR}/{uuid.uuid4().hex}.png"
        print(f"[INFO] About to generate image at: {temp_filename}")

        create_image_from_text(text, temp_filename)
        print("[INFO] Image generated successfully.")

        result = agent.post_photo(username, password, temp_filename, caption)
        print("[INFO] Instagram post result:", result)

        os.remove(temp_filename)
        print("[INFO] Temporary file removed.")

        return {"status": "success", "message": "Posted successfully"}

    except Exception as e:
        print(f"[ERROR] Unhandled exception: {e}")
        return {"status": "error", "message": str(e)}
