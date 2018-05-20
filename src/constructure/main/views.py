# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json

from match.match import *

def build_worker(body):
    worker = Worker(body['name'], body['age'], body['work_age'],
        body['education'], body['hometown'])
    worker.specialities.append(body['speciality'])
    return worker


def echo(request):
    if request.method == "GET":
        #GET http://localhost:8000/user/worker/?q=1&arg2=2
        return HttpResponse("%s, %s, %s" % (request.method, request.path, request.GET.get('q', 'aadljalja')))
    else:
        #curl -XPOST http://localhost:8000/user/worker/ -d '{"key1":"value1"}'
        return HttpResponse("%s, %s, %s" % (request.method, request.path, request.body))

def worker(request):
    if request.method == "GET":
        #GET http://localhost:8000/user/worker/?q=1&arg2=2
        return HttpResponse(json.dumps({'data':get_workers()}))
    elif request.method == "POST":
        #curl -XPOST http://localhost:8000/user/worker/ -d '{"key1":"value1"}'
        body = json.loads(request.body)
        worker = build_worker(body)
        worker_id = add_worker(worker)
        ex_teams = body['ex_teams']
        for ex_team in ex_teams:
            team_id = ex_team['team_id']
            starts = ex_team['starts']
            ends = ex_team['ends']
            add_worker_to_team(worker_id, team_id, starts, ends)
        start_match_calculation(worker_id)
        return HttpResponse(json.dumps({'msg': 'worker added', 'id': worker_id}))

    return echo(request)

def team(request):
    if request.method == "GET":
        # GET all teams
        return HttpResponse(json.dumps({'data': get_teams()}))
    return echo(request)

def worker_team(request):
    if request.method == "POST":
        body = json.loads(request.body)
        add_worker_to_team(body['worker_id'], body['team_id'], body['starts'],
            body['ends'])
        start_match_calculation(body['worker_id'])
        return HttpResponse(json.dumps({'msg': 'worker added to team.'}))
    return echo(request)

def worker_match(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({'data': get_matched_workers(
            request.GET.get('worker_id'))}))

    return echo(request)

def team_match(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({'data': get_matched_teams(
            request.GET.get('worker_id'))}))
    return echo(request)

