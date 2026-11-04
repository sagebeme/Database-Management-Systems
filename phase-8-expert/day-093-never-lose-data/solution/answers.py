"""Day 93: never lose data. Replace each None."""

# Backups run every night at 02:00. The disk dies at 17:00, before that night's backup.
# How many hours of changes are lost with backups alone? (That's the recovery point.)
HOURS_LOST = 15

# True or False
A_REPLICA_IS_A_BACKUP = False
A_BACKUP_YOU_HAVE_NEVER_RESTORED_IS_PROVEN = False
WITH_WAL_ARCHIVING_YOU_CAN_RESTORE_TO_ANY_MOMENT = True
ASYNCHRONOUS_REPLICATION_CAN_LOSE_COMMITTED_TRANSACTIONS = True

# "RPO" or "RTO": the name for how long the system may be down while you recover.
TIME_TO_RECOVER_IS_CALLED = "RTO"
