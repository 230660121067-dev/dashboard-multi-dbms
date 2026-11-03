-- Buat Tabel Master Pelanggan
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    province VARCHAR(50) NOT NULL,
    membership_tier VARCHAR(20) NOT NULL
);

-- Seed Data Pelanggan
INSERT INTO customers (customer_id, customer_name, city, province, membership_tier) VALUES
('CUST-001', 'Budi Santoso', 'Bandung', 'Jawa Barat', 'Gold'),
('CUST-002', 'Siti Aminah', 'Surabaya', 'Jawa Timur', 'Platinum'),
('CUST-003', 'Ahmad Rizky', 'Sumedang', 'Jawa Barat', 'Silver'),
('CUST-004', 'Dewi Lestari', 'Jakarta Selatan', 'DKI Jakarta', 'Gold');