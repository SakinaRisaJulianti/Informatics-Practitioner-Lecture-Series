"""
Sesi 6 - Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI
Narasumber : Bart Slagter (Wageningen University & Research)
Studi Kasus: Klasifikasi penyebab deforestasi di Sumatra dari fitur citra satelit

Fitur (simulasi):
  - delta_ndvi : penurunan indeks vegetasi (makin negatif = vegetasi hilang)
  - delta_nbr  : penurunan Normalized Burn Ratio (sangat negatif = bekas terbakar)
  - jarak_jalan_km, luas_ha, bentuk_kompak (0-1; 1 = bentuk blok teratur)
Kelas penyebab: Kebakaran, Perkebunan, Infrastruktur, Perambahan kecil
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

os.makedirs("output", exist_ok=True)
rng = np.random.default_rng(11)


def buat(n, kelas, d_ndvi, d_nbr, jarak, luas, kompak):
    return pd.DataFrame({
        "delta_ndvi": rng.normal(*d_ndvi, n),
        "delta_nbr": rng.normal(*d_nbr, n),
        "jarak_jalan_km": np.abs(rng.normal(*jarak, n)),
        "luas_ha": np.abs(rng.normal(*luas, n)),
        "bentuk_kompak": np.clip(rng.normal(*kompak, n), 0, 1),
        "penyebab": kelas,
    })


data = pd.concat([
    buat(250, "Kebakaran",        (-0.45, 0.10), (-0.60, 0.12), (6, 3), (60, 30), (0.35, 0.15)),
    buat(250, "Perkebunan",       (-0.55, 0.10), (-0.10, 0.08), (4, 2), (120, 40), (0.85, 0.08)),
    buat(250, "Infrastruktur",    (-0.35, 0.10), (-0.08, 0.06), (0.8, 0.5), (15, 8), (0.30, 0.12)),
    buat(250, "Perambahan kecil", (-0.30, 0.10), (-0.12, 0.07), (3, 1.5), (4, 2), (0.55, 0.15)),
], ignore_index=True).sample(frac=1, random_state=1).reset_index(drop=True)

X, y = data.drop(columns="penyebab"), data["penyebab"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_tr, y_tr)
pred = model.predict(X_te)
print(classification_report(y_te, pred))

fig, ax = plt.subplots(1, 2, figsize=(13, 5))
ConfusionMatrixDisplay.from_predictions(y_te, pred, ax=ax[0], xticks_rotation=30, colorbar=False)
ax[0].set_title("Confusion Matrix")
imp = pd.Series(model.feature_importances_, index=X.columns).sort_values()
imp.plot.barh(ax=ax[1]); ax[1].set_title("Pentingnya Fitur")
plt.tight_layout(); plt.savefig("output/06_deforestasi.png", dpi=120)

# Peringatan (alert) baru yang belum diketahui penyebabnya
alert_baru = pd.DataFrame([
    {"delta_ndvi": -0.50, "delta_nbr": -0.62, "jarak_jalan_km": 7.0, "luas_ha": 55, "bentuk_kompak": 0.30},
    {"delta_ndvi": -0.58, "delta_nbr": -0.09, "jarak_jalan_km": 4.5, "luas_ha": 130, "bentuk_kompak": 0.88},
    {"delta_ndvi": -0.33, "delta_nbr": -0.07, "jarak_jalan_km": 0.5, "luas_ha": 12, "bentuk_kompak": 0.28},
])
hasil = model.predict(alert_baru)
proba = model.predict_proba(alert_baru).max(axis=1)
print("\nPrediksi alert baru:")
for i, (h, p) in enumerate(zip(hasil, proba), 1):
    print(f"  Alert {i}: {h} (keyakinan {p:.0%})")
