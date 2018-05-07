# Constructure 1.0
# Bojun Wang, May 2018

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
    with DatabaseConnection() as conn:
        same_team = conn.execute("""
            SELECT t.name, a.starts, a.ends, b.starts, b.ends
            FROM WorkerPartOfTeam a
            JOIN WorkerPartOfTeam b ON (a.team_id = b.team_id)
            JOIN Teams t ON (a.team_id = t.team_id)
            WHERE a.worker_id = ? AND b.worker_id = ?
            AND ((a.ends is NULL AND b.ends is NULL)
                OR (a.ends is NULL AND a.starts > b.ends)
                OR (b.ends is NULL AND b.starts > a.ends)
                OR a.ends > b.starts
                OR b.ends > a.starts)
                """, (worker_id1, worker_id2))
        total_team1 = conn.execute("""  
            SELECT count(*)
            FROM WorkerPartOfTeam
            WHERE worker_id = ? """, (worker_id1, ))[0]
        total_team2 = conn.execute("""
            SELECT count(*)
            FROM WorkerPartOfTeam
            WHERE worker_id = ? """, (worker_id2, ))[0]

        same_project = conn.execute("""
            SELECT p.name, (SELECT name FROM Places WHERE place_id = p.place_id), a.starts, a.ends, b.starts, b.ends
            FROM ParticipateProject a
            JOIN ParticipateProject b ON (a.project_id = b.project_id)
            JOIN Projects p ON (a.project_id = p.project_id)
            WHERE a.worker_id = ? AND b.worker_id = ?
            AND a.team_id <> b.team_id
            AND ((a.ends is NULL AND b.ends is NULL)
                OR (a.ends is NULL AND a.starts > b.ends)
                OR (b.ends is NULL AND b.starts > a.ends)
                OR a.ends > b.starts
                OR b.ends > a.starts)
            """, (worker_id1, worker_id2))
        total_projects1 = conn.execute("""
            SELECT count(*)
            FROM ParticipateProject
            WHERE worker_id = ?
            """, (worker_id1, ))[0]
        total_projects2 = conn.execute("""
            SELECT count(*)
            FROM ParticipateProject
            WHERE worker_id = ?
            """, (worker_id2, ))[0]

        personal_relations = conn.execute("""
            SELECT worker_id1, notes
            FROM WorkerKnowsWorker
            WHERE (worker_id1 = ? AND worker_id2 = ?) OR (worker_id1 = ? AND worker_id2 = ?)
            """, (worker_id1, worker_id2, worker_id2, worker_id1))

        return (same_team, total_team1, total_team2, same_project, total_projects1, total_projects2, personal_relations)


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
            """, (team_id, worker_id))

def get_team_workers_comp(worker_id, team_id):
    team_worker_ids = []
    with DatabaseConnection() as conn:
        team_worker_ids = conn.execute("""
            SELECT worker_id FROM WorkerPartOfTeam WHERE team_id = ?
            """, (team_id, ))

    _string = "(%s)" % ", ".join("?" for x in team_worker_ids)
    _tuple = tuple([x[0] for x in team_worker_ids])
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT avg(score)
            FROM MatchedWorkers
            WHERE (worker_id1 = ? AND worker_id2 in %s)
            OR (worker_id2 = ? AND worker_id1 in %s) 
            """ % (_string, _string), (worker_id, _tuple, worker_id, _tuple))
