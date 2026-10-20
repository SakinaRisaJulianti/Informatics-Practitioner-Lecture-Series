"""
Sesi 2 - Bridging Global Infrastructure to Address Local Challenges with HPC
Narasumber : Asst. Prof. Worawan Diaz Carballo (Thammasat University)
Studi Kasus: Estimasi nilai Pi dengan Monte Carlo - perbandingan sekuensial vs paralel

Ide HPC: pekerjaan besar dipecah menjadi bagian kecil yang dikerjakan
banyak core CPU secara bersamaan, lalu hasilnya digabung.
"""
import os
import time
import numpy as np
import multiprocessing as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOTAL = 40_000_000


def hitung_dalam_lingkaran(args):
    n, seed = args
    rng = np.random.default_rng(seed)
    x, y = rng.random(n), rng.random(n)
    return int(np.count_nonzero(x * x + y * y <= 1.0))


def sekuensial(total):
    t = time.perf_counter()
    hasil = hitung_dalam_lingkaran((total, 0))
    return 4 * hasil / total, time.perf_counter() - t


def paralel(total, workers):
    t = time.perf_counter()
    bagian = total // workers
    tugas = [(bagian, s) for s in range(workers)]
    with mp.Pool(workers) as pool:
        hasil = sum(pool.map(hitung_dalam_lingkaran, tugas))
    return 4 * hasil / (bagian * workers), time.perf_counter() - t


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    maks = mp.cpu_count()
    print(f"CPU core tersedia: {maks}")
    pi_s, t_s = sekuensial(TOTAL)
    print(f"Sekuensial : pi={pi_s:.6f}  waktu={t_s:.2f}s")

    uji = sorted({1, 2, 4, maks})
    uji = [w for w in uji if w <= maks]
    waktu, speedup = [], []
    for w in uji:
        pi_p, t_p = paralel(TOTAL, w)
        waktu.append(t_p); speedup.append(t_s / t_p)
        print(f"Paralel {w:>2} proses: pi={pi_p:.6f}  waktu={t_p:.2f}s  speedup={t_s/t_p:.2f}x")

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].bar([str(w) for w in uji], waktu); ax[0].set_title("Waktu eksekusi (detik)")
    ax[0].set_xlabel("Jumlah proses")
    ax[1].plot(uji, speedup, marker="o", label="Aktual")
    ax[1].plot(uji, uji, "--", label="Ideal"); ax[1].legend()
    ax[1].set_title("Speedup"); ax[1].set_xlabel("Jumlah proses")
    plt.tight_layout(); plt.savefig("output/02_speedup.png", dpi=120)
    print("Grafik disimpan di output/02_speedup.png")
