"""
Sesi 1 - Make Sense of Data with Analysis and AI
Narasumber : Andria Arisal (BRIN)
Studi Kasus: Analisis penjualan toko kopi kampus dan prediksi penjualan bulan depan

Tiga tahap analisis data:
  1. Deskriptif  -> apa yang terjadi?
  2. Diagnostik  -> mengapa terjadi?
  3. Prediktif   -> apa yang akan terjadi?
(Data adalah simulasi untuk keperluan pembelajaran.)
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

os.makedirs("output", exist_ok=True)
rng = np.random.default_rng(42)

# ---------- Data simulasi: 12 bulan x 3 produk ----------
bulan = pd.date_range("2025-11-01", periods=12, freq="MS")
produk = {"Kopi Susu": 1200, "Americano": 700, "Teh Tarik": 900}
rows = []
for i, b in enumerate(bulan):
    for p, base in produk.items():
        promo = rng.choice([0, 1], p=[0.6, 0.4])          # ada promo atau tidak
        qty = int(base + i * 25 + promo * 180 + rng.normal(0, 60))
        harga = {"Kopi Susu": 18000, "Americano": 15000, "Teh Tarik": 12000}[p]
        rows.append([b, p, promo, qty, qty * harga])
df = pd.DataFrame(rows, columns=["bulan", "produk", "promo", "qty", "omzet"])

# Simulasi data kosong lalu diisi median (data cleaning)
df.loc[df.sample(3, random_state=1).index, "qty"] = np.nan
df["qty"] = df.groupby("produk")["qty"].transform(lambda s: s.fillna(s.median()))

# ---------- 1. Deskriptif ----------
print("=== ANALISIS DESKRIPTIF ===")
print(df.groupby("produk")[["qty", "omzet"]].agg(["mean", "sum"]).round(0))
bulanan = df.groupby("bulan")["omzet"].sum()

# ---------- 2. Diagnostik ----------
print("\n=== ANALISIS DIAGNOSTIK: pengaruh promo ===")
efek = df.groupby(["produk", "promo"])["qty"].mean().unstack()
efek["kenaikan_%"] = ((efek[1] - efek[0]) / efek[0] * 100).round(1)
print(efek.round(1))

# ---------- 3. Prediktif ----------
X = np.arange(len(bulanan)).reshape(-1, 1)
y = bulanan.values
model = LinearRegression().fit(X, y)
prediksi = model.predict([[len(bulanan)]])[0]
print(f"\n=== PREDIKSI === Omzet bulan berikutnya: Rp {prediksi:,.0f}")
print(f"R^2 model: {model.score(X, y):.3f}")

# ---------- Visualisasi ----------
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(bulanan.index, bulanan.values / 1e6, marker="o", label="Aktual")
ax[0].plot(bulanan.index, model.predict(X) / 1e6, "--", label="Tren regresi")
ax[0].set_title("Omzet Bulanan (juta Rp)")
ax[0].legend(); ax[0].tick_params(axis="x", rotation=45)
efek[[0, 1]].plot.bar(ax=ax[1])
ax[1].set_title("Rata-rata Qty: tanpa promo (0) vs promo (1)")
ax[1].tick_params(axis="x", rotation=0)
plt.tight_layout()
plt.savefig("output/01_analisis_penjualan.png", dpi=120)
print("Grafik disimpan di output/01_analisis_penjualan.png")
