# Informatics Practitioner Lecture Series — Studi Kasus & Implementasi

Tugas: membuat studi kasus berdasarkan materi para pemateri **Informatics Practitioner Lecture Series: Connecting Academic Knowledge with Industry and Global Technology** (Program Studi Informatika, Fakultas Teknik, Universitas Bengkulu), lengkap dengan implementasi kode.

**Nama:** _Sakina Risa Julianti_  
**NPM:** _G1A025069_

> Semua data pada repositori ini adalah **data simulasi** untuk memahami konsep dan alur kerja, bukan analisis lapangan atau sistem produksi yang telah divalidasi.

## Cara Menjalankan

```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
pip install -r requirements.txt
python 01_make_sense_of_data_with_ai.py
```
Hasil (grafik, peta, dashboard) tersimpan di folder `output/`.

## Ringkasan Sesi

| Sesi | Narasumber | Materi | Studi Kasus | File |
|---|---|---|---|---|
| 1 | Andria Arisal (BRIN) | Make Sense of Data with Analysis and AI | Analisis penjualan toko kopi kampus & prediksi omzet | `01_make_sense_of_data_with_ai.py` |
| 2 | Worawan Diaz Carballo (Thammasat UnivERSITY.) | Bridging Global Infrastructure to Address Local Challenges with HPC | Estimasi Pi Monte Carlo: sekuensial vs paralel | `02_hpc_bridging_global_infrastructure.py` |
| 3 | Widi Prima Deva (Citycare Property, NZ) | Career and Competition in Industrial Era with GIS | Prioritas pemeriksaan fasilitas publik di Kota Bengkulu terhadap zona rawan banjir | `03_gis_career_and_competition.py` |
| 4 | Taniza Tajuddin (Universiti Teknologi MARA, Cawangan Kedah) | Introduction to Machine Learning | Prediksi kelulusan tepat waktu mahasiswa (Decision Tree vs KNN) | `04_introduction_to_machine_learning.py` |
| 5 | Arafat Febriandirza (BRIN) | Human-Computer Interaction & Data Visualization | Dashboard monitoring server kampus | `05_hci_and_data_visualization.py` |
| 6 | Bart Slagter (Wageningen University & Research) | Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI | Klasifikasi penyebab deforestasi dari fitur NDVI/NBR | `06_deforestation_satellite_imagery_ai.py` |

---

## Sesi 1 — Make Sense of Data with Analysis and AI
**Studi kasus:** pemilik toko kopi kampus ingin memahami penjualan 12 bulan dan memperkirakan omzet bulan depan.
- **Deskriptif:** rata-rata dan total penjualan per produk; data kosong diisi median (data cleaning).
- **Diagnostik:** membandingkan penjualan saat ada promo dan tanpa promo untuk melihat produk mana yang paling terpengaruh.
- **Prediktif:** *Linear Regression* pada tren omzet bulanan untuk memperkirakan bulan berikutnya.

## Sesi 2 — HPC
**Studi kasus:** estimasi nilai π dengan metode Monte Carlo (tebar titik acak di dalam persegi, hitung yang jatuh di dalam seperempat lingkaran).
- Pekerjaan dipecah menjadi beberapa bagian dengan `multiprocessing.Pool`, lalu hasilnya digabung.
- Program membandingkan waktu sekuensial dan paralel serta menghitung *speedup*. Hasil bergantung pada jumlah core CPU di perangkat yang menjalankan.

## Sesi 3 — GIS
**Studi kasus:** dinas ingin menentukan fasilitas publik mana yang diperiksa lebih dulu terkait titik rawan banjir.
- Jarak aset ke titik rawan dihitung dengan rumus **Haversine**.
- Skor prioritas (0–100) = kerusakan (50%) + usia aset (25%) + kedekatan dengan zona (25%).
- Output: peta interaktif `folium` (`03_peta_aset.html`) dan **GeoJSON** yang bisa dibuka di QGIS.
- Koordinat bersifat perkiraan/simulasi.

## Sesi 4 — Introduction to Machine Learning
**Studi kasus:** memprediksi apakah mahasiswa lulus tepat waktu dari IPK, kehadiran, SKS, jam belajar, dan keaktifan organisasi.
- Pembagian data latih 80% dan uji 20%.
- Dua algoritma dibandingkan: **Decision Tree** dan **KNN** (dengan standardisasi fitur).
- Evaluasi dengan *accuracy*, *precision*, *recall*, *F1-score*, dan *confusion matrix*; model terbaik dipakai untuk memprediksi mahasiswa baru.

## Sesi 5 — HCI & Data Visualization
**Studi kasus:** dashboard monitoring server kampus (`output/05_dashboard.html`).
- **Visibility & chunking:** tiap metrik berada dalam kartu terpisah.
- **Color coding + ikon + teks:** status normal/waspada/kritis tidak hanya bergantung pada warna (aksesibilitas).
- **Affordance & feedback:** tombol diagnostik tampak bisa diklik dan memberi respons (status "Memeriksa..." lalu hasil).

## Sesi 6 — Deforestasi dengan Citra Satelit & AI
**Studi kasus:** mengklasifikasikan penyebab peringatan deforestasi: Kebakaran, Perkebunan, Infrastruktur, Perambahan kecil.
- Fitur: perubahan NDVI, perubahan NBR, jarak ke jalan, luas area, dan kekompakan bentuk.
- Model **Random Forest** dengan laporan klasifikasi dan grafik pentingnya fitur.
- Model dipakai untuk memprediksi penyebab pada alert baru.

## Struktur Repositori
```
├── 01_make_sense_of_data_with_ai.py
├── 02_hpc_bridging_global_infrastructure.py
├── 03_gis_career_and_competition.py
├── 04_introduction_to_machine_learning.py
├── 05_hci_and_data_visualization.py
├── 06_deforestation_satellite_imagery_ai.py
├── requirements.txt
├── output/        # grafik, peta, dashboard hasil run
└── README.md
```
