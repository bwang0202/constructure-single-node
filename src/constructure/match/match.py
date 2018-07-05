# -*- coding: utf-8 -*-

# Constructure 1.0
# Bojun Wang, May 2018
#TODO: 1. make this OO 2. match reason
#

import config

from config import *
from util import *


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

def _match_hometown(hometown1, hometown2):
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
        u"老乡")

def _match_same_experience(same_experiences):
    return MatchEntry(0 if not same_experiences else 100,
        MatchWorkersConstants.teammates,
        u"搭档")

def match_workers(worker_id1, worker_id2):
    (_, _, hometown1) = get_worker_info_helper(worker_id1)
    (_, _, hometown2) = get_worker_info_helper(worker_id2)

    same_experiences = get_workers_same_experience(worker_id1, worker_id2)
    return [_match_hometown(hometown1.split(","), hometown2.split(",")),
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
        if not notes:
            notes = [u"新伙伴"]
        insert_match_result(x[0], worker_id, score, "|".join(notes))

def match_worker_team_helper(worker_id, team_id):
    hommies = get_team_homies(worker_id, team_id)
    teammates = get_team_ex_teammates(worker_id, team_id)
    cooperations = get_cooperation(worker_id, team_id)

    return [MatchEntry(100 if cooperations else 0,
                MatchTeamsConstants.cooperation, u"曾合作"),
            MatchEntry(100 if teammates > 10 else teammates * 10,
                MatchTeamsConstants.teammates, u"旧搭档多"),
            MatchEntry(100 if hommies > 10 else hommies * 10,
                MatchTeamsConstants.hometown, u"老乡多")]

def compute_match_for_worker_team(worker_id, team_id):
    match_entries = match_worker_team_helper(worker_id, team_id)
    score = 0
    notes = []
    for y in match_entries:
        score += y.score * y.weight
        if y.score:
            notes.append(y.keyword)
    if len(notes) == 0:
        notes = [u"新伙伴"]
    return (score, u"|".join(notes))

def match_team_specialty_workers(team_id, specialty):
    # get unhired workers:
    specialty_candidate_workers = get_specialty_candidate_workers(team_id, specialty)

    # compute cci for each
    worker_ccis = []
    for (name, worker_id, hometown, certified) in specialty_candidate_workers:
        (score, notes) = compute_match_for_worker_team(worker_id, team_id)
        worker_ccis.append({
            'name': name,
            'id': worker_id,
            'hometown': hometown,
            'cci': score,
            'certified': True if certified else False,
            'notes': notes
            })

    worker_ccis = sorted(worker_ccis, key=lambda x: 0 - x['cci'])

    return worker_ccis


def get_worker_info(worker_id):
    (worker_name, picture, specialty) = get_worker_specialty_helper(worker_id)
    matched_workers = []
    for (name2, worker_id2, specialty2, score2, note2) in get_matched_workers_for_worker(worker_id):
        matched_workers.append({'name': name2, 'worker_id': worker_id2,
            'specialty': specialty2, 'cci': score2, 'note': note2})
    ex_projects = []
    for (name, picture) in get_ex_projects_for_worker(worker_id):
        ex_projects.append({'name': name, 'picture': picture})
    ex_teams = []
    for (team_id, name) in get_ex_teams_for_worker(worker_id):
        ex_teams.append({'name':name, 'team_id': team_id})
    return {
        'name': worker_name,
        'specialty': specialty,
        'picture': picture,
        'matched_workers': matched_workers,
        'ex_projects': ex_projects,
        'ex_teams': ex_teams
    }

def get_team_info(team_id):
    (name, picture, laborcompany) = get_team_info_helper(team_id)
    ex_projects = []
    for (name2, picture2) in get_ex_projects_for_team(team_id):
        ex_projects.append({'name': name2, 'picture': picture2})
    current_workers = []
    for (count, specialty) in get_current_workers_for_team(team_id):
        current_workers.append({'specialty': specialty, 'number': count,
            'note': "共同合作"})
    return {
        'name': name,
        'picture': picture,
        'laborcompany': laborcompany,
        'ex_projects': ex_projects,
        'current_workers': current_workers
    }
