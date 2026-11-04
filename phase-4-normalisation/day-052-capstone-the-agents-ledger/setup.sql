-- Three M-Pesa agents' ledgers, typed into one spreadsheet over three days (invented people, tills and
-- commission rates; real codes look like these but aren't these). Everything came in as text.
--   tools/mysql.sh ledger < phase-4-normalisation/day-052-capstone-the-agents-ledger/setup.sql
DROP TABLE IF EXISTS transactions, customers, agents, ledger_raw;
CREATE TABLE ledger_raw (
    code VARCHAR(20),
    date_time VARCHAR(20),
    till VARCHAR(10),
    agent_name VARCHAR(60),
    location VARCHAR(60),
    phone VARCHAR(20),
    customer_name VARCHAR(60),
    txn_type VARCHAR(20),
    amount VARCHAR(20),
    commission VARCHAR(10)
);
INSERT INTO ledger_raw VALUES
    ('TJYA9FPUJV', '01/10/2026 09:02', '512377', ' Baraka Mobile Shop  ', 'Githurai 45', '0701000606', 'Hassan Ali', 'Withdrawal ', '200', '15'),
    ('TJYR6THVU1', '01/10/2026 11:40', '600218', 'Kilimani Cyber', 'Kilimani', '0768 000 707', 'Njeri Wambui ', 'deposit', '12,000', '50'),
    ('TJHV3GOWID', '01/10/2026 11:48', '512340', 'Mama Lucy Agencies ', 'Kawangware', '254745000505', 'Akinyi Atieno  ', 'deposit', '7,500', '50'),
    ('TJHT0A3FHN', '01/10/2026 12:55', '512377', 'Baraka Mobile Shop', 'Githurai 45', '0110000404', ' Mutua Musyoka', 'Deposit ', '7,500', '50'),
    ('TJ08Z32F45', '01/10/2026 13:05', '600218', 'Kilimani Cyber', 'Kilimani', '0110000404', 'Mutua Musyoka', 'Deposit', '3000', '25'),
    ('TJPUNXQMIF', '01/10/2026 15:20', '512377', 'Baraka Mobile Shop  ', 'Githurai 45', '+254712000101', 'Wanjiku Kamau', 'Deposit ', '1,000', '10'),
    ('TJ4GHV01BO', '01/10/2026 16:10', '512377', ' Baraka Mobile Shop', 'Githurai 45', '0733 000 303', ' Chebet Rono ', 'Deposit ', '5,000', '25'),
    ('TJTQX194A4', '01/10/2026 18:07', '512377', ' Baraka Mobile Shop ', 'Githurai 45', '0701000606', ' Hassan Ali', 'deposit', '7,500', '50'),
    ('TJNMHGDI00', '01/10/2026 18:42', '600218', 'Kilimani Cyber  ', 'Kilimani', '254110000404', ' Mutua Musyoka ', 'withdrawal', '750', '15'),
    ('TJEJCAXQEZ', '01/10/2026 18:47', '512340', 'Mama Lucy Agencies', 'Kawangware', '0722 000 202', ' Otieno Ouma', 'withdrawal', '750', '15'),
    ('TJY6AJT3CL', '01/10/2026 18:47', '600218', 'Kilimani Cyber', 'Kilimani', '0722000202', 'Otieno Ouma  ', 'deposit', '750', '10'),
    ('TJVPNAKH41', '02/10/2026 10:04', '600218', ' Kilimani Cyber ', 'Kilimani', '+254722000202', 'Otieno Ouma', 'DEPOSIT', '3,000', '25'),
    ('TJ88ADV99E', '02/10/2026 12:36', '600218', 'Kilimani Cyber  ', 'Kilimani', '+254745000505', ' Akinyi Atieno  ', 'deposit', '1,500', '25'),
    ('TJLRFUL11B', '02/10/2026 14:08', '512340', ' Mama Lucy Agencies', 'Kawangware', '+254712000101', 'Wanjiku Kamau ', 'deposit', '7500', '50'),
    ('TJRD64X0CI', '02/10/2026 14:40', '512340', 'Mama Lucy Agencies  ', 'Kawangware', '0768 000 707', 'Njeri Wambui ', 'Deposit ', '750', '10'),
    ('TJUXXSAKZQ', '02/10/2026 18:11', '512340', ' Mama Lucy Agencies', 'Kawangware', '0110 000 404', ' Mutua Musyoka', 'Deposit ', '200', '10'),
    ('TJKHLFINTM', '03/10/2026 09:47', '600218', ' Kilimani Cyber  ', 'Kilimani', '+254745000505', 'Akinyi Atieno  ', 'DEPOSIT', '500', '10'),
    ('TJ42NEQDSQ', '03/10/2026 10:13', '600218', 'Kilimani Cyber', 'Kilimani', '+254722000202', 'Otieno Ouma  ', 'DEPOSIT', '2,500', '25'),
    ('TJ7S7R1F3I', '03/10/2026 10:16', '600218', 'Kilimani Cyber', 'Kilimani', '0712 000 101', 'Wanjiku Kamau', 'Deposit', '12000', '50'),
    ('TJAC8Y2APE', '03/10/2026 11:31', '512340', 'Mama Lucy Agencies ', 'Kawangware', '0722000202', ' Otieno Ouma  ', 'deposit', '1,000', '10'),
    ('TJRA2L52LV', '03/10/2026 15:17', '512340', 'Mama Lucy Agencies', 'Kawangware', '+254110000404', 'Mutua Musyoka  ', 'WITHDRAWAL', '5,000', '40'),
    ('TJTT68H8VY', '03/10/2026 15:32', '600218', 'Kilimani Cyber ', 'Kilimani', '+254110000404', ' Mutua Musyoka ', 'deposit', '750', '10'),
    ('TJNJ6O2JP7', '03/10/2026 17:12', '600218', ' Kilimani Cyber  ', 'Kilimani', '254768000707', 'Njeri Wambui ', 'withdrawal', '3,000', '40'),
    ('TJ50HCYFZX', '03/10/2026 17:33', '600218', ' Kilimani Cyber', 'Kilimani', '0722000202', 'Otieno Ouma  ', 'Deposit', '3,000', '25');
