-- rw_app must stop adding rows to riverwood_ops. Take that one privilege away and leave the rest.
REVOKE INSERT ON riverwood_ops.* FROM 'rw_app'@'%';
