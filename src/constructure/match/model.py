
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
    def __init__(self, name):
        # PLACE ?? TODO
        self.name = name
    def __str__(self):
        return "%s工程队" % self.name

def add_worker(worker):
    # validate hometown
    # Insert hometown if necessary
    
    # Insert speciality if necessary

    # Insert worker

    # return worker_id
    pass

def add_worker_to_team(worker, team, starts, ends=None):
    # validate worker

    # validate team

    # Insert

    # return T/F
    pass

def get_teams(place=None, prefix=None):
    pass

def start_match_calculation(worker):
    if not worker.worker_id:
        raise RuntimeException()
    # Background TODO
    compute_match_for_worker(worker.worker_id)

def get_matched_workers(worker):

def get_matched_teams(worker):