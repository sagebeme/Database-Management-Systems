-- Route number and sacco of every route not run by Neema Line.
SELECT route_no, sacco FROM routes WHERE sacco <> 'Neema Line';
