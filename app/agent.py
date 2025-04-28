from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont

def generate_image_from_text(text, filename):
    img = Image.new('RGB', (1080, 1080), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    lines = []
    words = text.split()
    line = ""
    for word in words:
        if len(line + word) < 20:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y_text = 200
    for line in lines:
        width, height = draw.textsize(line, font=font)
        draw.text(((1080 - width) / 2, y_text), line, font=font, fill=(0, 0, 0))
        y_text += height + 20

    img.save(filename)

class InstagramAgent:
    def __init__(self):
        self.sessions = {}

    def login(self, username, password):
        if username in self.sessions:
            return self.sessions[username]

        cl = Client()
        cl.login(username, password)
        self.sessions[username] = cl
        return cl

    def post_photo(self, username, password, photo_path, caption):
        client = self.login(username, password)
        media = client.photo_upload(photo_path, caption)
        return f"Post uploaded successfully with media id: {media.pk}"
