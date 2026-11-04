-- A table payments like payments_old (id BIGINT, paid_on DATE, phone TEXT, amount INT, all required), partitioned
-- by range on paid_on, with the primary key (id, paid_on); and four partitions: payments_2026_01,
-- payments_2026_02 and payments_2026_03 for those months, and payments_default for any other date.
CREATE TABLE payments (
    id BIGINT NOT NULL,
    paid_on DATE NOT NULL,
    phone TEXT NOT NULL,
    amount INT NOT NULL,
    PRIMARY KEY (id, paid_on)
) PARTITION BY RANGE (paid_on);
CREATE TABLE payments_2026_01 PARTITION OF payments FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE payments_2026_02 PARTITION OF payments FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE payments_2026_03 PARTITION OF payments FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE payments_default PARTITION OF payments DEFAULT;
