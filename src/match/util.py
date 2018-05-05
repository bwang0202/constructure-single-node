import apsw

import config

def longest_common_prefix(seq1, seq2):
    start = 0
    while start < min(len(seq1), len(seq2)):
        if seq1[start] != seq2[start]:
            break
        start += 1
    return seq1[:start]

class SqliteDatabaseConnection(object):
    """
    **Case 1**: You want to run a single query in a transaction

    Just use conn.execute()

    **Case 2**: You want to run > 1 queries in a transaction.
    In this case, structure your code as follows

    try:
        with ConfigDatabaseConnection as conn
        conn.begin()
        try
            conn.execute(query1)
            conn.execute(query2)
            ...
            conn.execute(quern)
            conn.commit() // no error, lets commit
        exception as e:
            conn.rollback() //error during query processing. Even commit() might throw an error
    except CipherBucketOpenDatabaseError as dberr:
        log error -- this was error while opening db by new conn() or error in begin()

    """

    def __init__(self, db_path, read_only=True):
        super(SqliteDatabaseConnection, self).__init__()
        self._conn = None
        self._cur = None
        self._db_retry_sleep = 1
        self._db_path = db_path
        self._read_only = read_only

    def __enter__(self):
        kwargs = {'flags': apsw.SQLITE_OPEN_READONLY} if self._read_only else {}
        self._conn = apsw.Connection(self._db_path, **kwargs)
        # Set the amount of time to automatically retry in case
        # db is locked
        self._conn.setbusytimeout(self._db_retry_sleep * 1000)
        return self

    def __exit__(self, *args):
        self._conn.close()

    def cursor(self):
        """Cursor to the database."""
        if self._cur is None:
            self._cur = self._conn.cursor()
        return self._cur;

    def begin(self):
        """Start a transaction."""
        if self._read_only:
            self.cursor().execute("BEGIN;")
        else:
            self.cursor().execute("BEGIN IMMEDIATE;")

    def begin(self):
        """Start a transaction."""
        self.cursor().execute("BEGIN IMMEDIATE;")

    def commit(self):
        """Commit a transaction."""
        self.cursor().execute("COMMIT;")

    def rollback(self):
        """Start a transaction."""
        self.cursor().execute("ROLLBACK;")

    def execute(self, *args, **kwargs):
        return self.cursor().execute(*args, **kwargs).fetchall()

    def lastrowid(self):
        return self._conn.last_insert_rowid();


def get_worker_info(worker_id):

def get_workers_experience(worker_id1, worker_id2):
	