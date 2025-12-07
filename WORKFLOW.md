# GitHub Actions Workflow Documentation

## Overview

Workflow ini menjalankan scraper otomatis setiap hari untuk mengupdate trending topic di README.

## File: `.github/workflows/scraper.yml`

### Trigger (Kapan Workflow Berjalan)

```yaml
on:
  schedule:
    # Jalankan setiap hari pada jam 00:00 UTC (07:00 WIB)
    - cron: '0 0 * * *'

  # Juga bisa dijalankan manual dari Actions tab
  workflow_dispatch:
```

**Penjelasan:**

- `schedule` - Berjalan otomatis sesuai jadwal
- `cron: '0 0 * * *'` - Setiap hari pukul 00:00 UTC

  - Format: `minute hour day month weekday`
  - `0 0` = 00:00 (tengah malam UTC)
  - Untuk WIB (UTC+7): Pukul 07:00 pagi

- `workflow_dispatch` - Bisa dijalankan manual dari Actions tab

### Jobs

#### Setup Environment

```yaml
runs-on: ubuntu-latest
```

Workflow berjalan di Ubuntu latest environment.

#### Permissions

```yaml
permissions:
  contents: write
```

Memerlukan akses write untuk commit dan push ke repository.

### Steps

#### 1. Checkout Repository

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

Clone repository ke workflow environment.

#### 2. Setup Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'
```

Install Python 3.11 dan cache pip untuk kecepatan.

#### 3. Install Dependencies

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install requests beautifulsoup4
```

Install requirements yang dibutuhkan scraper.

#### 4. Run Scraper

```yaml
- name: Run scraper
  run: python scraper.py
```

Jalankan script scraper untuk get trending data dan update README.

#### 5. Commit dan Push

```yaml
- name: Commit and push changes
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"

    if git diff --quiet; then
      echo "No changes to commit"
    else
      git add README.md
      git commit -m "🔥 Update random trending topic - $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
      git push
```

Jika ada perubahan di README, otomatis commit dengan pesan timestamp.

## Melihat Workflow Berjalan

1. Buka repository di GitHub
2. Klik tab **"Actions"**
3. Pilih **"Daily Trending Scraper"** di sidebar
4. Klik workflow run untuk melihat detail logs

## Menjalankan Secara Manual

1. Buka tab **"Actions"**
2. Pilih **"Daily Trending Scraper"**
3. Klik tombol **"Run workflow"** → **"Run workflow"**
4. Workflow akan berjalan segera

## Troubleshooting

### Workflow tidak muncul di Actions tab?

**Solusi:**

1. Pastikan file `.github/workflows/scraper.yml` ada di repository
2. Commit dan push file ke GitHub
3. Refresh halaman Actions

### Workflow berjalan tapi tidak update README?

**Periksa:**

1. Lihat logs di Actions untuk error details
2. Pastikan `python scraper.py` return code 0 (success)
3. Cek apakah ada syntax error di README format

### Cron schedule tidak jalan sesuai waktu?

**Catatan:**

- GitHub Actions menggunakan UTC timezone
- Jika ingin 12:00 WITA (UTC+8), gunakan: `0 4 * * *`
- Jika ingin 00:00 WIB (UTC+7), gunakan: `0 17 * * *` (hari sebelumnya)

### Repo permission error saat push?

**Solusi:**

1. Pastikan workflow memiliki `write` permissions
2. Di repository Settings → Actions → Workflow permissions
3. Pilih "Read and write permissions"

## Customization

### Mengubah Jadwal

Edit `.github/workflows/scraper.yml`:

```yaml
on:
  schedule:
    - cron: '0 12 * * *' # Ubah ke 12:00 UTC
```

### Mengubah Timezone

Saat ini menggunakan UTC. Untuk convert:

- **WIB (UTC+7):** Kurangi 7 jam dari jam yang diinginkan
  - Contoh: Ingin 07:00 WIB → `0 0 * * *` (00:00 UTC)
- **WITA (UTC+8):** Kurangi 8 jam
  - Contoh: Ingin 08:00 WITA → `0 0 * * *` (00:00 UTC)

## Best Practices

1. **Test Workflow**

   - Jalankan scraper.py secara lokal terlebih dahulu
   - Pastikan tidak ada error sebelum push

2. **Monitor Status**

   - Cek Actions tab secara berkala
   - Setup branch protection rules kalau diperlukan

3. **Update Dependencies**

   - Periksa versi Python & packages secara berkala
   - Update action versions yang deprecated

4. **Commit Messages**
   - Include timestamp untuk tracking
   - Use emoji untuk visual clarity

---

Untuk info lebih lanjut, lihat [GitHub Actions Documentation](https://docs.github.com/en/actions)
