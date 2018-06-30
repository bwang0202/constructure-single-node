# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json
import traceback
import urllib
import base64

from match.match import *

BACKGROUND = False

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
            return HttpResponse(json.dumps({'experiences': get_worker_experience(worker_id)}))
        except ResouceNotFound:
            resp = HttpResponse(json.dumps({'msg': 'worker not found'}))
            resp.status_code = 404
            return resp
        except Exception as e:
            traceback.print_exc()
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            add_worker_team_project(body['worker_id'], body['team'], body['project'],
                body['starts'], body.get('ends', None))

            # FIXME:
            if BACKGROUND:
                put_next_worker_id(body['worker_id'])
            else:
                compute_match_for_worker(body['worker_id'])
            return HttpResponse(json.dumps({'msg': 'success'}))
        except ResouceNotFound as e:
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 404
            return resp
        except Exception as e:
            traceback.print_exc()
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

################ Get specialty workers for team ###############
################ Get Workers matched workers ##################

def worker_match(request):
    if request.method == "GET":
        try:
            if request.GET.get('team_id'):
                specialty = request.GET.get('specialty')
                # FIXME:
                specialty = base64.decodestring(specialty + "==").decode('utf8')
                return HttpResponse(json.dumps({'workers': match_team_specialty_workers(
                    request.GET.get('team_id'), specialty)}))
            if request.GET.get('worker_id'):
                return HttpResponse(json.dumps(get_worker_info(request.GET.get('worker_id'))))
        except Exception as e:
            traceback.print_exc()
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp

    raise RuntimeException()

################ Get team info ###############################

def team_match(request):
    if request.method == "GET":
        try:
            return HttpResponse(json.dumps(get_team_info(
                request.GET.get('team_id'))))
        except Exception as e:
            traceback.print_exc()
            resp = HttpResponse(json.dumps({'msg': e.message}))
            resp.status_code = 500
            return resp
    raise RuntimeException()

