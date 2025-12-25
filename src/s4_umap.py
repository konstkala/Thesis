import numpy as np
import pandas as pd
import umap
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------
# Paths
# -------------------------
EMB_PATH = Path("../data/embeddings")
OUT_PATH = Path("../data/umap")
OUT_PATH.mkdir(parents=True, exist_ok=True)

# -------------------------
# Load data
# -------------------------
X = np.load(EMB_PATH / "X.npy")
meta = pd.read_csv(EMB_PATH / "meta.csv")

print("Loaded X shape:", X.shape)
print("Subjects:", meta["subject"].nunique())

# -------------------------
# UMAP
# -------------------------
reducer = umap.UMAP(
    n_neighbors=10,      # καλό για 10 subjects
    min_dist=0.1,
    n_components=2,
    metric="euclidean",
    random_state=42
)

X_umap = reducer.fit_transform(X)

# -------------------------
# Save
# -------------------------
np.save(OUT_PATH / "X_umap.npy", X_umap)

# -------------------------
# Plot
# -------------------------
plt.figure(figsize=(8, 6))

subjects = meta["subject"].astype("category").cat.codes
scatter = plt.scatter(
    X_umap[:, 0],
    X_umap[:, 1],
    c=subjects,
    cmap="tab10",
    s=50
)

plt.title("UMAP of Fingerprint CNN Embeddings")
plt.xlabel("UMAP-1")
plt.ylabel("UMAP-2")
plt.colorbar(scatter, label="Subject ID")
plt.tight_layout()

plt.savefig(OUT_PATH / "umap_plot.png", dpi=300)
plt.show()