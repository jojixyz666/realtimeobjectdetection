# Pemecahan Masalah (Troubleshooting)

Dokumen ini berisi solusi untuk beberapa masalah umum yang mungkin Anda temui saat menginstal atau menjalankan aplikasi Realtime Object Detection.

## 1. Kamera (Webcam) Tidak Terbaca
**Gejala:** Aplikasi berjalan namun langsung keluar dengan pesan error `Could not open video source. Exiting.`
**Penyebab & Solusi:**
- **Kamera tidak terhubung atau sedang digunakan aplikasi lain:** Pastikan kamera (webcam) tertancap dengan baik dan tidak sedang dipakai oleh aplikasi seperti Zoom, OBS, atau Skype. Tutup aplikasi tersebut lalu coba lagi.
- **Index Kamera Salah:** Pada file `config.yaml`, nilai `source.input` mungkin `0`. Jika Anda memiliki lebih dari satu kamera, coba ubah menjadi `1`, `2`, dst.

## 2. Error pada saat Instalasi Dependensi (pip install)
**Gejala:** Terdapat tulisan berwarna merah (Error) ketika menjalankan `pip install -r requirements.txt`, khususnya pada paket `opencv-python` atau `torch`.
**Solusi:**
- Pastikan versi Python Anda adalah 3.8 hingga 3.11. Terkadang pustaka belum mendukung versi Python yang terlalu baru (seperti 3.12+).
- Coba perbarui versi pip: `python -m pip install --upgrade pip`, kemudian jalankan lagi perintah instalasinya.
- Jika error terkait `torch`, cobalah menginstal `torch` secara terpisah dari website resmi PyTorch yang sesuai dengan spesifikasi perangkat Anda.

## 3. Frame Rate (FPS) Sangat Rendah
**Gejala:** Video terlihat patah-patah (lag) atau FPS yang ditampilkan di layar sangat kecil (misal: di bawah 5 FPS).
**Solusi:**
- **Gunakan GPU:** Secara default, inference akan menggunakan CPU jika PyTorch dengan CUDA tidak terinstal. Menginstal PyTorch versi CUDA sangat meningkatkan FPS.
- **Ubah Ukuran Gambar (imgsz):** Buka `config.yaml` dan turunkan nilai `model.imgsz` dari `640` ke angka yang lebih kecil yang kelipatan 32 (misalnya `320` atau `416`). Perlu diingat, ini mungkin mengurangi akurasi deteksi.
- **Aktifkan Half Precision (FP16):** Jika Anda menggunakan GPU, ubah konfigurasi `model.half` menjadi `true` di `config.yaml`.

## 4. Tampilan Jendela (Window) Tidak Muncul atau Langsung Tertutup
**Gejala:** Script selesai dijalankan (atau error) tapi tidak ada jendela video yang terbuka.
**Solusi:**
- Cek file log di dalam folder `logs/app.log` untuk melihat pesan error secara spesifik.
- Pastikan `output.show_window` di `config.yaml` bernilai `true`.
- Jika Anda menjalankannya pada server atau environment tanpa Desktop/GUI (headless), Anda harus menyetel `output.show_window: false` dan menggunakan fitur `save_video: true` untuk melihat hasilnya.

## 5. Model Gagal Dimuat (Error Loading Model)
**Gejala:** Pesan error terkait file `.pt` atau YOLO tidak ditemukan/corrupt.
**Solusi:**
- Cek folder `models/`. Pastikan file model (misal `yolo26n.pt`) ada dan dapat dibaca.
- Hapus file model tersebut jika ukurannya tidak wajar (corrupt) agar aplikasi bisa mengunduhnya ulang saat dijalankan.
- Periksa koneksi internet saat menjalankan aplikasi pertama kali, karena library YOLO butuh mengunduh model.
