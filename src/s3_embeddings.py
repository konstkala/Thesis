import os
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm

import torch
from torchvision import models, transforms

# -------------------------
# Config
# -------------------------
DATA_DIR = "../data/processed"
OUT_DIR = "../data/embeddings"
OUT_DIR = os.path.abspath(OUT_DIR)

os.makedirs(OUT_DIR, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------
# Model
# -------------------------
model = models.resnet18(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # remove classifier
model.to(DEVICE)
model.eval()

# -------------------------
# Preprocessing
# -------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.485, 0.485],
        std=[0.229, 0.229, 0.229]
    )
])

# -------------------------
# Embedding extraction
# -------------------------
X = []
meta = []

subjects = sorted(os.listdir(DATA_DIR))

for subject in subjects:
    subject_path = os.path.join(DATA_DIR, subject)
    if not os.path.isdir(subject_path):
        continue

    images = sorted(os.listdir(subject_path))

    for img_name in tqdm(images, desc=f"{subject}"):
        img_path = os.path.join(subject_path, img_name)

        img = Image.open(img_path).convert("RGB")
        x = transform(img).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            emb = model(x).squeeze().cpu().numpy()

        X.append(emb)
        meta.append({
            "subject": subject,
            "filename": img_name
        })

# -------------------------
# Save outputs
# -------------------------
X = np.stack(X)
np.save(os.path.join(OUT_DIR, "X.npy"), X)
pd.DataFrame(meta).to_csv(os.path.join(OUT_DIR, "meta.csv"), index=False)

print("Embeddings saved.")
print("X shape:", X.shape)