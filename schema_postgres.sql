-- Buat Tabel Transaksi Penjualan
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    transaction_date DATE NOT NULL,
    quantity INT NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL
);

-- Seed Data Transaksi
INSERT INTO transactions (customer_id, transaction_date, quantity, total_amount) VALUES
('CUST-001', '2026-10-01', 2, 500000.00),
('CUST-002', '2026-10-02', 1, 1500000.00),
('CUST-001', '2026-10-03', 4, 1000000.00),
('CUST-003', '2026-10-04', 3, 750000.00),
('CUST-002', '2026-10-05', 2, 3000000.00),
('CUST-004', '2026-10-06', 5, 1250000.00);