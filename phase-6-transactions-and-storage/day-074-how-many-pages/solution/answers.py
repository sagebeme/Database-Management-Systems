"""Day 74: how many pages. Replace each None."""

# A file of 30,000 records of 100 bytes, in blocks of 1,024 bytes, sorted on its key; index entries of 15 bytes.
BLOCKING_FACTOR = 10
DATA_BLOCKS = 3000
INDEX_ENTRIES_PER_BLOCK = 68
# A primary index has one entry per data block. How many blocks does its first level take?
PRIMARY_INDEX_BLOCKS = 45

# True or False
A_PRIMARY_INDEX_IS_SPARSE = True
A_SECONDARY_INDEX_ON_A_KEY_IS_DENSE = True
A_FILE_CAN_HAVE_MORE_THAN_ONE_PRIMARY_INDEX = False
