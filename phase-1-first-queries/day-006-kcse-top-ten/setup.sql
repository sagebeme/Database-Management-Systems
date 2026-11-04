-- KCSE results for 25 candidates. The schools and counties are real; the candidates and their
-- points are made up. Points run from 12 to 84 (seven subjects, up to 12 points each).
--   tools/mysql.sh kcse < phase-1-first-queries/day-006-kcse-top-ten/setup.sql
DROP TABLE IF EXISTS results;
CREATE TABLE results (
    id INT,
    name VARCHAR(60),
    school VARCHAR(60),
    county VARCHAR(30),
    points INT,
    grade VARCHAR(2)
);
INSERT INTO results (id, name, school, county, points, grade) VALUES
    (1, 'Achieng Odhiambo', 'Kenya High', 'Nairobi', 63, 'B'),
    (2, 'Esther Mohamed', 'Maseno School', 'Kisumu', 65, 'B'),
    (3, 'Purity Atieno', 'Kapsabet Boys', 'Nandi', 55, 'B-'),
    (4, 'Brian Mwangi', 'Mang''u High', 'Kiambu', 61, 'B'),
    (5, 'Kiprop Langat', 'Mang''u High', 'Kiambu', 73, 'B+'),
    (6, 'Linet Omondi', 'Alliance High', 'Kiambu', 66, 'B'),
    (7, 'Faith Njeri', 'Mang''u High', 'Kiambu', 79, 'A-'),
    (8, 'Ivy Kimani', 'Bunyore Girls', 'Vihiga', 58, 'B-'),
    (9, 'Yusuf Onyango', 'Lenana School', 'Nairobi', 78, 'A-'),
    (10, 'Otieno Ndegwa', 'Bunyore Girls', 'Vihiga', 78, 'A-'),
    (11, 'Chebet Kiplagat', 'Lenana School', 'Nairobi', 52, 'C+'),
    (12, 'Mutua Kariuki', 'Moi Girls Eldoret', 'Uasin Gishu', 66, 'B'),
    (13, 'Kamau Mutiso', 'Lenana School', 'Nairobi', 68, 'B+'),
    (14, 'James Chepkoech', 'Alliance High', 'Kiambu', 84, 'A'),
    (15, 'Njoroge Kilonzo', 'Moi Girls Eldoret', 'Uasin Gishu', 82, 'A'),
    (16, 'George Barasa', 'Moi Girls Eldoret', 'Uasin Gishu', 75, 'A-'),
    (17, 'Rashid Kiprono', 'Kapsabet Boys', 'Nandi', 78, 'A-'),
    (18, 'Nekesa Muthoni', 'Kenya High', 'Nairobi', 81, 'A'),
    (19, 'Mercy Wairimu', 'Kapsabet Boys', 'Nandi', 70, 'B+'),
    (20, 'Zawadi Wambui', 'Alliance High', 'Kiambu', 76, 'A-'),
    (21, 'Tabitha Juma', 'Alliance High', 'Kiambu', 49, 'C+'),
    (22, 'Halima Akinyi', 'Kenya High', 'Nairobi', 73, 'B+'),
    (23, 'Sharon Nduta', 'Maseno School', 'Kisumu', 82, 'A'),
    (24, 'Daniel Wanjiru', 'Maseno School', 'Kisumu', 74, 'A-'),
    (25, 'Wekesa Wafula', 'Bunyore Girls', 'Vihiga', 71, 'B+');
