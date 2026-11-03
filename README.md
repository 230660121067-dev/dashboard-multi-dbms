# Multi-DBMS Data Pipeline: PostgreSQL + MySQL

## Ringkasan Arsitektur Data
Aplikasi ini mengintegrasikan dua sistem basis data relational yang berbeda:
1. **DBMS 1 (PostgreSQL - Neon/Supabase):** Menyimpan data transaksi harian (ID Transaksi, Pelanggan, Tanggal, Jumlah, dan Total Harga).
2. **DBMS 2 (MySQL - Aiven/Cloud MySQL):** Menyimpan data master profil pelanggan (Nama, Kota, Provinsi, dan Membership Tier).

### Alur Integrasi Data (Pipeline)
1. Kueri data transaksi dari PostgreSQL dieksekusi menggunakan `SQLAlchemy` dan `psycopg2`.
2. Kueri data master pelanggan dari MySQL dieksekusi menggunakan `SQLAlchemy` dan `mysql-connector-python`.
3. Penggabungan data (*Data Federation/Joining*) dilakukan di tingkat aplikasi menggunakan `Pandas` (`pd.merge()`) berbasis kolom `customer_id`.
4. Hasil penggabungan disajikan dalam visualisasi grafik interaktif Plotly melalui antarmuka web Streamlit.

## Fitur Interaktif
- **Filter Multi-Variabel:** Filtering data interaktif berdasarkan Provinsi dan Membership Tier.
- **Metric Cards:** Menampilkan KPI Total Transaksi, Total Item Terjual, dan Jumlah Pelanggan secara real-time.
- **Visualisasi Dynamic:** Grafik Batang dan Grafik Line interaktif.

## Tautan Referensi
- **Sumber Data Asli:** [Open Data Indonesia / Kaggle Dataset Sample](https://satu.data.go.id/) *(Sesuaikan)*
- **Referensi Kode/Proyek:** [Streamlit MySQL & PostgreSQL Connection Guide](https://docs.streamlit.io/) *(Sesuaikan)*