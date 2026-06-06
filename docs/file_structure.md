# Struktur File dan Direktori

Berikut adalah penjelasan struktur direktori dari aplikasi Realtime Object Detection ini untuk mempermudah Anda dalam memahami *source code* dan konfigurasi yang ada.

```text
realtimeobjectdetection/
│
├── app/                        # Direktori utama kode aplikasi
│   ├── annotator.py            # Modul untuk menggambar Bounding Box dan Teks FPS pada frame video
│   ├── config_manager.py       # Modul untuk memuat dan membaca file config.yaml
│   ├── detector.py             # Modul inti untuk memuat model YOLO dan melakukan inference/deteksi
│   ├── output_manager.py       # Modul untuk menangani penyimpanan video, gambar (screenshot), dan log
│   ├── source.py               # Modul untuk mengambil input video (webcam, file video, atau RTSP)
│   └── utils.py                # Kumpulan fungsi bantuan, seperti setup logger (pencatatan sistem)
│
├── docs/                       # Direktori untuk dokumentasi
│   ├── file_structure.md       # (File ini) Penjelasan struktur file
│   ├── installation.md         # Panduan instalasi dan setup awal
│   └── troubleshooting.md      # Panduan perbaikan masalah (Error solving)
│
├── logs/                       # Folder untuk menyimpan file log
│   └── app.log                 # Catatan (log) dari aktivitas aplikasi saat dijalankan
│
├── models/                     # Folder penyimpanan file model (Weights)
│   └── yolo26n.pt              # Contoh file model YOLO yang digunakan
│
├── output/                     # Folder untuk menyimpan hasil keluaran (opsional jika diset pada config)
│   ├── images/                 # Menyimpan file screenshot (tombol S)
│   └── videos/                 # Menyimpan hasil deteksi dalam bentuk rekaman video
│
├── venv/                       # Direktori Virtual Environment Python (Jika dibuat)
│
├── .gitkeep                    # File dummy untuk mempertahankan folder kosong di git
├── config.yaml                 # File konfigurasi UTAMA (Setting parameter deteksi, video, dll)
├── main.py                     # Skrip utama untuk menjalankan aplikasi (Entry point)
├── prd.md                      # Product Requirements Document (Dokumen Spesifikasi Kebutuhan Aplikasi)
├── README.md                   # Halaman depan / Informasi singkat proyek
└── requirements.txt            # Daftar pustaka (library) Python yang dibutuhkan
```

### Penjelasan File Utama
- **`main.py`**: Merupakan *entry point* yang menghubungkan semua modul dari folder `app/`. Saat dijalankan, `main.py` akan memanggil `ConfigManager`, membuat objek `VideoSource` dan `YOLO26Detector`, lalu menjalankan *looping* utama untuk menampilkan frame secara *real-time*.
- **`config.yaml`**: File konfigurasi ini memudahkan pengguna tanpa harus mengubah kode (coding). Pengguna dapat mengatur input kamera, akurasi deteksi, ketebalan kotak, hingga di mana file hasil akan disimpan.
- **`app/detector.py`**: Bertanggung jawab berinteraksi langsung dengan model YOLO (atau model AI lainnya) dan memproses hasil mentah (tensor) menjadi objek yang mudah dibaca oleh aplikasi.
