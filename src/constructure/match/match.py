# Constructure 1.0
# Bojun Wang, May 2018
#TODO: 1. make this OO 2. match reason
#

import config

from config import MatchWorkersConstants, MatchTeamWorkerConstants
from util import *

class ResouceNotFound(Exception):
    pass

class DuplicateResource(Exception):
    pass

class InvalidCredential(Exception):
    pass

class MatchEntry:
    def __init__(self, score, weight, keyword=None, is_speciality=False):
        self.score = score
        self.weight = weight
        self.keyword = keyword
        self.is_speciality = is_speciality # useful for worker/team composition
    def __str__(self):
        return self.keyword if self.keyword else ""


def _match_specialites(worker1, worker2):
    weight = MatchWorkersConstants.speciality
    if worker1.speciality.name == worker2.speciality.name:
        return MatchEntry(100, weight, worker1.speciality.name, is_speciality=True)
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
        result.append(hometown1[i])
    return MatchEntry(0 if not result else 100,
        MatchWorkersConstants.hometown,
        "%s" % ",".join(result))

def _match_same_experience(same_experiences):
    return MatchEntry(0 if not same_experiences else 100,
        MatchWorkersConstants.team,
        ",".join(same_experiences))

def match_workers(worker_id1, worker_id2):
    worker1 = get_worker_info(worker_id1)
    worker2 = get_worker_info(worker_id2)

    same_experiences = get_workers_same_experience(worker_id1, worker_id2)

    return [_match_hometown(worker1, worker2),
            _match_same_experience(same_experiences)]

def match_worker_team(worker_id, team_id, display=4):
    # display three results together:

    # job match speciality
    # job = get_team_needs(worker_id, team_id)
    # used to work together
    ex_members = get_team_ex_members(worker_id, team_id)TODODO

    # homies
    homies = get_team_homies(worker_id, team_id)
    # ex teammates
    ex_teammates = get_team_ex_teammates(worker_id, team_id)


    teammates_candidates = []
    for x in homies:
        teammates_candidates.append(x[0])
    for x in ex_teammates:
        teammates_candidates.append(x[0])

    matched_workers = get_top_matched_workers(worker_id, teammates_candidates,
        limit=display)

    return [MatchEntry(100 if job else 0,
                       MatchTeamWorkerConstants.job,
                       "Needs %s" % job if job else ""),
            MatchEntry(100 if matched_workers else 0,
                       MatchTeamWorkerConstants.teammates,
                       ".    ".join(["%s %s" % (x[0], x[1]) for x in matched_workers]) if matched_workers else "")
            ]

def start_match_calculation(worker_id):
    if not worker_id:
        raise RuntimeException("worker_id %s" % str(worker_id))
    # Background TODO
    compute_match_for_worker(worker_id)

def team_start_match_calculation(team_id):
    if not team_id:
        raise RuntimeException("team_id %s" % str(team_id))
    # Background TODO
    compute_match_for_team(team_id)


def compute_match_for_worker(worker_id):
    all_workers = get_all_workers()
    for x in all_workers:
        if x[0] == worker_id:
            continue
        # FIXME: check existing match result first
        match_entries = match_workers(x[0], worker_id)
        # sort according to match result
        match_entries = sorted(match_entries, key=lambda me:(-me.score * me.weight))

        score = 0
        for y in match_entries:
            score += y.score * y.weight
        insert_match_result(x[0], worker_id, score,
                            "; ".join([z.keyword for z in match_entries[:3]]))
    all_teams = get_team_ids()
    for x in all_teams:
        match_entries = match_worker_team(worker_id, x[0])
        # 
        score = 0
        for y in match_entries:
            score += y.score * y.weight
        insert_match_team_result(worker_id, x[0], score,
                                 ";".join([z.keyword for z in match_entries]))


def compute_match_for_team(team_id):
    all_workers = get_all_workers()
    for x in all_workers:
        match_entries = match_worker_team(x[0], team_id)
        score = 0
        for y in match_entries:
            score += y.score * y.weight
        insert_match_team_result(x[0], team_id, score,
                                 ";".join([z.keyword for z in match_entrie]))

