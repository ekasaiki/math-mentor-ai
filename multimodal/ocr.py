import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image_np = np.array(image)

    results = reader.readtext(image_np)

    texts = []
    confs = []

    for _, text, conf in results:
        texts.append(text)
        confs.append(conf)

    final_text = " ".join(texts)
    confidence = sum(confs) / len(confs) if confs else 0.0

    return final_text, round(confidence, 2)
