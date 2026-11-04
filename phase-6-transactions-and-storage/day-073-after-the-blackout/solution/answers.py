"""Day 73: after the blackout. Replace each None."""

# True or False
UNDO_LOGGING_NEEDS_THE_NEW_VALUE_IN_THE_LOG = False
REDO_LOGGING_LETS_UNCOMMITTED_CHANGES_REACH_DISK = False
UNDO_REDO_LOGGING_LETS_DIRTY_PAGES_BE_WRITTEN_WHENEVER_THE_BUFFER_POOL_LIKES = True
A_CHECKPOINT_MEANS_RECOVERY_CAN_SKIP_PART_OF_THE_LOG = True
RECOVERY_MUST_BE_SAFE_TO_RUN_TWICE = True

# The InnoDB setting that, at 1 (its default), flushes the redo log to disk at every commit.
SETTING_THAT_FLUSHES_THE_LOG_AT_COMMIT = "innodb_flush_log_at_trx_commit"
