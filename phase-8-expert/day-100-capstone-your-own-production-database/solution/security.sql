-- The app logs in as capstone_app: it can read everything and record payments, and nothing more.
CREATE ROLE capstone_app LOGIN;
GRANT USAGE ON SCHEMA public TO capstone_app;
GRANT SELECT ON guardians, students, terms, invoices, payments TO capstone_app;
GRANT INSERT ON payments TO capstone_app;
