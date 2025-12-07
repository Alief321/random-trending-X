# Random Trending X

Aplikasi yang menampilkan trending topic acak (random) dari Indonesia dalam format SVG badge.

## Fitur

- 🔥 Menampilkan trending topic **acak** dari Indonesia
- 📊 Menampilkan jumlah tweet untuk setiap trending
- 💾 Caching otomatis 24 jam untuk menghemat request
- 🎨 Output SVG yang dapat ditampilkan di berbagai platform

## Teknologi

- **Python 3.x**
- **Flask** - Web framework
- **BeautifulSoup** - Web scraping
- **Requests** - HTTP client
- **trends24.in** - Data source trending topics

## Instalasi

1. Clone atau download project ini
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Penggunaan

1. Jalankan server lokal:

```bash
python local_server.py
```

2. Server akan berjalan di `http://localhost:3000`

3. Akses endpoint trending:

```
GET http://localhost:3000/api/trending
```

Akan mengembalikan SVG badge dengan trending topic acak.

### Parameter Query

- `?theme=light` - Gunakan light mode (default: dark)
- `?theme=dark` - Gunakan dark mode

Contoh:

```
GET http://localhost:3000/api/trending?theme=light
GET http://localhost:3000/api/trending?theme=dark
```

## Deploy ke Vercel

### Prerequisites

- Akun Vercel
- Git repository

### Langkah-langkah Deploy

1. Push kode ke GitHub:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push
```

2. Buka [vercel.com](https://vercel.com) dan login dengan GitHub

3. Klik "New Project" dan pilih repository ini

4. Vercel akan otomatis mendeteksi konfigurasi dari `vercel.json`

5. Klik "Deploy"

### Testing di Vercel

Setelah deploy, akses endpoint:

```
https://your-project-name.vercel.app/api/trending
https://your-project-name.vercel.app/api/trending?theme=light
```

## Struktur Folder

```
random-trending-X/
├── api/
│   ├── index.py             # Entrypoint Vercel (Flask app)
│   ├── trending.py          # Handler endpoint API
│   └── __pycache__/
├── utils/
│   ├── scrape_trending.py   # Fungsi scraping data trending
│   ├── cache.py             # Sistem caching
│   └── __pycache__/
├── local_server.py          # Server Flask lokal
├── requirements.txt         # Dependencies
├── pyproject.toml          # Konfigurasi Python project
├── vercel.json             # Konfigurasi Vercel deployment
├── README.md               # Dokumentasi
└── .git/                   # Git repository
```

## Cara Kerja

1. **Scraping**: `scrape_trending.py` mengambil data dari trends24.in dan memilih **satu trending topic secara acak** dari daftar
2. **Caching**: `cache.py` menyimpan hasil scraping selama 24 jam untuk mengurangi beban
3. **API**: `api/trending.py` mengembalikan data dalam format SVG badge
4. **Server**: `local_server.py` menjalankan Flask server di port 3000

## Dependencies

- flask
- requests
- beautifulsoup4

Lihat `requirements.txt` untuk versi lengkap.

## Notes

- Data trending diambil dari Indonesia (trends24.in/indonesia/)
- Cache berlaku 24 jam, setelah itu data akan di-refresh
- Setiap refresh akan mengambil trending topic yang berbeda (acak)
