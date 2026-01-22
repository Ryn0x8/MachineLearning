import os, mimetypes, io, time, random, requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import HF_API

model = "facebook/detr-resnet-50"
API = f"https://router.huggingface.co/hf-inference/models/{model}"
ALLOWED, MAX_MB = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}, 8
EMOJI = {
  "person":"🧑🏻","car":"🚗","truck":"🚚","bus":"🚌","bicycle":"🚲","motorcycle":"🏍️",
  "dog":"🐕","cat":"🐈","bird":"🐦","horse":"🐎","sheep":"🐑","cow":"🐄","bear":"🐻",
  "giraffe":"🦒","zebra":"🦓","banana":"🍌","apple":"🍎","orange":"🍊","pizza":"🍕",
  "broccoli":"🥦","book":"📚","laptop":"💻","tv":"📺","bottle":"🍾","cup":"☕"
}

def font(sz = 18):
    for f in ("DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except:
            pass
    return ImageFont.load_default()

def ask_image():
    print("\nPick an image file from this folder to detect: ")
    while True:
        p = input("Image file path: ").strip('"').strip("'").strip()
        if not p or not os.path.isfile(p):
            print("Invalid file path, try again.")
            continue
        if os.path.splitext(p)[1].lower() not in ALLOWED:
            print(f"Unsupported file type, allowed: {', '.join(ALLOWED)}")
            continue
        if os.path.getsize(p)/(1024*1024) > MAX_MB:
            print(f"File too large, max size is {MAX_MB} MB")
            continue
        try:
            img = Image.open(p).verify()
        except:
            print("File is not a valid image, try again.")
            continue
        return p

def infer(path, img_bytes, tries = 8):
    mime , _ = mimetypes.guess_type(path)
    for _ in range(tries):
        if mime and mime.startswith("image/"):
            r = requests.post(API, 
                headers = {"Authorization": f"Bearer {HF_API}", "Content-Type": mime},
                data = img_bytes, timeout = 60
                )
        else:
            r = requests.post(API, 
                headers = {"Authorization": f"Bearer {HF_API}"},
                files = {"inputs": (os.path.basename(path), img_bytes, "application/octet-stream")},
                timeout = 60
                )
        if r.status_code == 200:
            d = r.json()
            if isinstance(d, dict) and "error" in d:
                raise Exception("Inference API Error: " + d["error"])
            if not isinstance(d, list):
                raise Exception("Inference API returned invalid response")
            return d
        if r.status_code == 503:
            print("Model is loading, waiting 5 seconds...")
            time.sleep(5)
            continue
        raise RuntimeError(f"Inference API request failed with status code {r.status_code}: {r.text}")
    raise RuntimeError("Model Warmup Timeout")

def draw(img, dets, thr = 0.5):
    d = ImageDraw.Draw(img);f = font(); counts = {}
    for det in dets[:50]:
        s = float(det.get("score", 0))
        if s<thr:
            continue
        lab = det.get("label", "object"); b  = det.get("box", {})
        x1,y1,x2,y2 = (int(b.get(k, 0)) for k in ("xmin","ymin","xmax","ymax"))
        if not (x2>0 and y2>0):
            x,y,w,h = (int(b.get(k, 0)) for k in ("x","y","w","h"))
            x1,y1,x2,y2 = x,y,x+w,y+h
        color = tuple(random.randint(80, 256) for _ in range(3))
        d.rectangle([x1,y1,x2,y2], outline = color, width = 4)
        txt = f"{EMOJI.get(lab.lower(), '')} {lab}: {s*100:.1f}%"
        bbox = d.textbbox((0,0), txt, font=f)   
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1] + 6
 
        f.size+6
        d.rectangle([(x1+4, max(0, y1-th)), (x1+tw + 8, y1)], fill = color)
        d.text((x1+4, y1-th+3), txt, font = f, fill = (0,0,0))
        counts[lab] = counts.get(lab, 0) + 1
    return counts

def main():
    path = ask_image()
    with open(path, "rb") as f:
        img_bytes = f.read()
    try:
        dets = infer(path, img_bytes)
    except Exception as e:
        return print("Error during inference: " + str(e))
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    counts = draw(img, dets)
    out = f"annotated_{os.path.basename(path)}"
    img.save(out)
    print("Saved: ", out)
    if counts:
        print("I Found: ")
        for k, v in sorted(counts.items(), key = lambda kv: (-kv[1], kv[0])):
            print(f"{EMOJI.get(k.lower(), '')} {k}: {v}")
    else:
        print("No objects detected above the confidence threshold.")

if __name__ == "__main__":
    main()

                                                  



