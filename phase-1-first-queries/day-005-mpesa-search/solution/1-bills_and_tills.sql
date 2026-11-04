-- Code, kind and counterparty of every Paybill or Till payment, using IN.
SELECT code, kind, counterparty FROM transactions WHERE kind IN ('Paybill', 'Till');
