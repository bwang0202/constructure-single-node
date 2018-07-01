# constructure-single-node

Developer Docs:

1. useful commands:
	a. grep for non-ascii chars in a file.

pcregrep --color="auto" -n "[^\x00-\x7F]" <file path>

2. TODO:
        a. https://blog.csdn.net/xjtarzan/article/details/51492106
	    b. Try deploy in AWS (django)

Demo Front End Notes & API:
    Request:
    POST /worker/
    post-body is a json with format below:
    {"name":"xing ming",
     "age": 40,
     "work_age": 20,
     "education": 3,
     "hometown": "Sichuan, Chengdu",
     "jobs": 4,
     "projects": 10,
     "average_project_days": 100,
     "type_of_projects": 2,
     "num_of_teams": 2,
     "type_of_teams": 2,
     "speciality": "mujiang",
     "certificate": 1}
    Response:
    {"msg":"worker added",
     "worker_id": 123,
     "worker_level": 6,
     "worker_percentile": 34,
     "worker_skill": 5,
     "worker_experience": 5}


{"name":"姓名",
     "age": 40,
     "work_age": 20,
     "education": 3,
     "hometown": "四川",
     "jobs": 4,
     "projects": 10,
     "average_project_days": 100,
     "type_of_projects": 2,
     "num_of_teams": 2,
     "type_of_teams": 2,
     "speciality": "木匠",
     "certificate": 1}


jobs --> 会几个工种，projects -- 参与过几个项目，average project days -- 项目平均时间
type of projects 1 单独住宅 2 住宅小区 3 公共建筑 4 办公楼
num of teams 换过几个东家
type of teams 1 世界企业 2 全国企业 3 地区领头企业 4 地区企业
certificate 0 尚未认证 1 初级 2 中级 3 高级 4 技师
education 1 小学 2 初中 3 高中 4 本科
worker percentile 领先比率 worker level 综合吸引力