echo -e "Type any key to start Demo:"
read line

echo "Admin displaying all workers..."
curl -s XGET http://localhost:8000/user/worker/ | jq .

echo -e "Type any key to continue:"
read line

echo "Admin displaying all teams..."

curl -s XGET http://localhost:8000/user/team/ | jq .

echo -e "Type any key to continue:"
read line

echo "Adding a new worker to Service..."
echo "Yang Juncheng, Zhejiang, age 35, estimate clerks"

curl -s -XPOST http://localhost:8000/user/worker/ -d '
{"name": "Yang Juncheng",
"hometown": "Zhejiang",
"age": 35, "work_age": 10,
"education": "College",
"speciality": "estimate clerks",
"ex_teams": [{"team_id":1, "starts":"2010-01-01 00:00:00.000", "ends":"2015-01-01 00:00:00.000"}]}' | jq .

echo -e "Type any key to continue:"
read line

echo "Adding a new worker to Service..."
echo "Li Kai, Sichuan, age 45, construction workers"

curl -s -XPOST http://localhost:8000/user/worker/ -d '
{"name": "Li Kai",
"hometown": "Sichuan",
"age": 45, "work_age": 22,
"education": "College",
"speciality": "construction worker",
"ex_teams": [{"team_id":4, "starts":"2010-01-01 00:00:00.000", "ends":"2016-01-01 00:00:00.000"}]}' | jq .

echo -e "Type any key to continue:"
read line
echo "Computing Workers CCI for new worker..."
sleep 2

curl -s -GET http://localhost:8000/user/worker_match/?worker_id=26 | jq .

echo -e "Type any key to continue:"
read line
echo "Computing Workers CCI for 2nd new worker..."
sleep 2

curl -s -GET http://localhost:8000/user/worker_match/?worker_id=27 | jq .

echo -e "Type any key to continue:"
read line
echo "Fetching Team Suggestion CCI for new worker..."
sleep 2

curl -s -GET http://localhost:8000/user/team_match/?worker_id=26 | jq .

echo -e "Type any key to continue:"
read line
echo "Fetching Team Suggestion CCI for 2nd new worker..."
sleep 2

curl -s -GET http://localhost:8000/user/team_match/?worker_id=27 | jq .