"""
Sesi 5 - Human-Computer Interaction & Data Visualization
Narasumber : Arafat Febriandirza (BRIN)
Studi Kasus: Dashboard pemantauan server kampus yang mudah dipindai

Prinsip HCI yang diterapkan:
  - Visibility      : status tiap metrik terlihat jelas
  - Color coding    : hijau (normal) / kuning (waspada) / merah (kritis) + ikon & teks
                      agar tidak hanya bergantung pada warna (aksesibilitas)
  - Chunking        : informasi dikelompokkan dalam kartu
  - Affordance      : tombol terlihat bisa diklik
  - Feedback        : tombol memberi respons setelah ditekan
Output: output/05_dashboard.html (buka di browser)
"""
import os
import json

os.makedirs("output", exist_ok=True)

metrik = [
    {"nama": "CPU", "nilai": 45, "unit": "%", "waspada": 70, "kritis": 90},
    {"nama": "Memori", "nilai": 78, "unit": "%", "waspada": 75, "kritis": 90},
    {"nama": "Disk", "nilai": 93, "unit": "%", "waspada": 80, "kritis": 90},
    {"nama": "Latensi Jaringan", "nilai": 38, "unit": "ms", "waspada": 100, "kritis": 200},
    {"nama": "Pengguna Aktif", "nilai": 412, "unit": "", "waspada": 800, "kritis": 1000},
    {"nama": "Error Rate", "nilai": 0.4, "unit": "%", "waspada": 2, "kritis": 5},
]


def status(m):
    if m["nilai"] >= m["kritis"]:
        return "kritis", "⛔", "Kritis"
    if m["nilai"] >= m["waspada"]:
        return "waspada", "⚠️", "Waspada"
    return "normal", "✅", "Normal"


kartu = ""
for m in metrik:
    kelas, ikon, label = status(m)
    persen = min(100, m["nilai"] / m["kritis"] * 100)
    kartu += f"""
    <div class="card {kelas}">
      <div class="judul">{m['nama']}</div>
      <div class="nilai">{m['nilai']}<span>{m['unit']}</span></div>
      <div class="bar"><div style="width:{persen:.0f}%"></div></div>
      <div class="badge">{ikon} {label}</div>
    </div>"""

html = f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard Monitoring Server</title>
<style>
  body {{ font-family: system-ui, sans-serif; background:#f4f6fa; margin:0; padding:24px; color:#1c2333; }}
  h1 {{ margin:0 0 4px; }} p.sub {{ margin:0 0 20px; color:#5b6478; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; }}
  .card {{ background:#fff; border-radius:14px; padding:16px; border-left:8px solid; box-shadow:0 2px 8px #0001; }}
  .card.normal  {{ border-color:#2e9e5b; }} .card.waspada {{ border-color:#e0a100; }} .card.kritis {{ border-color:#d6372f; }}
  .judul {{ font-size:14px; color:#5b6478; }}
  .nilai {{ font-size:34px; font-weight:700; margin:6px 0; }} .nilai span {{ font-size:16px; margin-left:4px; }}
  .bar {{ background:#e6e9f0; height:8px; border-radius:4px; overflow:hidden; }}
  .bar div {{ height:100%; background:currentColor; }}
  .normal .bar div {{ background:#2e9e5b; }} .waspada .bar div {{ background:#e0a100; }} .kritis .bar div {{ background:#d6372f; }}
  .badge {{ margin-top:10px; font-weight:600; font-size:14px; }}
  button {{ margin-top:24px; padding:12px 22px; border:0; border-radius:10px; background:#2f5bea; color:#fff;
            font-size:16px; cursor:pointer; transition:transform .1s, background .2s; }}
  button:hover {{ background:#1f45c4; }} button:active {{ transform:scale(.97); }}
  #hasil {{ margin-top:14px; padding:12px; border-radius:10px; background:#fff; display:none; }}
</style></head><body>
<h1>Dashboard Monitoring Server Kampus</h1>
<p class="sub">Data simulasi — warna + ikon + teks dipakai bersama agar mudah dibaca semua pengguna.</p>
<div class="grid">{kartu}</div>
<button id="diag">🔍 Jalankan Diagnostik</button>
<div id="hasil" role="status" aria-live="polite"></div>
<script>
  const metrik = {json.dumps(metrik)};
  document.getElementById('diag').addEventListener('click', function() {{
    const btn = this; btn.disabled = true; btn.textContent = '⏳ Memeriksa...';
    setTimeout(() => {{
      const bermasalah = metrik.filter(m => m.nilai >= m.waspada);
      const el = document.getElementById('hasil');
      el.style.display = 'block';
      el.innerHTML = bermasalah.length
        ? '<b>' + bermasalah.length + ' metrik perlu perhatian:</b> ' + bermasalah.map(m => m.nama).join(', ')
        : 'Semua metrik normal ✅';
      btn.disabled = false; btn.textContent = '🔍 Jalankan Diagnostik';
    }}, 800);
  }});
</script></body></html>"""

with open("output/05_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Dashboard dibuat: output/05_dashboard.html")
