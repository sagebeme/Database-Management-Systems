-- Passwords for the members' app. Never store a password, only a slow, salted hash of it (bcrypt, from pgcrypto).
-- A table member_logins (member_id INT primary key referencing members, password_hash TEXT NOT NULL), and two functions:
--   set_password(member INT, password TEXT) RETURNS void: stores the bcrypt hash of the password (cost 10), replacing any
--     old one. It refuses passwords shorter than 8 characters with an error. Only the owner may call it.
--   check_password(member INT, password TEXT) RETURNS boolean: true if the password is that member's, false otherwise
--     (also false, not NULL, for a member with no password). Tellers may call it, though they can't read member_logins.
-- Nobody but the owner can read member_logins, not even the auditor.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE member_logins (
    member_id INT PRIMARY KEY REFERENCES members (id),
    password_hash TEXT NOT NULL
);

CREATE FUNCTION set_password(member INT, password TEXT) RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    IF length(password) < 8 THEN
        RAISE EXCEPTION 'a password needs at least 8 characters';
    END IF;
    INSERT INTO member_logins (member_id, password_hash)
    VALUES (member, crypt(password, gen_salt('bf', 10)))
    ON CONFLICT (member_id) DO UPDATE SET password_hash = EXCLUDED.password_hash;
END;
$$;

-- crypt(password, stored_hash) reads the salt and cost back out of the stored hash, so hashing the attempt the same
-- way and comparing tells you if it matches. SECURITY DEFINER lets a teller check without reading the table.
CREATE FUNCTION check_password(member INT, password TEXT) RETURNS boolean
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public
AS $$
    SELECT coalesce((SELECT password_hash = crypt(password, password_hash)
                     FROM member_logins WHERE member_id = member), false);
$$;

-- Every new function can be run by everyone (PUBLIC) until you say otherwise.
REVOKE EXECUTE ON FUNCTION set_password(INT, TEXT), check_password(INT, TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_password(INT, TEXT) TO sacco_teller, sacco_teller2;
