# Changelog

Semua perubahan penting pada proyek **Real-Time Object Detection** ini akan dicatat di file ini. Format berkas ini mengacu pada [Keep a Changelog](https://keepachangelog.com/id/1.0.0/) dan proyek ini mematuhi [Semantic Versioning](https://semver.org/lang/id/).

---

## [1.1.0] - 2026-06-07

### Ditambahkan
- **Menu Interaktif CLI**: Penambahan menu pemilihan interaktif di terminal saat aplikasi dijalankan untuk memilih Model YOLO, Perangkat Keras (Device), dan Resolusi secara dinamis.
- **Dukungan AMD GPU (DirectML)**: Penambahan dukungan akselerasi inferensi menggunakan AMD GPU melalui format ONNX dan *Execution Provider* DirectML, serta pilihan CPU dan NVIDIA GPU (CUDA).
- **Auto-Resize Resolusi**: Fitur *software resize* otomatis sebagai *fallback* jika kamera perangkat keras tidak mendukung resolusi yang diminta pengguna.
- **Pilihan Berbagai Model**: Kemampuan untuk memilih antara beberapa varian model secara instan (YOLOv8n, YOLOv8s, YOLOv11n, YOLO26n) atau jalur model custom.

### Diubah
- **Alur Eksekusi Utama (`main.py`)**: Diubah menjadi interaktif (menunggu input pengguna) saat dijalankan, kecuali argumen tertentu diberikan melalui command line.

---

## [1.0.0] - 2026-06-06

### Ditambahkan
- **Modul Deteksi YOLO (`app/detector.py`)**: Integrasi dengan model Ultralytics YOLO (default `yolo26n.pt`) untuk pengenalan objek secara real-time.
- **Modul Video Source (`app/source.py`)**: Penanganan input video yang fleksibel, mendukung Webcam, file video lokal (`.mp4`, `.avi`, dll.), dan stream RTSP.
- **Manajemen Konfigurasi (`app/config_manager.py` & `config.yaml`)**: Sistem konfigurasi modular berbasis YAML untuk mempermudah pengaturan parameter tanpa harus menyentuh kode program.
- **Modul Output (`app/output_manager.py`)**: Fitur untuk menyimpan video beranotasi, menangkap gambar (screenshot), dan menyimpan log deteksi objek dalam bentuk file JSON.
- **Anotasi Visual (`app/annotator.py`)**: Penggambaran bounding box objek, nama kelas, confidence score, overlay FPS, dan timestamp pada frame video.
- **Kontrol Keyboard Interaktif**:
  - `Q` / `ESC` untuk keluar.
  - `SPACE` untuk jeda (pause) dan melanjutkan (resume) video.
  - `S` untuk mengambil screenshot frame asli.
  - `B` untuk menyembunyikan/menampilkan bounding boxes.
  - `I` untuk menyembunyikan/menampilkan overlay informasi (FPS & total objek).
- **Log Sistem (`logs/app.log`)**: Menggunakan modul Python `logging` untuk melacak proses inisialisasi aplikasi, error, dan ringkasan sesi.
- **Dokumentasi Lengkap (`docs/`)**:
  - `installation.md`: Panduan instalasi dan prasyarat sistem.
  - `file_structure.md`: Penjelasan struktur folder dan arsitektur kode.
  - `troubleshooting.md`: Penanganan masalah (troubleshoot) error kamera, lag, atau instalasi.
- **Lisensi MIT**: Penambahan file `LICENSE` MIT untuk proyek atas nama Joice Hielman Abbrori.

---

*Catatan: Versi ini adalah rilis awal (Initial Release) untuk memenuhi kebutuhan Tugas Besar Computer Vision 2026.*
