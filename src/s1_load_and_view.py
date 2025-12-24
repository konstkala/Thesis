# step1_load_and_view.py

from PIL import Image
import matplotlib.pyplot as plt

# Path προς την εικόνα
IMAGE_PATH = "../data/raw/subject001/101_1.png"  # ή .tif

# Φόρτωση εικόνας
img = Image.open(IMAGE_PATH)

# Εμφάνιση εικόνας
plt.figure(figsize=(4,4))
plt.imshow(img, cmap='gray')
plt.title("Fingerprint Image")
plt.axis('off')
plt.show()
