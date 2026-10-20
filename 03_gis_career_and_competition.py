"""
Sesi 3 - Career and Competition in Industrial Era with GIS
Narasumber : Widi Prima Deva (Citycare Property, Selandia Baru)
Studi Kasus: Prioritas pemeriksaan fasilitas publik di Kota Bengkulu
             berdasarkan jarak ke titik rawan banjir (asset management)

Koordinat fasilitas & titik rawan adalah SIMULASI/perkiraan kasar.
Output: peta interaktif HTML + file GeoJSON.
"""
import os
import json
import math
import pandas as pd
import folium

os.makedirs("output", exist_ok=True)

# Titik rawan banjir (simulasi, sekitar Kota Bengkulu)
HAZARD = (-3.7960, 102.2640)
RADIUS_KM = 2.0

aset = pd.DataFrame([
    # nama, jenis, lat, lon, usia (th), kerusakan (0-10)
    ("Jembatan A",      "Jembatan",  -3.7935, 102.2610, 32, 7),
    ("Puskesmas B",     "Kesehatan", -3.8050, 102.2700, 15, 3),
    ("SD Negeri C",     "Sekolah",   -3.7900, 102.2800, 22, 5),
    ("Pasar D",         "Pasar",     -3.7975, 102.2655, 28, 8),
    ("Gorong-gorong E", "Drainase",  -3.8100, 102.2500, 40, 9),
    ("Halte F",         "Transport", -3.8200, 102.2900, 8, 2),
    ("Kantor Kelurahan G", "Kantor", -3.7850, 102.2550, 18, 4),
], columns=["nama", "jenis", "lat", "lon", "usia", "kerusakan"])


def haversine(lat1, lon1, lat2, lon2):
    """Jarak 2 titik di permukaan bumi (km)."""
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


aset["jarak_km"] = aset.apply(lambda r: haversine(r.lat, r.lon, *HAZARD), axis=1).round(2)
aset["di_zona_rawan"] = aset["jarak_km"] <= RADIUS_KM

# Skor prioritas (0-100): kerusakan 50%, usia 25%, kedekatan zona 25%
aset["skor"] = (
    aset["kerusakan"] / 10 * 50
    + (aset["usia"] / 40).clip(upper=1) * 25
    + (1 - (aset["jarak_km"] / RADIUS_KM).clip(upper=1)) * 25
).round(1)
aset = aset.sort_values("skor", ascending=False).reset_index(drop=True)
print(aset[["nama", "jenis", "jarak_km", "di_zona_rawan", "skor"]])


def warna(s):
    return "red" if s >= 65 else "orange" if s >= 45 else "green"


peta = folium.Map(location=HAZARD, zoom_start=13)
folium.Circle(HAZARD, radius=RADIUS_KM * 1000, color="blue", fill=True,
              fill_opacity=0.1, tooltip="Zona rawan banjir").add_to(peta)
folium.Marker(HAZARD, icon=folium.Icon(color="blue", icon="tint", prefix="fa"),
              tooltip="Titik rawan banjir").add_to(peta)
for _, r in aset.iterrows():
    folium.CircleMarker(
        [r.lat, r.lon], radius=9, color=warna(r.skor), fill=True, fill_opacity=0.8,
        tooltip=f"{r.nama} | skor {r.skor}",
        popup=f"{r.nama}<br>Jenis: {r.jenis}<br>Jarak: {r.jarak_km} km<br>Skor: {r.skor}",
    ).add_to(peta)
peta.save("output/03_peta_aset.html")

# Ekspor GeoJSON agar bisa dibuka di QGIS
geojson = {"type": "FeatureCollection", "features": [
    {"type": "Feature",
     "geometry": {"type": "Point", "coordinates": [r.lon, r.lat]},
     "properties": {"nama": r.nama, "jenis": r.jenis, "jarak_km": r.jarak_km, "skor": r.skor}}
    for _, r in aset.iterrows()]}
with open("output/03_aset.geojson", "w") as f:
    json.dump(geojson, f, indent=2)
print("Peta: output/03_peta_aset.html | GeoJSON: output/03_aset.geojson")
