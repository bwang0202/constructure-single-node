# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json
import traceback

from match.match import *

def build_worker(body):
    worker = Worker(body['name'], body['password'], body['idcard'],
        body['picture'], body['hometown'], body['specialty'])
    return worker

def build_team(body):
    team = Team(body['name'], body['password'], body['idcode'],
        body['picture'])
    return team

def echo(request):
    if request.method == "GET":
        #GET http://localhost:8000/user/worker/?q=1&arg2=2
        return HttpResponse("%s, %s, %s" % (request.method, request.path, request.GET.get('q', 'aadljalja')))
    else:
        #curl -XPOST http://localhost:8000/user/worker/ -d '{"key1":"value1"}'
        return HttpResponse("%s, %s, %s" % (request.method, request.path, request.body))

################ New User Registration ########################################

def worker(request):
    if request.method == "GET":
        #GET http://localhost:8000/user/worker/?q=1&arg2=2
        return HttpResponse(json.dumps({'data':get_workers()}))
    elif request.method == "POST":
        #curl -XPOST http://localhost:8000/user/worker/ -d '{"key1":"value1"}'
        try:
            body = json.loads(request.body)
            worker = build_worker(body)
            worker_id = add_worker(worker)
            return HttpResponse(json.dumps({'msg': 'success', 'worker_id': worker_id}))
        except DuplicateResource as e:
            resp = HttpResponse(json.dumps({'msg': 'Worker with same card ID already exists'}))
            resp.status_code = 400
            return resp
        except Exception as e:
            traceback.print_exc()
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    raise RuntimeException("Unknown request worker %s" % request.method)

def team(request):
    if request.method == "GET":
        # GET all teams
        return HttpResponse(json.dumps({'data': get_teams()}))
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            team = build_team(body)
            team_id = add_team(team)
            start_team_match_calculation(team_id)
            return HttpResponse(json.dumps({'msg': 'success', 'team_id': team_id}))
        except DuplicateResource as e:
            resp = HttpResponse(json.dumps({'msg': 'Team with same registration ID already exists'}))
            resp.status_code = 400
            return resp
        except Exception as e:
            traceback.print_exc()
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    raise RuntimeException("Unknown request team %s" % request.method)

################# User Logging On #############################################

def worker_logon(request):
    if request.method == "GET":
        try:
            card_id = request.GET.get('id')
            pwd = request.GET.get('pwd')
            worker_id = verify_worker(card_id, pwd)
            return HttpResponse(json.dumps({'worker_id': worker_id}))
        except ResouceNotFound:
            resp = HttpResponse(json.dumps({'msg': 'worker not found'}))
            resp.status_code = 404
            return resp
        except InvalidCredential:
            resp = HttpResponse(json.dumps({'msg': 'wrong password'}))
            resp.status_code = 403
            return resp
        except Exception as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            res.status_code = 500
            return resp
    raise RuntimeException()

def team_logon(request):
    if request.method == "GET":
        try:
            reg_id = request.GET.get('id')
            pwd = request.GET.get('pwd')
            team_id = verify_team(reg_id, pwd)
            return HttpResponse(json.dumps({'team_id': team_id}))
        except ResouceNotFound:
            resp = HttpResponse(json.dumps({'msg': 'team not found'}))
            resp.status_code = 404
            return resp
        except InvalidCredential:
            resp = HttpResponse(json.dumps({'msg': 'wrong password'}))
            resp.status_code = 403
            return resp
        except Exception as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            res.status_code = 500
            return resp
    raise RuntimeException()

################# User Experiences and Certificates ###########################

def worker_exp(request):
    if request.method == "GET":
        try:
            worker_id = request.GET.get('worker_id')
            return HttpResponse(json.dumps({'experiences': get_work_experience(worker_id)}))
        except ResouceNotFound:
            resp = HttpResponse(json.dumps({'msg': 'worker not found'}))
            resp.status_code = 404
            return resp
        except Exception as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            add_worker_team_project(body['worker_id'], body['team'], body['project'],
                body['starts'], body.get('ends', None))
            put_next_worker_id(body['worker_id'])
        except ResouceNotFound as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 404
            return resp
        except Exception as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    raise RuntimeException()

def worker_certificate(request):
    if request.method == "GET":
        try:
            worker_id = request.GET.get('worker_id')
            return HttpResponse(json.dumps({'certified': get_worker_certified(worker_id)}))
        except Exception as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    raise RuntimeException()

################ specialty ##############################

def specialty(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({'specialty': get_specialties()}))

################

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

