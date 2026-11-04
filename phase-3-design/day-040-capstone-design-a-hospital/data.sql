-- One week at a made-up county hospital's outpatient clinic. The people are invented and the
-- drug prices are illustrative, not real tariffs. Run it after your schema.sql:
--   tools/mysql.sh hospital < phase-3-design/day-040-capstone-design-a-hospital/data.sql
INSERT INTO departments (id, name) VALUES
    (1, 'Outpatient'), (2, 'Paediatrics'), (3, 'Maternity'), (4, 'Dental'), (5, 'Eye');
INSERT INTO doctors (id, name, licence_no, department_id) VALUES
    (1, 'Dr Achieng Oloo', 'A10001', 1), (2, 'Dr Brian Mutua', 'A10002', 1),
    (3, 'Dr Caroline Wafula', 'A10003', 2), (4, 'Dr David Kiprop', 'A10004', 3),
    (5, 'Dr Esther Njeri', 'A10005', 4);
INSERT INTO patients (id, name, national_id, born_on, phone) VALUES
    (1, 'Wanjiru Kamau', '23456781', '1988-04-12', '254711000101'),
    (2, 'Omondi Otieno', '24567892', '1975-09-30', '254722000202'),
    (3, 'Halima Yusuf', '30123456', '1996-01-21', '254733000303'),
    (4, 'Kiprono Langat', NULL, '2021-06-02', NULL),
    (5, 'Njeri Mwangi', '28765431', '1990-11-11', '254755000505'),
    (6, 'Peter Ndungu', '21987654', '1969-02-14', '254766000606');
INSERT INTO next_of_kin (patient_id, name, relationship, phone) VALUES
    (1, 'James Kamau', 'spouse', '254711222333'),
    (4, 'Mary Langat', 'mother', '254722333444'),
    (4, 'Paul Langat', 'father', '254733444555');
INSERT INTO visits (id, patient_id, doctor_id, visited_at, diagnosis) VALUES
    (1, 1, 1, '2026-10-01 09:00:00', 'Malaria'),
    (2, 2, 1, '2026-10-01 10:30:00', 'Hypertension'),
    (3, 4, 3, '2026-10-02 08:45:00', 'Pneumonia'),
    (4, 1, 4, '2026-10-03 11:00:00', 'Antenatal check'),
    (5, 3, 5, '2026-10-03 14:00:00', 'Tooth extraction'),
    (6, 4, 3, '2026-10-05 09:30:00', 'Pneumonia review'),
    (7, 1, 2, '2026-10-06 10:00:00', 'Malaria follow-up'),
    (8, 6, 2, '2026-10-06 12:00:00', 'Typhoid'),
    (9, 2, 2, '2026-10-07 09:15:00', NULL);
INSERT INTO drugs (id, name, unit_price) VALUES
    (1, 'Artemether-lumefantrine', 120.00), (2, 'Paracetamol', 5.00), (3, 'Amlodipine', 15.00),
    (4, 'Amoxicillin', 10.00), (5, 'Ferrous sulphate', 3.00), (6, 'Ciprofloxacin', 12.00),
    (7, 'Insulin', 450.00);
INSERT INTO prescriptions (visit_id, drug_id, quantity) VALUES
    (1, 1, 24), (1, 2, 18), (2, 3, 30), (3, 4, 21), (3, 2, 10), (4, 5, 30), (5, 2, 12),
    (7, 2, 10), (8, 6, 14);
