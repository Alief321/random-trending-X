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

## Struktur Folder

```
random-trending-X/
├── api/
│   └── trending.py          # Handler endpoint API
├── utils/
│   ├── scrape_trending.py   # Fungsi scraping data trending
│   └── cache.py             # Sistem caching
├── local_server.py          # Server Flask lokal
├── requirements.txt         # Dependencies
└── README.md               # Dokumentasi
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
