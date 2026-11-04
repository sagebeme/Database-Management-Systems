-- An audit trail. A table audit_log (id identity primary key, at TIMESTAMPTZ default now(), who TEXT, action TEXT,
-- loan_id INT, old JSONB, new JSONB, the four of who, action, at and id required), and a trigger loans_audit that adds
-- a row for every INSERT, UPDATE and DELETE on loans: who is the user who made the change, action is the operation
-- (INSERT, UPDATE or DELETE), old and new are the row before and after as JSON (NULL where there is none).
-- It must work for a teller, who has no rights on audit_log at all. The auditor can read audit_log.
CREATE TABLE audit_log (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    at TIMESTAMPTZ NOT NULL DEFAULT now(),
    who TEXT NOT NULL,
    action TEXT NOT NULL,
    loan_id INT,
    old JSONB,
    new JSONB
);
CREATE FUNCTION audit_loans() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
BEGIN
    INSERT INTO audit_log (who, action, loan_id, old, new)
    VALUES (session_user, TG_OP, COALESCE(NEW.id, OLD.id),
            CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE to_jsonb(OLD) END,
            CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE to_jsonb(NEW) END);
    RETURN COALESCE(NEW, OLD);
END $$;
CREATE TRIGGER loans_audit AFTER INSERT OR UPDATE OR DELETE ON loans
FOR EACH ROW EXECUTE FUNCTION audit_loans();
GRANT SELECT ON audit_log TO sacco_auditor;
