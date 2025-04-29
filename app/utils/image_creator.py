from diffusers import StableDiffusionPipeline
import torch
import os

# Load model safely for CPU (no GPU)
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float32  # ✅ Use float32 for CPU
).to("cpu")  # ✅ Run on CPU

def create_image_from_text(prompt, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"[DEBUG] Generating AI image for prompt: {prompt}")
    
    image = pipe(prompt, num_inference_steps=20).images[0]  # ✅ 20 steps = faster
    image.save(filename)
    print(f"[DEBUG] Image saved at: {filename}")
