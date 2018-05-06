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

class DatabaseConnection(SqliteDatabaseConnection):
    def __init__(self, read_only=True):
        super(DatabaseConnection, self).__init__(config.db_path, read_only)

def get_worker_speciality(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT speciality_id, name
            FROM WorkerHasSpeciality
            JOIN Speciality USING (speciality_id)
            WHERE worker_id = ?
            """, (worker_id, ))

def get_worker_cert(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT cert_id, name, level, achieved
            FROM WorkerHasCert
            JOIN Certificate USING (cert_id)
            WHERE worker_id = ?
            """)

def get_worker_info(worker_id):
    with DatabaseConnection() as conn:
        conn.execute("""
            SELECT Workers.name, age, work_age, education,
                   (SELECT Places.name FROM Places WHERE Places.place_id = Workers.place_id)
            FROM Workers
            WHERE worker_id = ?
            LIMIT 1
            """, (worker_id, ))[0] + (get_worker_speciality(worker_id), get_worker_cert(worker_id))

def get_workers_common_experience(worker_id1, worker_id2):

    SELECT count(*)
    FROM WorkerPartOfTeam a
    JOIN WorkerPartOfTeam b ON (a.team_id = b.team_id)
    WHERE a.worker_id = ? AND b.worker_id = ?
    AND ((a.ends is NULL AND b.ends is NULL)
        OR (a.ends is NULL AND a.starts > b.ends)
        OR (b.ends is NULL AND b.starts > a.ends)
        OR a.ends > b.starts
        OR b.ends > a.starts)

    SELECT count(*)
    FROM WorkerPartOfTeam
    WHERE worker_id = ?

    SELECT count(*)
    FROM ParticipateProject a
    JOIN ParticipateProject b ON (a.project_id = b.project_id)
    WHERE a.worker_id = ? AND b.worker_id = ?
    AND a.team_id <> b.team_id # DONT double count
    AND ((a.ends is NULL AND b.ends is NULL)
        OR (a.ends is NULL AND a.starts > b.ends)
        OR (b.ends is NULL AND b.starts > a.ends)
        OR a.ends > b.starts
        OR b.ends > a.starts)

    SELECT count(*)
    FROM ParticipateProject
    WHERE worker_id = ?

    SELECT count(*)
    FROM WorkerKnowsWorker
    WHERE (worker_id1 = ? AND worker_id2 = ?) OR (worker_id1 = ? AND worker_id2 = ?)
    LIIMIT 1

def get_team_needs(worker_id, team_id):
    worker_specialities = get_worker_speciality(worker_id)

    for x in worker_specialities:
    SELECT count(*)
    FROM TeamNeedsSpeciality
    WHERE team_id = ?
    AND speciality_id = ?
    AND count < (SELECT count(worker_id) FROM WorkerPartOfTeam JOIN WorkerHasSpeciality ON (worker_id) WHERE speciality_id = ?)








