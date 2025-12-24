import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

import torch
from torchvision import models, transforms

# Paths
INPUT_FOLDER = "../data/processed"  # περιέχει subfolders ανά subject
EMB_PATH = "X.npy"
META_PATH = "meta.csv"

# Device
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# CNN model (ResNet18 χωρίς το classification layer)
def get_cnn_model(device=DEVICE):
    model = models.resnet18(pretrained=True)
    model = torch.nn.Sequential(*(list(model.children())[:-1]))  # αφαιρούμε τον classifier
    model.to(device).eval()
    return model

# Προεπεξεργασία εικόνων για ResNet
preprocess_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.485,0.485],[0.229,0.229,0.229])
])

# Εξαγωγή embedding
def extract_embedding(img_gray, model, device=DEVICE):
    if len(img_gray.shape)==2:  # grayscale -> RGB
        img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    else:
        img = img_gray
    x = preprocess_transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = model(x).squeeze().cpu().numpy()
    return emb

# Εκτέλεση pipeline
X = []
meta = []

subjects = sorted([d for d in os.listdir(INPUT_FOLDER) if os.path.isdir(os.path.join(INPUT_FOLDER,d))])
print("Subjects found:", subjects)

for subject in subjects:
    subj_dir = os.path.join(INPUT_FOLDER, subject)
    images = sorted([f for f in os.listdir(subj_dir) if f.lower().endswith(('.png','.jpg','.jpeg','.tif'))])
    if not images:
        print(f"No images found for {subject}, skipping...")
        continue

    for fname in tqdm(images, desc=f"Subject {subject}"):
        path = os.path.join(subj_dir, fname)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Could not read {path}, skipping...")
            continue
        emb = extract_embedding(img, get_cnn_model())
        X.append(emb)
        meta.append({'filename': path, 'subject': subject})

if not X:
    raise ValueError("No embeddings were extracted! Check your folders and image files.")

# Αποθήκευση embeddings και metadata
X = np.stack(X)
np.save(EMB_PATH, X)
pd.DataFrame(meta).to_csv(META_PATH, index=False)

print(f"Saved {len(X)} embeddings to {EMB_PATH}")
print(f"Saved metadata to {META_PATH}")
