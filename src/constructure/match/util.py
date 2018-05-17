# Constructure 1.0
# Bojun Wang, May 2018
# TODO FIX LIMIT 1

import apsw
import config

from model import *

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

def invalidateWorker(self, worker_id):
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("DELETE FROM MatchedWorkers WHERE worker_id1 = ? OR worker_id2 = ?", (worker_id, worker_id))
        conn.execute("DELETE FROM MatchedWorkerTeam WHERE worker_id = ?", (worker_id, ))
        conn.commit()

def invalidateTeam(self, team_id):
    with DatabaseConnection(read_only=False) as conn:
        self.begin()
        self.execute("DELETE FROM MatchedWorkerTeam WHERE team_id = ?", (team_id, ))
        self.commit()

def get_all_workers():
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT worker_id
            FROM Workers
            """)

def get_team_ids(prefix=None, place=None):
    """
    TODO: implement prefix + place filter
    """
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT team_id
            FROM Teams
            """)

def insert_match_result(worker_id1, worker_id2, score, reason):
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO MatchedWorkers
            VALUES (?, ?, ?, ?)
            """, (worker_id1, worker_id2, score, reason))
        conn.execute("""
            INSERT INTO MatchedWorkers
            VALUES (?, ?, ?, ?)
            """, (worker_id2, worker_id1, score, reason))
        conn.commit()

def insert_match_team_result(worker_id, team_id, score, reason):
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO MatchedWorkerTeam
            VALUES (?, ?, ?, ?)
            """, (worker_id, team_id, score, reason))
        conn.commit()

def get_worker_speciality(worker_id):
    with DatabaseConnection() as conn:
        (speciality_id, name) = conn.execute("""
            SELECT speciality_id, name
            FROM WorkerHasSpeciality
            JOIN Speciality USING (speciality_id)
            WHERE worker_id = ?
            LIMIT 1
            """, (worker_id, ))[0]
        print("Got worker Speciality %s %s" % (speciality_id, name))
        return Speciality(name, speciality_id=speciality_id)

def get_worker_cert(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT cert_id, name, achieved, level
            FROM WorkerHasCert
            JOIN Certificate USING (cert_id)
            WHERE worker_id = ?
            LIMIT 1
            """) 

def get_worker_info(worker_id):
    with DatabaseConnection() as conn:
        (name, age, work_age, education, hometown) = conn.execute("""
            SELECT Workers.name, age, work_age, education,
                   (SELECT Places.name FROM Places WHERE Places.place_id = Workers.place_id)
            FROM Workers
            WHERE worker_id = ?
            LIMIT 1
            """, (worker_id, ))[0]
    return Worker(name, age, work_age, education, hometown,
            worker_id).add_speciality(get_worker_speciality(worker_id))

def _form_common_date(start, end):
    if not end:
        return "%s - Now" % start
    return "%s - %s" % (start, end)

def get_workers_common_team(worker_id1, worker_id2):
    # TODO: get multiple
    same_team = ""
    with DatabaseConnection() as conn:
        result = conn.execute("""
            SELECT t.name,
            CASE WHEN a.starts < b.starts THEN b.starts ELSE a.starts END,
            CASE WHEN (a.ends IS NULL AND b.ends IS NULL) THEN NULL
                 WHEN (a.ends IS NULL) THEN b.ends
                 WHEN (b.ends IS NULL) THEN a.ends
                 WHEN (a.ends < b.ends) THEN a.ends
                 ELSE b.ends END
            FROM WorkerPartOfTeam a
            JOIN WorkerPartOfTeam b ON (a.team_id = b.team_id)
            JOIN Teams t ON (a.team_id = t.team_id)
            WHERE a.worker_id = ? AND b.worker_id = ?
            AND ((a.ends is NULL AND b.ends is NULL)
                OR (a.ends is NULL AND a.starts > b.ends)
                OR (b.ends is NULL AND b.starts > a.ends)
                OR a.ends > b.starts
                OR b.ends > a.starts)
            LIMIT 1
                """, (worker_id1, worker_id2))[0]
        if result:
            (team_name, start, end) = result
            same_team = "%s %s" % (team_name, _form_common_date(start, end))
        return same_team

def get_team_needs(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT Speciality.name
            FROM TeamNeedsSpeciality
            JOIN WorkerHasSpeciality USING (speciality_id)
            JOIN Speciality USING (speciality_id)
            WHERE TeamNeedsSpeciality.team_id = ?
            AND WorkerHasSpeciality.worker_id = ?
            AND TeamNeedsSpeciality.count > (SELECT count(worker_id)
                                             FROM WorkerPartOfTeam
                                             JOIN WorkerHasSpeciality ON (worker_id)
                                             WHERE team_id = TeamNeedsSpeciality.team_id
                                             AND speciality_id = TeamNeedsSpeciality.speciality_id)
            LIMIT 1
            """, (team_id, worker_id))[0]

def get_team_homies(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT worker_id
            FROM WorkerPartOfTeam
            JOIN Teams ON (worker_id)
            JOIN Workers ON (worker_id)
            WHERE team_id = ?
            AND ends is NULL
            AND place_id = (SELECT place_id FROM Workers WHERE worker_id = ?)
            """, (team_id, worker_id))

def get_team_ex_teammates(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT worker_id
            FROM WorkerPartOfTeam
            WHERE team_id = ?
            AND ends is NULL
            AND worker_id IN (
                SELECT b.worker_id
                FROM WorkerPartOfTeam a
                JOIN WorkerPartOfTeam b ON (a.team_id = b.team_id)
                WHERE a.worker_id = ?
                AND ((a.ends is NULL AND b.ends is NULL)
                OR (a.ends is NULL AND a.starts > b.ends)
                OR (b.ends is NULL AND b.starts > a.ends)
                OR a.ends > b.starts
                OR b.ends > a.starts)
            )
            """, (team_id, worker_id))

def get_top_matched_workers(worker_id, matched_workers, limit=10):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT (SELECT name FROM Workers
                    WHERE worker_id = MatchedWorkers.worker_id2),
                    reason
            FROM MatchedWorkers
            WHERE worker_id1 = ?
            AND worker_id2 in (%s)
            ORDER BY score DESC
            LIMIT ?
            """ % ",".join(["?" for x in matched_workers]),
            (worker_id, ) + tuple(matched_workers) + (limit, ))


def insert_place_if_not_exist(place):
    with DatabaseConnection() as conn:
        place_id = conn.execute("""
            SELECT place_id FROM Places WHERE name = ?
            """, (place, ))[0]
        if place_id:
            return place_id
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Places (name) VALUES (?)
            """, (place, ))
        place_id = conn.lastrowid()
        conn.commit()
        return place_id

def insert_speciality_if_not_exist(name):
    with DatabaseConnection() as conn:
        speciality_id = conn.execute("""
            SELECT speciality_id FROM Speciality WHERE name = ?
            """, (name, ))[0]
        if speciality_id:
            return speciality_id
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Speciality (name) VALUES (?)
            """, (name, ))
        speciality_id = conn.lastrowid()
        conn.commit()
        return speciality_id

def worker_exists(worker_id):
    with DatabaseConnection() as conn:
        return not conn.execute("""
            SELECT * FROM Workers WHERE worker_id = ?
            """, (worker_id, )) == []

def team_exists(team_id):
    with DatabaseConnection() as conn:
        return not conn.execute("""
            SELECT * FROM Teams WHERE team_id = ?
            """, (team_id, )) == []
