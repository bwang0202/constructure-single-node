# constructure-single-node

Developer Docs:

1. useful commands:
	a. grep for non-ascii chars in a file.

pcregrep --color='auto' -n '[^\x00-\x7F]' <file path>

2. TODO:
	a. Try deploy in AWS (django)
	b. zhongwen

Demo Front End Notes & API:
    Request:
    POST /worker/
    post-body is a json with format below:
    {'name':'xing ming',
     'age': 40,
     'work_age': 20,
     'education': 3,
     'hometown': 'Sichuan, Chengdu',
     'jobs': 4,
     'projects': 10,
     'average_project_days': 100,
     'type_of_projects': 2,
     'num_of_teams': 2,
     'type_of_teams': 2,
     'speciality': 'mujiang',
     'certificate': 1}
    Response:
    {'msg':'worker added',
     'worker_id': 123,
     'worker_level': 6,
     'worker_percentile': 34}
