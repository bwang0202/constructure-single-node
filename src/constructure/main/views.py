# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

import json

from match.match import *

DO_MATCHING = False
DO_COMPETING = True

education_enum = {"小学": 1, "初中": 2, "高中": 3, "本科": 4}
certificate_enum = {"尚未认证": 0, "初级": 1, "中级": 2, "高级": 3, "技师": 4}
projects_enum = {"单独住宅": 1, "住宅小区": 2, "公共建筑": 3, "办公楼": 4}
teams_enum = {"世界企业": 4, "全国企业": 3, "地区领头企业": 2, "地区企业": 1}


def test(request):
    print('this is a test log')
    return HttpResponse('Testing view.')


def build_worker(body):
    worker = Worker(body['name'], body['age'], body['work_age'],
        education_enum.get(body['education'], 1), body['hometown'], body['jobs'], body['projects'],
        body['average_project_days'], projects_enum.get(body['type_of_projects'], 1),
        body['num_of_teams'], teams_enum.get(body['type_of_teams'], 1))
    worker.specialities.append(body['speciality'])
    worker.certificates.append(certificate_enum.get(body['certificate'], 0))
    return worker


def echo(request):
    if request.method == "GET":
        #GET http://localhost:8000/user/worker/?q=1&arg2=2
        return HttpResponse("%s, %s, %s" % (request.method, request.path, request.GET.get('q', 'aadljalja')))
    else:
        #curl -XPOST http://localhost:8000/user/worker/ -d '{"key1":"value1"}'
        return HttpResponse("%s, %s, %s" % (request.method, request.path, request.body))

def worker(request):
    print('inside worker view function')
    if request.method == "GET":
        #GET http://localhost:8000/user/worker/?q=1&arg2=2
        return HttpResponse(json.dumps({'data':get_workers()}))
    elif request.method == "POST":
        #curl -XPOST http://localhost:8000/user/worker/ -d '{"key1":"value1"}'
        print(request.body)
        body = json.loads(request.body)
        worker = build_worker(body)
        worker_id = add_worker(worker)
        if 'ex_teams' in body:
            ex_teams = body['ex_teams']
            for ex_team in ex_teams:
                team_id = ex_team['team_id']
                starts = ex_team['starts']
                ends = ex_team['ends']
                add_worker_to_team(worker_id, team_id, starts, ends)

        if DO_MATCHING:
            start_match_calculation(worker_id)

        resp_obj = {'msg': 'worker added', 'id': worker_id}

        if DO_COMPETING:
            worker_level = worker.get_worker_level()
            resp_obj['worker_level'] = 10 if worker_level > 100 else worker_level/10
            update_worker_level(worker_id, worker_level)
            resp_obj['worker_percentile'] = compute_worker_percentile(worker_id)
            resp_obj['worker_skill'] = worker.compute_worker_skill()
            resp_obj['worker_experience'] = worker.compute_worker_experience()

        return HttpResponse(json.dumps(resp_obj))

    return echo(request)

# test the flow of html template pass json object via ajax into views function and render result page
def test_worker(request):
    print('inside test worker view function')
    print(request.body)

    response = {'status':1, 'msg':'worker added', 'worker_id': 123, 'worker_percentile': 90, 'worker_skill': 70, 'worker_experience': 60, 'worker_level': 80}

    return HttpResponse(json.dumps(response), content_type='application/json')
     
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

