-- Routes with their stops (an array), trips with what the app recorded about each (JSONB), and notices for
-- passengers (text to search). Stops are real Nairobi places; everything else is made up.
--   tools/psql.sh matatu -f phase-7-beyond-mysql/day-080-postgres-superpowers/setup.sql
DROP TABLE IF EXISTS routes, trips, notices;
CREATE TABLE routes (
    number TEXT PRIMARY KEY,
    stops TEXT[] NOT NULL
);
CREATE TABLE trips (
    id INT PRIMARY KEY,
    route TEXT NOT NULL REFERENCES routes (number),
    details JSONB NOT NULL
);
CREATE TABLE notices (
    id INT PRIMARY KEY,
    posted DATE NOT NULL,
    body TEXT NOT NULL
);
INSERT INTO routes VALUES
    ('46', '{Kencom,"Kenyatta Avenue",Westlands,Kawangware}'),
    ('111', '{Railways,"Kenyatta Market",Karen,Ngong}'),
    ('125', '{Railways,Nyayo,"Lang''ata",Rongai}'),
    ('105', '{Odeon,Westlands,Uthiru,Kikuyu}'),
    ('58', '{Kencom,Jogoo,Buruburu}'),
    ('237', '{Odeon,Ngara,Roysambu,Thika}');
INSERT INTO trips VALUES
    (1, '46', '{"driver": "Otieno", "seats": 14, "cashless": true, "fares": [70, 70, 50], "stops_missed": []}'),
    (2, '46', '{"driver": "Kamau", "seats": 14, "cashless": false, "fares": [70, 70, 70, 70]}'),
    (3, '111', '{"driver": "Chebet", "seats": 33, "cashless": true, "fares": [100, 80], "music": "loud"}'),
    (4, '125', '{"driver": "Mutua", "seats": 33, "cashless": true, "fares": [120, 120, 120], "stops_missed": ["Nyayo"]}'),
    (5, '105', '{"driver": "Njeri", "seats": 14, "cashless": false, "fares": []}'),
    (6, '58', '{"driver": "Otieno", "seats": 14, "cashless": true, "fares": [60, 60, 60, 60, 60]}'),
    (7, '237', '{"driver": "Wanjiru", "seats": 51, "cashless": true, "fares": [150, 150], "music": "gospel"}'),
    (8, '125', '{"driver": "Kiprop", "seats": 14, "fares": [100]}');
INSERT INTO notices VALUES
    (1, '2026-03-02', 'Thika Road is closed near Roysambu for repairs. Route 237 will use the service lane.'),
    (2, '2026-03-05', 'Fares rise by ten shillings on the Ngong road routes from Monday.'),
    (3, '2026-03-09', 'Cashless payment is now accepted on every route. Pay by M-Pesa at the door.'),
    (4, '2026-03-11', 'Heavy rain: expect delays on Langata Road and Mombasa Road this evening.'),
    (5, '2026-03-14', 'The Kencom stage is closing for a week while the road is repaired.'),
    (6, '2026-03-20', 'Lost property: a blue umbrella was left on a route 46 matatu. Ask at the Kencom office.');
