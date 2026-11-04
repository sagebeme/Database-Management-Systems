-- 003: M-Pesa payments against invoices. Money is never updated or deleted, only added.

CREATE TABLE payments (
    id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    invoice_id    integer NOT NULL REFERENCES invoices (id),
    mpesa_receipt text NOT NULL UNIQUE CHECK (mpesa_receipt ~ '^[A-Z0-9]{10}$'),
    amount        integer NOT NULL CHECK (amount > 0),
    paid_at       timestamptz NOT NULL
);
CREATE INDEX payments_invoice ON payments (invoice_id);
CREATE INDEX payments_paid_at ON payments (paid_at);
