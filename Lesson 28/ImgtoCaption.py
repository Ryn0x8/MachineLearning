import torch
from PIL import Image
from transformers import (
    VisionEncoderDecoderModel,
    ViTImageProcessor,
    AutoTokenizer
)

# ----------------------------
# CONFIG
# ----------------------------
MODEL_ID = "nlpconnect/vit-gpt2-image-captioning"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MAX_LENGTH = 30
NUM_BEAMS = 5

GEN_KWARGS = {
    "max_length": MAX_LENGTH,
    "num_beams": NUM_BEAMS,
    "repetition_penalty": 1.2,
    "early_stopping": True
}

# ----------------------------
# LOAD MODEL & PROCESSORS
# ----------------------------
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
feature_extractor = ViTImageProcessor.from_pretrained(MODEL_ID)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_ID)

# GPT-2 token fix
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.eos_token_id
model.config.eos_token_id = tokenizer.eos_token_id

model.to(DEVICE)
model.eval()

# ----------------------------
# PREDICTION FUNCTION
# ----------------------------
def predict_step(image_paths):
    images = []

    for path in image_paths:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    pixel_values = feature_extractor(
        images=images,
        return_tensors="pt"
    ).pixel_values.to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(pixel_values, **GEN_KWARGS)

    captions = tokenizer.batch_decode(
        output_ids,
        skip_special_tokens=True
    )

    return [c.strip() for c in captions]

# ----------------------------
# MAIN
# ----------------------------
def main():
    images = ["image.png"]  # <-- replace with your image paths
    captions = predict_step(images)

    for img, cap in zip(images, captions):
        print(f"Image: {img}")
        print(f"Caption: {cap}")
        print("-" * 40)

if __name__ == "__main__":
    main()
