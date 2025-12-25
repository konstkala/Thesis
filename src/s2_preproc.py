import os
import cv2
import matplotlib.pyplot as plt

# Paths
INPUT_FOLDER = "../data/raw/subject001"
OUTPUT_FOLDER = "../data/processed/subject001"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Βρόχος σε όλες τις εικόνες του φακέλου
for fname in os.listdir(INPUT_FOLDER):
    input_path = os.path.join(INPUT_FOLDER, fname)
    output_path = os.path.join(OUTPUT_FOLDER, fname)
    
    # 1️⃣ Φόρτωση εικόνας σε grayscale
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Could not read {input_path}")
        continue

    # 2️⃣ CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_clahe = clahe.apply(img)

    # 3️⃣ Κανονικοποίηση σε 0-1
    img_norm = img_clahe / 255.0

    # 4️⃣ Αποθήκευση (σε 0-255 για PNG)
    cv2.imwrite(output_path, (img_norm*255).astype("uint8"))

    # 5️⃣ Οπτικοποίηση (προαιρετικό)
    plt.figure(figsize=(8,4))
    plt.subplot(1,2,1)
    plt.imshow(img, cmap='gray')
    plt.title("Original")
    plt.axis('off')

    plt.subplot(1,2,2)
    plt.imshow(img_clahe, cmap='gray')
    plt.title("CLAHE")
    plt.axis('off')
    plt.show()
