-- Kata: Change the Locks. rw_reader's password leaked. Change it to rw_reader_new.
ALTER USER 'rw_reader'@'%' IDENTIFIED BY 'rw_reader_new';
