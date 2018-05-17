
class Speciality:
    def __init__(self, name, certificate_name=None,
            speciality_id=None):
        self.name = name
        self.certificate_name = certificate_name
        self.speciality_id = speciality_id
    def __str__(self):
        if self.certificate_name:
            return "%s %s" % (self.name, self.certificate_name)
        return self.name

class Worker:
    def __init__(self, name, age, work_age, education,
            hometown, worker_id=None):
        self.name = name
        self.age = age
        self.work_age = work_age
        self.education = education
        self.hometown = hometown
        self.specialities = []
        self.certificates = []
        self.worker_id = worker_id
    def __str__(self):
        result = [self.name, self.hometown]
        if self.specialities:
            result.append(self.specialities[0])
        result.append("工龄%d" % self.work_age)
        if len(result) < 5:
            result.append("籍贯%s" % self.hometown)
        if len(result) < 5:
            result.append("年龄%s" % self.age)
        return ", ".join(result)

    def add_speciality(self, speciality):
        self.specialities.append(speciality)
        return self

def Team:
    def __init__(self, name, team_id=None):
        self.name = name
        self.team_id = team_id
    def __str__(self):
        return "%s%s工程队" % (self.name)

def add_worker(worker):
    # Insert hometown if necessary
    place_id = insert_place_if_not_exist(worker.hometown)
    # Insert worker
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO Workers (name, age, work_age, place_id, education)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (worker.name, worker.age, worker.work_age, place_id, worker.education))
        worker_id = conn.lastrowid()
        conn.commit()

    # Insert speciality if necessary
    speciality_id = insert_speciality_if_not_exist(worker.specialities[0])
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO WorkerHasSpeciality (worker_id, speciality_id)
            VALUES (?, ?)
            """, (worker_id, speciality_id))
        conn.commit()

    return worker_id

def add_worker_to_team(worker_id, team_id, starts, ends=None):
    # validate worker
    if not worker_id or not worker_exists(worker_id):
        raise RuntimeError("worker %s not exists" % str(worker_id))
    # validate team
    if not team_id or not team_exists(team_id):
        raise RuntimeError("team %s not exists" % str(team_id))
    # Insert
    with DatabaseConnection(read_only=False) as conn:
        conn.begin()
        conn.execute("""
            INSERT INTO WorkerPartOfTeam (worker_id, team_id, starts, ends)
            VALUES (?, ?, ?, ?)
            """, (worker_id, team_id, starts, ends))
        conn.commit()

def get_teams(place=None, prefix=None):
    with DatabaseConnection() as conn:
        result = conn.execute("""
            SELECT team_id, name FROM Teams
            """)
    return [Team(x[1], x[0]) for x in result]

def start_match_calculation(worker):
    if not worker.worker_id:
        raise RuntimeException("worker_id %s" % str(worker.worker_id))
    # Background TODO
    compute_match_for_worker(worker.worker_id)

def get_matched_workers(worker_id, limit=10):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT worker_id2, score, reason
            FROM MatchedWorkers
            WHERE worker_id1 = ?
            ORDER BY score DESC
            LIMIT ?
            """, (worker_id, limit, ))

def get_matched_teams(worker_id, limit=5):
    with DatabaseConnection() as conn:
        return conn.execute("""
            SELECT team_id, score, reason
            FROM MatchedWorkerTeam
            WHERE worker_id = ?
            ORDER BY score DESC
            LIMIT ?
            """, (worker_id, limit))
