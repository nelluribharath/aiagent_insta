from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .agent import InstagramAgent, generate_image_from_text
import os
import uuid

app = FastAPI()
agent = InstagramAgent()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_TOKEN = "MY_SUPER_SECRET_TOKEN"

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
        temp_filename = f"{UPLOAD_DIR}/{uuid.uuid4().hex}.png"
        generate_image_from_text(text, temp_filename)

        result = agent.post_photo(username, password, temp_filename, caption)
        os.remove(temp_filename)

        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
