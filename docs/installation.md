# Panduan Instalasi (Installation Guide)

Dokumen ini menjelaskan langkah-langkah untuk mempersiapkan lingkungan (environment) dan menjalankan aplikasi Realtime Object Detection.

## Prasyarat
Sebelum menginstal aplikasi, pastikan sistem Anda memiliki:
1. **Python 3.8 - 3.11** (Sangat disarankan).
2. **Git** (Opsional, jika Anda mengkloning dari repository).
3. **Kamera (Webcam)** yang terhubung jika ingin mendeteksi objek secara langsung.

## Langkah-langkah Instalasi

### 1. Kloning Repository atau Unduh Kode
Jika Anda menggunakan Git:
```bash
git clone https://github.com/jojixyz666/realtimeobjectdetection.git
cd realtimeobjectdetection
```

### 2. Membuat Virtual Environment (Disarankan)
Sangat disarankan untuk menggunakan *virtual environment* agar dependensi (library) aplikasi tidak bentrok dengan library global di sistem Anda.

**Untuk Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Untuk Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Menginstal Dependensi
Setelah environment aktif, instal semua pustaka yang dibutuhkan melalui `requirements.txt`:
```bash
pip install -r requirements.txt
```

> **Catatan untuk Pengguna NVIDIA GPU (CUDA):**  
> Jika Anda memiliki GPU NVIDIA dan ingin mempercepat proses deteksi, instal versi PyTorch yang mendukung CUDA:
> ```bash
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
> ```
> *Sesuaikan versi `cu121` dengan versi CUDA yang terinstal di sistem Anda.*

> **Catatan untuk Pengguna AMD GPU (DirectML):**  
> Aplikasi ini mendukung akselerasi perangkat keras AMD menggunakan format ONNX dan *DirectML Execution Provider*. Untuk mengaktifkannya, pastikan Anda telah menginstal pustaka tambahan berikut:
> ```bash
> pip install onnx onnxruntime-directml
> ```

### 4. Mengunduh Model YOLO (Opsional)
Aplikasi ini menggunakan model YOLO (misalnya `yolo26n.pt`). Secara default, aplikasi akan secara otomatis mengunduh model tersebut jika tidak ditemukan di dalam folder `models/`. Anda juga bisa menempatkan model YOLO kustom Anda ke dalam folder `models/` dan mengubah konfigurasinya di `config.yaml`.

### 5. Menjalankan Aplikasi
Anda dapat langsung menjalankan aplikasi dengan perintah:
```bash
python main.py
```
Saat dijalankan, aplikasi akan memunculkan **menu interaktif di terminal** yang memungkinkan Anda untuk memilih secara langsung:
1. **Model YOLO** (YOLOv8n, YOLOv8s, YOLOv11n, YOLO26n, atau custom)
2. **Hardware Device** (Auto, CPU, NVIDIA GPU CUDA, atau AMD GPU DirectML)
3. **Resolusi Kamera** (Minimal, SD, HD, atau FHD)

*Catatan: Aplikasi tetap akan membaca konfigurasi awal sumber video dan parameter deteksi lainnya dari `config.yaml`.*
