"""
Sesi 4 - Introduction to Machine Learning
Narasumber : Taniza Tajuddin (Universiti Teknologi MARA)
Studi Kasus: Prediksi kelulusan tepat waktu mahasiswa
             (Decision Tree vs K-Nearest Neighbors)

Alur ML: data -> split train/test -> latih model -> evaluasi -> prediksi baru.
(Data simulasi.)
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, accuracy_score

os.makedirs("output", exist_ok=True)
rng = np.random.default_rng(7)
n = 500

data = pd.DataFrame({
    "ipk": rng.normal(3.1, 0.45, n).clip(1.8, 4.0),
    "kehadiran_persen": rng.normal(85, 10, n).clip(40, 100),
    "sks_per_semester": rng.integers(14, 25, n),
    "jam_belajar_per_minggu": rng.normal(12, 5, n).clip(0, 35),
    "aktif_organisasi": rng.integers(0, 2, n),
})
skor = (
    (data.ipk - 3.0) * 2.5
    + (data.kehadiran_persen - 80) / 10
    + (data.jam_belajar_per_minggu - 10) / 8
    - data.aktif_organisasi * 0.2
    + rng.normal(0, 0.8, n)
)
data["lulus_tepat_waktu"] = (skor > 0).astype(int)

X, y = data.drop(columns="lulus_tepat_waktu"), data["lulus_tepat_waktu"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

modelnya = {
    "Decision Tree": DecisionTreeClassifier(max_depth=4, random_state=42),
    "KNN (k=7)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7)),
}

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
terbaik, akurasi_terbaik = None, 0
for ax, (nama, m) in zip(axes, modelnya.items()):
    m.fit(X_tr, y_tr)
    pred = m.predict(X_te)
    acc = accuracy_score(y_te, pred)
    print(f"\n===== {nama} | akurasi {acc:.2%} =====")
    print(classification_report(y_te, pred, target_names=["Tidak", "Tepat waktu"]))
    ConfusionMatrixDisplay.from_predictions(y_te, pred, ax=ax, colorbar=False)
    ax.set_title(nama)
    if acc > akurasi_terbaik:
        terbaik, akurasi_terbaik = (nama, m), acc
plt.tight_layout(); plt.savefig("output/04_confusion_matrix.png", dpi=120)

# Prediksi mahasiswa baru memakai model terbaik
nama_m, m = terbaik
baru = pd.DataFrame([
    {"ipk": 3.6, "kehadiran_persen": 95, "sks_per_semester": 21, "jam_belajar_per_minggu": 18, "aktif_organisasi": 1},
    {"ipk": 2.4, "kehadiran_persen": 60, "sks_per_semester": 16, "jam_belajar_per_minggu": 4, "aktif_organisasi": 0},
])
print(f"\nPrediksi mahasiswa baru memakai {nama_m}:")
for i, (p, pr) in enumerate(zip(m.predict(baru), m.predict_proba(baru)[:, 1]), 1):
    print(f"  Mahasiswa {i}: {'Tepat waktu' if p else 'Berisiko terlambat'} (prob {pr:.0%})")

if hasattr(m, "feature_importances_"):
    print("\nPentingnya fitur:")
    print(pd.Series(m.feature_importances_, index=X.columns).sort_values(ascending=False).round(3))
