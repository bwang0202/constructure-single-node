# -*- coding: utf-8 -*-

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
    def __init__(self, score, weight, keyword=None, is_specialty=False):
        self.score = score
        self.weight = weight
        self.keyword = keyword
        self.is_specialty = is_specialty # useful for worker/team composition
    def __str__(self):
        return self.keyword if self.keyword else ""

def _match_specialites(worker1, worker2):
    weight = MatchWorkersConstants.specialty
    if worker1.specialty.name == worker2.specialty.name:
        return MatchEntry(100, weight, worker1.specialty.name, is_specialty=True)
    return MatchEntry(0, weight, is_specialty=True)

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

def compute_match_for_worker(worker_id):
    all_workers = get_all_workers()
    for x in all_workers:
        if x[0] == worker_id:
            continue
        # FIXME: check existing match result first
        match_entries = match_workers(x[0], worker_id)
        score = 0
        notes = []
        for y in match_entries:
            score += y.score * y.weight
            if y.score:
                notes.append(y.keyword)
        insert_match_result(x[0], worker_id, score, ",".join(notes))

def match_worker_team_helper(worker_id, team_id):
    hommies = get_team_homies(worker_id, team_id)
    teammates = get_team_ex_teammates(worker_id, team_id)
    cooperations = get_cooperation(worker_id, team_id)

    return [MatchEntry(100 if hommies > 10 else hommies * 10,
                MatchTeamsConstants.hometown, "老乡多"),
            MatchEntry(100 if teammates > 10 else teammates * 10,
                MatchTeamsConstants.teammates, "旧搭档多"),
            MatchEntry(100 if len(cooperations) else 0,
                MatchTeamsConstants.cooperation, "曾合作")]

def compute_match_for_worker_team(worker_id, team_id):
    match_entries = match_worker_team_helper(worker_id, team_id)
    score = 0
    notes = []
    for y in match_entries:
        score += y.score * y.weight
        if y.score:
            notes.append(y.keyword)
    return (score, ",".join(notes))

def match_team_specialty_workers(team_id, specialty):
    # get unhired workers:
    specialty_candidate_workers = get_specialty_candidate_workers(team_id, specialty)

    # compute cci for each
    worker_ccis = {}
    for (worker_id,) in specialty_candidate_workers:
        worker_ccis[worker_id] = compute_match_for_worker_team(worker_id, team_id)

    return worker_ccis
