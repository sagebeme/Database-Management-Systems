-- Day 96: the SACCO's tables.

CREATE TABLE members (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name      text NOT NULL CHECK (btrim(name) <> ''),
    phone     text NOT NULL UNIQUE CHECK (phone ~ '^254[17][0-9]{8}$'),
    joined_on date NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE ledger (
    id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id integer NOT NULL REFERENCES members (id),
    kind      text NOT NULL CHECK (kind IN ('deposit', 'withdrawal')),
    amount    bigint NOT NULL CHECK (amount > 0),
    at        timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ledger_member ON ledger (member_id, at);

CREATE TABLE loans (
    id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id integer NOT NULL REFERENCES members (id),
    principal bigint NOT NULL CHECK (principal > 0),
    balance   bigint NOT NULL CHECK (balance >= 0),
    status    text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'cleared')),
    issued_at timestamptz NOT NULL DEFAULT now(),
    CHECK ((status = 'cleared') = (balance = 0))
);
-- At most one active loan per member.
CREATE UNIQUE INDEX one_active_loan ON loans (member_id) WHERE status = 'active';

CREATE TABLE guarantees (
    loan_id   integer NOT NULL REFERENCES loans (id),
    member_id integer NOT NULL REFERENCES members (id),
    amount    bigint NOT NULL CHECK (amount > 0),
    PRIMARY KEY (loan_id, member_id)
);
CREATE INDEX guarantees_member ON guarantees (member_id);

CREATE TABLE repayments (
    id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loan_id integer NOT NULL REFERENCES loans (id),
    amount  bigint NOT NULL CHECK (amount > 0),
    at      timestamptz NOT NULL DEFAULT now()
);
