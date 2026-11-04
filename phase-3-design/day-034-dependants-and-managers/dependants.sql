-- Who each employee's medical cover includes. Run it after your 0-dependants.sql.
INSERT INTO dependants (employee_id, name, relationship, born_on) VALUES
    (1, 'Brian', 'spouse', '1975-03-02'),
    (1, 'Ivy', 'child', '2005-07-19'),
    (2, 'Ann', 'spouse', '1982-11-30'),
    (2, 'Leo', 'child', '2012-01-08'),
    (2, 'Mia', 'child', '2015-09-21'),
    (4, 'Ruth', 'spouse', '1990-04-14'),
    (7, 'Amina', 'child', '2018-06-01'),
    (7, 'Omar', 'child', '2020-12-12'),
    (9, 'Ivy', 'child', '2022-02-02');
