# Constructure 1.0
# Bojun Wang, May 2018
#TODO: 1. make this OO 2. match reason
#

import config

from config import MatchWorkersConstants, MatchTeamWorkerConstants
from util import *

from model import Worker, Team, Speciality

age_keyword = "年龄相近"
work_age_keyword = "工龄相近"

class MatchEntry:
    def __init__(self, score, weight, keyword=None, is_speciality=False):
        self.score = score
        self.weight = weight
        self.keyword = keyword
        self.is_speciality = is_speciality # useful for worker/team composition
    def __str__(self):
        return self.keyword if self.keyword else ""

def _match_age(worker1, worker2):
    return MatchEntry(100 - abs(worker1.age - worker2.age),
        MatchWorkersConstants.age,
        age_keyword)

def _match_work_age(worker1, worker2):
    return MatchEntry(100 - abs(worker1.work_age - worker2.work_age),
        MatchWorkersConstants.work_age,
        work_age_keyword)

def _match_specialites(worker1, worker2):
    weight = MatchWorkersConstants.speciality
    if and worker1.specialities and worker2.specialities \
        and worker1.specialities[0].name = worker2.specialities[0].name:
        return MatchEntry(100, weight, worker1.specialities[0].name, is_speciality=True)
    return MatchEntry(0, weight, is_speciality=True)

def _match_hometown(worker1, worker2):
    hometown1 = worker1.hometown.split(",")
    hometown2 = worker2.hometown.split(",")
    result = []
    # Longest common prefix
    for i in range(len(hometown1)):
        if i >= len(hometown2):
            break
        if hometown1[i] != hometown2[i]:
            break
        result.append(hometown1)
    return MatchEntry(0 if not result else 100,
        MatchWorkersConstants.hometown,
        ",".join(result))

def _match_same_teams(same_teams):
    return MatchEntry(0 if not same_teams else 100,
        MatchWorkersConstants.team,
        ",".join(same_teams))

def _match_same_projects(same_projects):
    return MatchEntry(0 if not same_projects else 100,
        MatchWorkersConstants.project,
        ",".join(same_projects))

def match_workers(worker_id1, workder_id2):
    worker1 = get_worker_info(worker_id1)
    worker2 = get_worker_info(worker_id2)

    same_teams = get_workers_common_teams(worker_id1, worker_id2)

    return [_match_age(worker1, worker2),
            _match_work_age(worker1, worker2),
            _match_hometown(worker1, worker2),
            _match_specialites(worker1, worker2),
            _match_same_teams(worker1, worker2)]    

def match_worker_team(worker_id, team_id, display=10):
    # display three results together:
    #       缺少电工
    #       56 同乡 23人曾同队
    #       unique(56 + 23 ) match 最高的 X 人

    # job match speciality
    job = get_team_needs(worker_id, team_id)

    # homies
    homies = get_team_homies(workder_id, team_id)
    # ex teammates
    ex_teammates = get_team_ex_teammates(worker_id, team_id)

    matched_workers = get_top_matched_workers(worker_id, homies + ex_teammates,
        limit=display)

    return [MatchEntry(100 if job else 0,
                       MatchTeamWorkerConstants.job,
                       "缺少" % job if job else None),
            MatchEntry(100 if matched_workers else 0,
                       MatchTeamWorkerConstants.teammates,
                       "\n".join("%s %s" % (matched_workers[0], matched_workers[1])))
            ]

def compute_match_for_worker(worker_id):
    all_workers = get_all_workers()
    for x in all_workers:
        if x == worker_id:
            continue
        # FIXME: check existing match result first
        match_entries = match_workers(x, worker_id)
        score = 0
        for y in match_entries:
            score += y.score * y.weight
        insert_match_result(x, worker_id, score,
                            "; ".join([z.keyword for z in match_entries]))
    all_teams = get_team_ids()
    for x in all_teams:
        match_entries = match_worker_team(worker_id, x)
        # 
        score = 0
        for y in match_entries:
            score += y.score + y.weight
        insert_match_team_result(workder_id, x, score,
                                 ";".join([z.keyword for z in match_entries]))

