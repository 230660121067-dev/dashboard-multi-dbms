import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Multi-DBMS Pipeline (PostgreSQL + MySQL)", layout="wide")

st.title("📊 Dashboard Integrasi Multi-DBMS (PostgreSQL & MySQL)")
st.markdown("Penggabungan Data **PostgreSQL** (Transaksi) & **MySQL** (Profil Pelanggan) menggunakan **Pandas**.")

# --- FUNGSI PIPELINE DATA ---
@st.cache_data(ttl=600)
def load_and_pipeline_data():
    # 1. Ambil data dari DBMS 1 (PostgreSQL)
    pg_url = st.secrets["postgres"]["url"]
    pg_engine = create_engine(pg_url)
    query_pg = "SELECT transaction_id, customer_id, transaction_date, quantity, total_amount FROM transactions;"
    df_pg = pd.read_sql(query_pg, con=pg_engine)

    # 2. Ambil data dari DBMS 2 (MySQL)
    mysql_url = st.secrets["mysql"]["url"]
    mysql_engine = create_engine(mysql_url)
    query_mysql = "SELECT customer_id, customer_name, city, province, membership_tier FROM customers;"
    df_mysql = pd.read_sql(query_mysql, con=mysql_engine)

    # 3. Samakan tipe data customer_id ke STRING (teks) agar kompatibel
    df_pg["customer_id"] = df_pg["customer_id"].astype(str)
    df_mysql["customer_id"] = df_mysql["customer_id"].astype(str)

    # 4. Data Federation / Joining via Pandas
    df_merged = pd.merge(df_pg, df_mysql, on="customer_id", how="inner")
    
    # Konversi Tipe Data Tambahan
    df_merged["transaction_date"] = pd.to_datetime(df_merged["transaction_date"])
    df_merged["total_amount"] = df_merged["total_amount"].astype(float)
    
    return df_merged

# Memuat Data & Menampilkan UI
try:
    df = load_and_pipeline_data()

    # --- SIDEBAR FILTER INTERAKTIF ---
    st.sidebar.header("Filter Interaktif")
    selected_province = st.sidebar.multiselect(
        "Pilih Provinsi:",
        options=df["province"].unique(),
        default=df["province"].unique()
    )
    
    selected_tier = st.sidebar.multiselect(
        "Pilih Membership Tier:",
        options=df["membership_tier"].unique(),
        default=df["membership_tier"].unique()
    )

    # Filtering Data
    filtered_df = df[
        (df["province"].isin(selected_province)) & 
        (df["membership_tier"].isin(selected_tier))
    ]

    # --- METRIK UTAMA ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transaksi", f"Rp {filtered_df['total_amount'].sum():,.0f}")
    col2.metric("Total Item Terjual", int(filtered_df['quantity'].sum()))
    col3.metric("Jumlah Pelanggan Aktif", filtered_df['customer_id'].nunique())

    st.markdown("---")

    # --- VISUALISASI ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Total Penjualan per Wilayah (Provinsi)")
        fig_bar = px.bar(
            filtered_df, 
            x="province", 
            y="total_amount", 
            color="membership_tier",
            barmode="group",
            title="Pendapatan per Provinsi berdasarkan Tier Membership",
            labels={"province": "Provinsi", "total_amount": "Total Bayar (Rp)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("Tren Penjualan Harian")
        fig_line = px.line(
            filtered_df.sort_values("transaction_date"), 
            x="transaction_date", 
            y="total_amount",
            color="customer_name",
            markers=True,
            title="Tren Pendapatan Harian per Pelanggan",
            labels={"transaction_date": "Tanggal", "total_amount": "Total Bayar (Rp)"}
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # --- TABEL DATA HASIL INTEGRASI ---
    st.subheader("Tabel Hasil Penggabungan Data (Data Federation)")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Gagal menghubungkan atau memproses data: {e}")