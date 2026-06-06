<div align="center">

# Real-Time Object Detection
### Tugas Besar Computer Vision 2026

[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.13.0+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-FF6F00?style=for-the-badge&logo=ultralytics&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<br>

<p align="center">
  <img src="https://raw.githubusercontent.com/ultralytics/assets/main/yolov8/banner-yolov8.png" width="800" alt="YOLOv8 Banner">
</p>

---

Aplikasi deteksi objek secara langsung (real-time) berbasis kecerdasan buatan (AI) menggunakan **YOLO (You Only Look Once)** dan **OpenCV**. Dikembangkan khusus untuk mendeteksi objek secara dinamis melalui webcam, file video, maupun stream RTSP dengan performa tinggi.

---
</div>

## Fitur Utama

- **Deteksi Real-Time Berperforma Tinggi** – Terintegrasi dengan PyTorch (mendukung akselerasi GPU CUDA) dan model YOLO untuk hasil inferensi yang cepat dan akurat.
- **Input Fleksibel** – Mendukung input video dari berbagai sumber: Webcam internal/eksternal, IP Camera, file video lokal (`.mp4`, `.avi`, dll.), atau gambar statis.
- **Konfigurasi Berbasis YAML** – Atur seluruh parameter aplikasi (sumber video, model, resolusi, threshold, dsb.) secara modular melalui [config.yaml](file:///d:/Development/pyhton/realtimeobjectdetection/config.yaml) tanpa mengubah kode program.
- **Kontrol Keyboard Interaktif** – Kontrol jalannya deteksi langsung dari window layar Anda (Pause, Resume, Toggle Kotak Bounding, Toggle Info overlay, Ambil Screenshot).
- **Output Kaya Data** – Opsi ekspor rekaman video beranotasi, penyimpanan screenshot instan, dan log deteksi objek berformat JSON.

---

## Dokumentasi Pendukung

Untuk panduan konfigurasi dan pemecahan masalah lebih mendalam, kunjungi:

| Dokumen | Deskripsi |
| :--- | :--- |
| **[Panduan Instalasi](docs/installation.md)** | Panduan setup Python, Virtual Environment, dan instalasi CUDA. |
| **[Struktur Direktori](docs/file_structure.md)** | Penjelasan arsitektur modul dan file kode pada aplikasi. |
| **[Pemecahan Masalah](docs/troubleshooting.md)** | Solusi jika kamera tidak terdeteksi, instalasi error, atau FPS rendah. |
| **[Changelog](CHANGELOG.md)** | Catatan riwayat versi dan pembaruan fitur pada aplikasi. |

---

## Memulai Cepat (Quick Start)

### 1. Setup Environment
```bash
# Buat Virtual Environment
python -m venv venv

# Aktifkan Environment (Windows)
venv\Scripts\activate

# Aktifkan Environment (Linux/macOS)
source venv/bin/activate

# Install Dependensi
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python main.py
```

---

## Kontrol Keyboard (Interactive Controls)

Saat jendela aplikasi terbuka, gunakan tombol berikut untuk berinteraksi langsung:

| Tombol | Aksi / Fungsi |
| :---: | :--- |
| <kbd>Q</kbd> atau <kbd>ESC</kbd> | **Keluar** dan menutup aplikasi secara aman. |
| <kbd>SPACE</kbd> (Spasi) | **Jeda (Pause) / Lanjutkan (Resume)** proses pemutaran video. |
| <kbd>S</kbd> | Mengambil **Screenshot** frame asli dan menyimpannya di folder output. |
| <kbd>B</kbd> | **Toggle Bounding Boxes** (menampilkan atau menyembunyikan kotak objek). |
| <kbd>I</kbd> | **Toggle Info Overlay** (menampilkan atau menyembunyikan FPS & jumlah objek). |

---

## Informasi Pengembang & Tugas

Aplikasi ini didevel dan diserahkan sebagai tugas mata kuliah:

<table>
  <tr>
    <td><b>Mata Kuliah</b></td>
    <td>Computer Vision 2026</td>
  </tr>
  <tr>
    <td><b>Nama Lengkap</b></td>
    <td>Joice Hielman Abbrori</td>
  </tr>
  <tr>
    <td><b>NPM</b></td>
    <td><code>722520073</code></td>
  </tr>
  <tr>
    <td><b>Lisensi</b></td>
    <td>MIT License (Lihat <a href="LICENSE">LICENSE</a>)</td>
  </tr>
</table>
