-- Create zones (zone CHAR(3) primary key, town required) and addresses (street, zone -> zones, the pair as the key).
CREATE TABLE zones (
    zone CHAR(3) PRIMARY KEY,
    town VARCHAR(30) NOT NULL
);
CREATE TABLE addresses (
    street VARCHAR(40) NOT NULL,
    zone CHAR(3) NOT NULL,
    PRIMARY KEY (street, zone),
    FOREIGN KEY (zone) REFERENCES zones (zone)
);
