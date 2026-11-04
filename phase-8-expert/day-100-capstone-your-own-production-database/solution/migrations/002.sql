-- 002: school terms, and the fee invoice each student gets per term.

CREATE TABLE terms (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year      integer NOT NULL CHECK (year BETWEEN 2020 AND 2100),
    term      integer NOT NULL CHECK (term BETWEEN 1 AND 3),
    starts_on date NOT NULL,
    ends_on   date NOT NULL,
    UNIQUE (year, term),
    CHECK (ends_on > starts_on)
);

CREATE TABLE invoices (
    id         integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id integer NOT NULL REFERENCES students (id),
    term_id    integer NOT NULL REFERENCES terms (id),
    amount     integer NOT NULL CHECK (amount > 0),
    UNIQUE (student_id, term_id)
);
CREATE INDEX invoices_term ON invoices (term_id);
