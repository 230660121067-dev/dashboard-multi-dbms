import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, MetaData

# Tautan koneksi MySQL Aiven
MYSQL_URL = "mysql+mysqlconnector://avnadmin:AVNS_D8Yo69rK2wPRlaikhhb@mysql-2b49d9e6-multi-dbms-project.k.aivencloud.com:21492/defaultdb"

# Data dummy pelanggan dengan format ID yang cocok dengan PostgreSQL ('CUST-xxx')
customers_data = [
    {"customer_id": "CUST-001", "customer_name": "Budi Santoso", "city": "Jakarta", "province": "DKI Jakarta", "membership_tier": "Gold"},
    {"customer_id": "CUST-002", "customer_name": "Siti Aminah", "city": "Bandung", "province": "Jawa Barat", "membership_tier": "Silver"},
    {"customer_id": "CUST-003", "customer_name": "Dewi Lestari", "city": "Surabaya", "province": "Jawa Timur", "membership_tier": "Platinum"},
    {"customer_id": "CUST-004", "customer_name": "Eko Prasetyo", "city": "Yogyakarta", "province": "DI Yogyakarta", "membership_tier": "Bronze"},
    {"customer_id": "CUST-005", "customer_name": "Rina Wijaya", "city": "Semarang", "province": "Jawa Tengah", "membership_tier": "Gold"}
]

try:
    print("Menghubungkan ke MySQL Aiven...")
    engine = create_engine(MYSQL_URL)
    metadata = MetaData()

    # Re-create tabel dengan Primary Key tipe String (VARCHAR)
    customers_table = Table(
        'customers', metadata,
        Column('customer_id', String(50), primary_key=True),
        Column('customer_name', String(255)),
        Column('city', String(100)),
        Column('province', String(100)),
        Column('membership_tier', String(50))
    )

    # Hapus tabel lama jika ada, lalu buat ulang
    metadata.drop_all(engine)
    metadata.create_all(engine)

    # Masukkan data baru
    df_customers = pd.DataFrame(customers_data)
    df_customers.to_sql('customers', con=engine, if_exists='append', index=False)
    print("✅ Data MySQL berhasil diperbarui dengan format ID 'CUST-xxx'!")
except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")