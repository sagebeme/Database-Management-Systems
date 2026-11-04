-- Row-level security on loans: a teller sees, and can add, only loans whose officer is themselves; the auditor
-- sees every loan. (The table owner is not affected.)
ALTER TABLE loans ENABLE ROW LEVEL SECURITY;
CREATE POLICY own_loans ON loans TO sacco_teller, sacco_teller2
    USING (officer = current_user) WITH CHECK (officer = current_user);
CREATE POLICY auditor_reads_all ON loans FOR SELECT TO sacco_auditor USING (true);
