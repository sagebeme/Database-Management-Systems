-- Code and kind of every transaction that is neither airtime nor under 50 bob.
SELECT code, kind FROM transactions WHERE NOT (kind = 'Airtime' OR amount < 50);
