-- Day 96: the rules, as functions. Every money-moving function locks the member's row first.

CREATE FUNCTION savings(p_member integer) RETURNS bigint
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(sum(CASE kind WHEN 'deposit' THEN amount ELSE -amount END), 0)::bigint
    FROM ledger WHERE member_id = p_member;
$$;

CREATE FUNCTION guaranteed(p_member integer) RETURNS bigint
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(sum(g.amount), 0)::bigint
    FROM guarantees g JOIN loans l ON l.id = g.loan_id
    WHERE g.member_id = p_member AND l.status = 'active';
$$;

CREATE FUNCTION free_savings(p_member integer) RETURNS bigint
LANGUAGE sql STABLE AS $$
    SELECT savings(p_member) - guaranteed(p_member);
$$;

CREATE FUNCTION lock_member(p_member integer) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    PERFORM 1 FROM members WHERE id = p_member FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'no such member %', p_member;
    END IF;
END;
$$;

CREATE FUNCTION deposit(p_member integer, p_amount bigint) RETURNS bigint
LANGUAGE plpgsql AS $$
BEGIN
    PERFORM lock_member(p_member);
    INSERT INTO ledger (member_id, kind, amount) VALUES (p_member, 'deposit', p_amount);
    RETURN savings(p_member);
END;
$$;

CREATE FUNCTION withdraw(p_member integer, p_amount bigint) RETURNS bigint
LANGUAGE plpgsql AS $$
BEGIN
    PERFORM lock_member(p_member);
    IF p_amount > free_savings(p_member) THEN
        RAISE EXCEPTION 'insufficient savings: % free', free_savings(p_member);
    END IF;
    INSERT INTO ledger (member_id, kind, amount) VALUES (p_member, 'withdrawal', p_amount);
    RETURN savings(p_member);
END;
$$;

CREATE FUNCTION issue_loan(p_member integer, p_principal bigint,
                           p_guarantors integer[], p_amounts bigint[]) RETURNS integer
LANGUAGE plpgsql AS $$
DECLARE
    loan integer;
    covered bigint;
    g integer;
    i integer;
BEGIN
    IF cardinality(p_guarantors) IS DISTINCT FROM cardinality(p_amounts) THEN
        RAISE EXCEPTION 'guarantors and amounts differ in length';
    END IF;
    IF p_member = ANY (p_guarantors) THEN
        RAISE EXCEPTION 'a member cannot guarantee their own loan';
    END IF;
    -- Lock everyone involved in id order, so two loans sharing guarantors can't deadlock.
    FOR g IN SELECT DISTINCT x FROM unnest(p_guarantors || p_member) AS x ORDER BY x LOOP
        PERFORM lock_member(g);
    END LOOP;
    IF (SELECT count(DISTINCT x) FROM unnest(p_guarantors) x) <> cardinality(p_guarantors) THEN
        RAISE EXCEPTION 'a guarantor is listed twice';
    END IF;
    IF EXISTS (SELECT 1 FROM loans WHERE member_id = p_member AND status = 'active') THEN
        RAISE EXCEPTION 'member % already has an active loan', p_member;
    END IF;
    IF p_principal > 3 * savings(p_member) THEN
        RAISE EXCEPTION 'loan limit is three times savings (%)', 3 * savings(p_member);
    END IF;
    covered := savings(p_member) + COALESCE((SELECT sum(x) FROM unnest(p_amounts) x), 0);
    IF covered < p_principal THEN
        RAISE EXCEPTION 'guarantees do not cover the loan: % short', p_principal - covered;
    END IF;
    FOR i IN 1 .. COALESCE(cardinality(p_guarantors), 0) LOOP
        IF p_amounts[i] > free_savings(p_guarantors[i]) THEN
            RAISE EXCEPTION 'guarantor % has only % free', p_guarantors[i], free_savings(p_guarantors[i]);
        END IF;
    END LOOP;
    INSERT INTO loans (member_id, principal, balance)
    VALUES (p_member, p_principal, p_principal + p_principal / 10)
    RETURNING id INTO loan;
    INSERT INTO guarantees (loan_id, member_id, amount)
    SELECT loan, x.m, x.a FROM unnest(p_guarantors, p_amounts) AS x (m, a);
    RETURN loan;
END;
$$;

CREATE FUNCTION repay(p_loan integer, p_amount bigint) RETURNS bigint
LANGUAGE plpgsql AS $$
DECLARE
    left_to_pay bigint;
BEGIN
    SELECT balance INTO left_to_pay FROM loans WHERE id = p_loan FOR UPDATE;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'no such loan %', p_loan;
    END IF;
    IF p_amount > left_to_pay THEN
        RAISE EXCEPTION 'overpayment: only % owed', left_to_pay;
    END IF;
    INSERT INTO repayments (loan_id, amount) VALUES (p_loan, p_amount);
    UPDATE loans SET balance = balance - p_amount,
                     status = CASE WHEN balance = p_amount THEN 'cleared' ELSE status END
    WHERE id = p_loan
    RETURNING balance INTO left_to_pay;
    RETURN left_to_pay;
END;
$$;
