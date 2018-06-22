# -*- coding: utf8 -*-

# Constructure 1.0
# Bojun Wang, May 2018
# TODO FIX LIMIT 1

import apsw
import config

from model import *
from match import *

class ResouceNotFound(Exception):
    pass

class Speciality:
    def __init__(self, name, speciality_id=None):
        self.name = name
        self.speciality_id = speciality_id
    def __str__(self):
        return self.name

class Worker:
    def __init__(self, name, pwd, card_id, picture, hometown, speciality, worker_id=None):
        self.name = name
        self.picture = picture
        self.pwd = pwd
        self.card_id = card_id
        self.hometown = hometown
        self.speciality = speciality
        self.worker_id = worker_id
    def __str__(self):
        strs = [self.name, self.speciality, "ID %s" % self.card_id[-4:]]
        return ", ".join(strs)

class Team:
    def __init__(self, name, pwd, registration_id, picture, team_id=None):
        self.name = name
        self.pwd = pwd
        self.registration_id = registration_id
        self.picture = picture
        self.team_id = team_id
    def __str__(self):
        return self.name

def add_worker(worker):
    # Insert hometown if necessary
    place_id = insert_place_if_not_exist(worker.hometown)

    # Insert worker
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Workers (name, card_id, pwd, place_id, picture)
            VALUES (?, ?, ?, ?, ?)
            """, (worker.name, worker.card_id, worker.pwd, place_id, worker.picture))
        worker_id = conn.lastrowid()
        conn.commit()

    # Insert speciality if necessary
    speciality_id = insert_speciality_if_not_exist(worker.speciality.name)
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO WorkerHasSpeciality (worker_id, speciality_id)
            VALUES (?, ?)
            """, (worker_id, speciality_id))
        conn.commit()

    return worker_id

def add_team(team):
    # insert team
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Teams (name, pwd, registration_id, picture)
            VALUES (?, ?, ?, ?)
            """, (team.name, team.pwd, team.registration_id, team.picture))
        team_id = conn.lastrowid()
        conn.commit()

        return team_id

def get_worker_certified(worker_id):
    with DatabaseConnection() as conn:
        certified = conn.execute("""
            SELECT certified FROM Workers WHERE worker_id = ?
            """, (worker_id, ))
        return str(certified).lower() == "true"

def api_time_to_db(time):
    # TODO: db compatible
    return time

def db_time_to_api(time):
    timestr = str(time)
    # TODO: strip to 2000-01-01
    return timestr

def get_worker_experience(worker_id):
    worker_experiences = []
    with DatabaseConnection() as conn:
        for (team_name, project_name, start, end) in conn.execute("""
            SELECT Teams.name, Projects.name, starts, ends
            FROM WorkerTeamProject
            JOIN Teams USING (team_id)
            JOIN Projects USING (project_id)
            WHERE worker_id = ?
            """, (worker_id, )):
            worker_experiences.append({'team': team_name, 'project': project_name,
                'start': process_time(start), 'end': process_time(end)})
    return worker_experiences


def add_worker_team_project(worker_id, team_name, project_name, starts, ends=None):
    # validate worker, team, project
    worker_id = worker_exists(worker_id)
    team_id = team_exists(team_name)
    project_id = project_exists(project_name)

    # Insert
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO WorkerTeamProject (worker_id, team_id, project_id, starts, ends)
            VALUES (?, ?, ?, ?, ?)
            """, (worker_id, team_id, project_id, starts, ends))
        conn.commit()

def get_teams(place=None, prefix=None):
    with DatabaseConnection() as conn:
        result = conn.execute("""
            SELECT team_id, name FROM Teams
            """)
    return [{'team_id': x[0], 'name': x[1]} for x in result]

def get_workers():
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT worker_id, name, age, education, (SELECT name FROM Places WHERE place_id = Workers.place_id)
            FROM Workers
            """)


def get_matched_workers(worker_id, limit=10):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT worker_id2, name, score, reason
            FROM MatchedWorkers
            JOIN Workers ON (worker_id2 = worker_id)
            WHERE worker_id1 = ?
            ORDER BY score DESC
            LIMIT ?
            """, (worker_id, limit, ))

def get_team_matched_workers(team_id, limit=10):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT Workers.worker_id, Workers.name, picture, score, reason
            FROM MatchedWorkerTeam
            JOIN Workers USING (worker_id)
            WHERE team_id = ?
            ORDER BY score DESC
            LIMIT ?
            """, (team_id, limit))

def get_team_projects(team_id, limit=5):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT project_id, name, picture
            FROM Projects
            WHERE project_id IN (SELECT DISTINCT project_id
                                 FROM WorkerTeamProject
                                 WHERE team_id = ?
                                 LIMIT ?)
            """, (team_id, limit))

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

def get_workers_same_experience(worker_id1, worker_id2):
    # TODO: get multiple
    same_team = "曾合作"
    with DatabaseConnection() as conn:
        result = conn.execute("""
            SELECT t.name, p.name
            CASE WHEN a.starts < b.starts THEN b.starts ELSE a.starts END,
            CASE WHEN (a.ends IS NULL AND b.ends IS NULL) THEN NULL
                 WHEN (a.ends IS NULL) THEN b.ends
                 WHEN (b.ends IS NULL) THEN a.ends
                 WHEN (a.ends < b.ends) THEN a.ends
                 ELSE b.ends END
            FROM WorkerTeamProject a
            JOIN WorkerTeamProject b ON (a.team_id = b.team_id)
            JOIN Teams t ON (t.team_id = a.team_id)
            JOIN Projects p ON (p.project_id = a.project_id)
            WHERE b.project_id = p.project_id
            AND a.worker_id = ? AND b.worker_id = ?
            AND ((a.ends is NULL AND b.ends is NULL)
                OR (a.ends is NULL AND a.starts < b.ends)
                OR (b.ends is NULL AND b.starts < a.ends)
                OR (a.ends > b.starts AND a.starts < b.ends)
                OR (b.ends > a.starts AND b.starts < a.ends))
            LIMIT 1
                """, (worker_id1, worker_id2))
        if len(result) == 0:
            return None
        return same_team

def get_team_needs(worker_id, team_id):
    with DatabaseConnection() as conn:
        result = conn.execute("""
            SELECT Speciality.name
            FROM TeamNeedsSpeciality
            JOIN WorkerHasSpeciality USING (speciality_id)
            JOIN Speciality USING (speciality_id)
            WHERE TeamNeedsSpeciality.team_id = ?
            AND WorkerHasSpeciality.worker_id = ?
            AND TeamNeedsSpeciality.count > (SELECT count(WorkerPartOfTeam.worker_id)
                                             FROM WorkerPartOfTeam
                                             JOIN WorkerHasSpeciality USING (worker_id)
                                             WHERE team_id = TeamNeedsSpeciality.team_id
                                             AND speciality_id = TeamNeedsSpeciality.speciality_id
                                             AND ends IS NULL)
            LIMIT 1
            """, (team_id, worker_id))
        if result:
            return result[0]
        return None

def get_team_homies(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT Workers.worker_id
            FROM WorkerPartOfTeam
            JOIN Teams USING (team_id)
            JOIN Workers USING (worker_id)
            WHERE team_id = ?
            AND ends is NULL
            AND place_id = (SELECT place_id FROM Workers WHERE Workers.worker_id = ?)
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
                OR (a.ends is NULL AND a.starts < b.ends)
                OR (b.ends is NULL AND b.starts < a.ends)
                OR (a.ends > b.starts AND a.starts < b.ends)
                OR (b.ends > a.starts AND b.starts < a.ends))
            )
            """, (team_id, worker_id))

def get_top_matched_workers(worker_id, matched_workers, limit=3):
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


####### UTIL FUNCS ###############################################

def insert_place_if_not_exist(place):
    with DatabaseConnection() as conn:
        place_id = conn.execute("""
            SELECT place_id FROM Places WHERE name = ?
            """, (place, ))
        if len(place_id) > 0:
            return place_id[0][0]
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
            """, (name, ))
        if len(speciality_id) > 0:
            return speciality_id[0][0]
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
        if conn.execute("""
            SELECT * FROM Workers WHERE worker_id = ?
            """, (worker_id, )) == []:
            raise ResouceNotFound("Worker %s not found" % worker_id)
    return worker_id

def team_exists(team_name):
    with DatabaseConnection() as conn:
        team_id = conn.execute("""
            SELECT team_id FROM Teams WHERE name = ?
            """, (team_name, ))
        if len(team_id) == 0:
            raise ResouceNotFound("Team %s not found" % team_name)
        return team_id[0]

def project_exists(project_name):
    with DatabaseConnection() as conn:
        project_id = conn.execute("""
            SELECT project_id FROM Projects WHERE name = ?
            """, (project_name,))
        if len(project_id) == 0:
            raise ResouceNotFound("Project %s not found" % project_name)
        return project_id[0]

