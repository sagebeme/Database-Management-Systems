-- A SACCO account two tellers serve at once, and a matatu with a few seats left (invented).
--   tools/mysql.sh sacco < phase-6-transactions-and-storage/day-066-two-tellers-one-account/setup.sql
DROP TABLE IF EXISTS bookings, trips, accounts;
CREATE TABLE accounts (
    phone CHAR(12) PRIMARY KEY,
    balance INT NOT NULL
);
CREATE TABLE trips (
    id INT PRIMARY KEY,
    route VARCHAR(40) NOT NULL,
    seats INT NOT NULL
);
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    passenger VARCHAR(40) NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips (id)
);
INSERT INTO accounts VALUES ('254711000001', 1500);
INSERT INTO trips VALUES (1, 'Nairobi - Nakuru', 14), (2, 'Nairobi - Machakos', 4);
INSERT INTO bookings (trip_id, passenger) VALUES (2, 'Wanjiku'), (2, 'Otieno');
