-- Least privilege. Tellers (sacco_teller and sacco_teller2): read only the id and name of members (never phone or
-- id_number), and read and add loans. The auditor: read every column of members and loans, nothing more.
GRANT SELECT (id, name) ON members TO sacco_teller, sacco_teller2;
GRANT SELECT, INSERT ON loans TO sacco_teller, sacco_teller2;
GRANT SELECT ON members, loans TO sacco_auditor;
