-- 001: guardians and the students they pay for.

CREATE TABLE guardians (
    id    integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name  text NOT NULL CHECK (btrim(name) <> ''),
    phone text NOT NULL UNIQUE CHECK (phone ~ '^254[17][0-9]{8}$')
);

CREATE TABLE students (
    id          integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    adm_no      text NOT NULL UNIQUE,
    name        text NOT NULL CHECK (btrim(name) <> ''),
    guardian_id integer NOT NULL REFERENCES guardians (id),
    class       text NOT NULL CHECK (class IN ('Grade 7', 'Grade 8', 'Grade 9', 'Form 3', 'Form 4'))
);
CREATE INDEX students_guardian ON students (guardian_id);
