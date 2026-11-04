-- Invoices from Neno Printers, a print shop on Moi Avenue, Mombasa. Made up.
--   tools/mysql.sh printers < phase-1-first-queries/day-012-receipts-and-due-dates/setup.sql
DROP TABLE IF EXISTS invoices;
CREATE TABLE invoices (
    id INT,
    customer VARCHAR(60),
    item VARCHAR(60),
    amount DECIMAL(10, 2),
    issued_on DATE,
    days_to_pay INT,
    paid_on DATE
);
INSERT INTO invoices (id, customer, item, amount, issued_on, days_to_pay, paid_on) VALUES
    (1, 'Fatma Said', 'Wedding cards x200', 18500.00, '2025-01-06', 14, '2025-01-15'),
    (2, 'Juma Mwinyi', 'Business cards x500', 2750.50, '2025-01-20', 7, '2025-02-03'),
    (3, 'Rehema Ali', 'Posters A2 x50', 12000.00, '2025-02-03', 30, NULL),
    (4, 'Omar Bakari', 'Receipt books x20', 4300.00, '2025-02-10', 14, '2025-02-24'),
    (5, 'Fatma Said', 'Menus x40', 6800.00, '2025-02-28', 14, '2025-03-20'),
    (6, 'Zuhura Mohamed', 'Banner 3m', 9500.00, '2025-03-05', 7, NULL),
    (7, 'Juma Mwinyi', 'Flyers x2000', 15250.00, '2025-03-17', 30, '2025-04-10');
