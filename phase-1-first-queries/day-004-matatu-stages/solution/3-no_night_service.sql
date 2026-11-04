-- Route number and destination of every route with no night fare.
SELECT route_no, destination FROM routes WHERE night_fare_kes IS NULL;
