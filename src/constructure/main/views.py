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
projects_enum = {"单体住宅": 1, "住宅小区": 2, "公共建筑": 3, "办公楼": 4}
teams_enum = {"世界企业": 4, "全国企业": 3, "地区领头企业": 2, "地区企业": 1}

def to_age(age_input):
    if age_input == "20 - 29":
        return 20
    if age_input == "30 - 39":
        return 30
    if age_input == "40 - 49":
        return 40
    return 50

def to_jobs(jobs_input):
    if jobs_input == "1 种":
        return 1
    if jobs_input == "2 种":
        return 2
    if jobs_input == "3 种":
        return 3
    return 4

def to_work_age(work_age_input):
    if work_age_input == "不到一年":
        return 0
    if work_age_input == "一到三年":
        return 1
    if work_age_input == "三到五年":
        return 3
    if work_age_input == "五年以上":
        return 5
    return 2

def to_projects(projects_input):
    if projects_input == "1 - 3个":
        return 2
    if projects_input == "4 - 6个":
        return 5
    if projects_input == "7 - 9 个":
        return 8
    if projects_input == "> 10个":
        return 11
    return 6

def to_project_days(project_days):
    if project_days == "1个月之内":
        return 30
    if project_days == "1个月 ~ 半年":
        return 180
    if project_days == "半年 ~ 一年":
        return 360
    if project_days == "一年以上":
        return 500
    return 200

def test(request):
    print('this is a test log')
    return HttpResponse('Testing view.')


def build_worker(body):
    worker = Worker(body['name'], to_age(body['age']), to_work_age(body['work_age']),
        education_enum.get(body['education'], 1), body['hometown'],
        to_jobs(body['jobs']), to_projects(body['projects']),
        to_project_days(body['average_project_days']), projects_enum.get(body['type_of_projects'], 1),
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
            resp_obj['worker_level'] = worker.get_worker_level()
            resp_obj['worker_percentile'] = compute_worker_percentile(worker_id)
            resp_obj['worker_skill'] = worker.compute_worker_skill()
            resp_obj['worker_experience'] = worker.compute_worker_experience()

        print(resp_obj)
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

