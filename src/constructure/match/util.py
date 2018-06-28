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

class DuplicateResource(Exception):
    pass

class InvalidCredential(Exception):
    pass

class Specialty:
    def __init__(self, name, specialty_id=None):
        self.name = name
        self.specialty_id = specialty_id
    def __str__(self):
        return self.name

class Worker:
    def __init__(self, name, pwd, card_id, picture, hometown, specialty, worker_id=None):
        self.name = name
        self.picture = picture
        self.pwd = pwd
        self.card_id = card_id
        self.hometown = hometown
        self.specialty = specialty
        self.worker_id = worker_id
    def __str__(self):
        strs = [self.name, self.specialty, "ID %s" % self.card_id[-4:]]
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
    # Check card_id not exists
    with DatabaseConnection() as conn:
        card_id = conn.execute("""
            SELECT 1 FROM Workers WHERE card_id = ?
            """, (worker.card_id, ))
        if len(card_id) > 0:
            raise DuplicateResource()

    # Insert hometown if necessary
    place_id = insert_place_if_not_exist(worker.hometown)
    # Insert specialty if necessary
    specialty_id = insert_specialty_if_not_exist(worker.specialty)
    # Insert worker
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Workers (name, card_id, pwd, place_id, picture)
            VALUES (?, ?, ?, ?, ?)
            """, (worker.name, worker.card_id, worker.pwd, place_id, worker.picture))
        worker_id = conn.lastrowid()
        conn.execute("""
            INSERT INTO WorkerHasSpecialty (worker_id, specialty_id)
            VALUES (?, ?)
            """, (worker_id, specialty_id))
        conn.commit()
        return worker_id

def verify_worker(card_id, pwd):
    with DatabaseConnection() as conn:
        db_pwd = conn.execute("""
            SELECT worker_id, pwd FROM Workers WHERE card_id = ?
            """, (card_id, ))
        if len(pwd) == 0:
            raise ResouceNotFound()
        if pwd != db_pwd[0][1]:
            raise InvalidCredential()
        return db_pwd[0][0]

def verify_team(reg_id, pwd):
    with DatabaseConnection() as conn:
        db_pwd = conn.execute("""
            SELECT team_id, pwd FROM Workers WHERE registration_id = ?
            """, (reg_id, ))
        if len(pwd) == 0:
            raise ResouceNotFound()
        if pwd != db_pwd[0][1]:
            raise InvalidCredential()
        return db_pwd[0][0]

def add_team(team):
    # Check registration_id not exists
    with DatabaseConnection() as conn:
        registration_id = conn.execute("""
            SELECT 1 FROM Teams WHERE registration_id = ?
            """, (team.registration_id, ))
        if len(registration_id) > 0:
            raise DuplicateResource()
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

    print(worker_id, team_id, project_id, starts, ends)

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
            SELECT worker_id, name, card_id, (SELECT name FROM Places WHERE place_id = Workers.place_id)
            FROM Workers
            """)
def get_specialties():
    with DatabaseConnection() as conn:
        result = conn.execute("""
            SELECT name FROM Specialty
            """)
        return [x[0] for x in result]

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
        super(DatabaseConnection, self).__init__(config.data_db_path, read_only)

class TodoDatabaseConnection(SqliteDatabaseConnection):
    def __init__(self):
        super(DatabaseConnection, self).__init__(config.todo_db_path, False)

def get_next_worker_id():
    with TodoDatabaseConnection() as conn:
        conn.begin()
        worker_id = conn.execute("""
            SELECT worker_id
            FROM Todos
            LIMIT 1
            """)
        if len(worker_id) == 0:
            return None
        conn.execute("""
            DELETE FROM Todos WHERE worker_id = ?
            """, worker_id[0])
        conn.commit()
        return worker_id[0]

def put_next_worker_id(worker_id):
    with TodoDatabaseConnection() as conn:
        conn.begin()
        if not len(conn.execute("SELECT worker_id FROM Todos WHERE worker_id = ?", (worker_id,))):
            return
        conn.execute("""
            INSERT INTO Todos VALUES (?)
            """, (worker_id, ))
        conn.commit()
        return

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

def get_worker_specialty(worker_id):
    with DatabaseConnection() as conn:
        (specialty_id, name) = conn.execute("""
            SELECT specialty_id, name
            FROM WorkerHasSpecialty
            JOIN Specialty USING (specialty_id)
            WHERE worker_id = ?
            LIMIT 1
            """, (worker_id, ))[0]
        return Specialty(name, specialty_id=specialty_id)

def get_worker_cert(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT cert_id, name, achieved, level
            FROM WorkerHasCert
            JOIN Certificate USING (cert_id)
            WHERE worker_id = ?
            LIMIT 1
            """) 

def get_worker_info_helper(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT Workers.name, picture, Specialty.name
            FROM Workers
            JOIN WorkerHasSpecialty USING (worker_id)
            JOIN Specialty USING (specialty_id)
            WHERE Workers.worker_id = ?
            LIMIT 1
            """, (worker_id, ))[0]

def get_team_info_helper(team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT Teams.name, Teams.picture, LaborTeams.name
            FROM Teams
            JOIN TeamWorksWithLaborTeams USING (team_id)
            JOIN LaborTeams USING (laborteam_id)
            WHERE Teams.team_id = ?
            LIMIT 1
            """, (team_id, ))[0]

def get_matched_workers_for_worker(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT a.name, a.worker_id, Specialty.name, score, reason
            FROM Workers a
            JOIN MatchedWorkers ON (a.worker_id = MatchedWorkers.worker_id1)
            JOIN Workers b ON (b.worker_id = MatchedWorkers.worker_id2)
            JOIN WorkerHasSpecialty ON (WorkerHasSpecialty.worker_id = a.worker_id)
            JOIN Specialty ON (Specialty.specialty_id = WorkerHasSpecialty.specialty_id)
            WHERE b.worker_id = ?
            AND score > 0
            ORDER BY score DESC
            """, (worker_id, ))

def get_ex_projects_for_worker(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT name, picture
            FROM Projects
            JOIN WorkerTeamProject USING (project_id)
            WHERE worker_id = ?
            """, (worker_id, ))

def get_ex_teams_for_worker(worker_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT team_id, name
            FROM Teams
            JOIN WorkerTeamProject USING (team_id)
            WHERE worker_id = ?
            """, (worker_id, ))

def get_ex_projects_for_team(team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT name, picture
            FROM Projects
            JOIN WorkerTeamProject USING (project_id)
            WHERE team_id = ?
            """, (team_id, ))

def get_current_workers_for_team(team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT COUNT(WorkerTeamProject.worker_id), Specialty.name
            FROM WorkerTeamProject
            JOIN WorkerHasSpecialty USING (worker_id)
            JOIN Specialty USING (specialty_id)
            WHERE team_id = ?
            GROUP BY specialty_id
            """, (team_id, ))

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

def get_team_homies(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT COUNT(DISTINCT WorkerTeamProject.worker_id)
            FROM WorkerTeamProject
            JOIN Teams USING (team_id)
            JOIN Workers USING (worker_id)
            WHERE Teams.team_id = ?
            AND ends is NULL
            AND Workers.place_id = (SELECT place_id FROM Workers WHERE Workers.worker_id = ?)
            """, (team_id, worker_id))[0]

def get_team_ex_members(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT starts, ends
            FROM WorkerTeamProject
            WHERE team_id = ? AND worker_id = ?
            AND ends IS NOT NULL
            """, (team_id, worker_id))

def get_team_ex_teammates(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT COUNT(DISTINCT WorkerTeamProject.worker_id)
            FROM WorkerTeamProject
            WHERE team_id = ?
            AND ends is NULL
            AND worker_id IN (
                SELECT b.worker_id
                FROM WorkerTeamProject a
                JOIN WorkerTeamProject b ON (a.team_id = b.team_id)
                WHERE a.worker_id = ?
                AND a.ends IS NOT NULL AND b.ends IS NOT NULL
                AND ((a.ends > b.starts AND a.starts < b.ends)
                OR (b.ends > a.starts AND b.starts < a.ends))
            )
            """, (team_id, worker_id))[0]

def get_cooperation(worker_id, team_id):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT COUNT(DISTINCT project_id)
            FROM WorkerTeamProject
            WHERE worker_id = ?
            AND team_id = ?
            AND ends IS NOT NULL
            """, (worker_id, team_id))[0]

def get_specialty_candidate_workers(team_id, specialty):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT Workers.name,
                   Workers.worker_id,
                   (SELECT Places.name
                    FROM Places
                    WHERE place_id = Workers.place_id),
                   Workers.certified
            FROM Workers
            JOIN WorkerHasSpecialty USING (worker_id)
            JOIN Specialty USING (specialty_id)
            WHERE Specialty.name = ?
            AND worker_id NOT IN (SELECT worker_id
                                  FROM WorkerTeamProject
                                  WHERE ends IS NULL
                                  AND team_id = ?
                                  )
            """, (specialty, team_id))

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

def insert_specialty_if_not_exist(name):
    with DatabaseConnection() as conn:
        specialty_id = conn.execute("""
            SELECT specialty_id FROM Specialty WHERE name = ?
            """, (name, ))
        if len(specialty_id) > 0:
            return specialty_id[0][0]
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Specialty (name) VALUES (?)
            """, (name, ))
        specialty_id = conn.lastrowid()
        conn.commit()
        return specialty_id

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
            raise ResouceNotFound("Team not found")
        return team_id[0][0]

def project_exists(project_name):
    with DatabaseConnection() as conn:
        project_id = conn.execute("""
            SELECT project_id FROM Projects WHERE name = ?
            """, (project_name,))
        if len(project_id) == 0:
            raise ResouceNotFound("Project not found")
        return project_id[0][0]

