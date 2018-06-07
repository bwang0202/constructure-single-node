-- Constructure 1.0
-- Bojun Wang, May 2018
-- Sqlite3

CREATE TABLE Places (
    place_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    --
    UNIQUE (name),
    CHECK (length(name) > 0)
);

CREATE TABLE Workers (
    worker_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    work_age INTEGER NOT NULL,
    place_id INTEGER NOT NULL REFERENCES Places(place_id),
    education INTEGER NOT NULL DEFAULT 0,
    jobs INTEGER NOT NULL DEFAULT 1,
    projects INTEGER NOT NULL DEFAULT 0,
    average_project_days INTEGER NOT NULL DEFAULT 30,
    type_of_projects INTEGER NOT NULL 1, # 1 住宅 2 小区 3 公共建筑 4 办公楼
    num_of_teams INTEGER NOT NULL DEFAULT 0,
    type_of_teams INTEGER NOT NULL 1, # 1 世界 2 全国 3 地区领头 4 地区
    worker_level INTEGER NOT NULL DEFAULT 50,
    --
    UNIQUE (name),
    CHECK (age > 0),
    CHECK (work_age >= 0),
    CHECK (length(name) > 0),
    CHECK (jobs > 0),
    CHECK (projects > 0),
    CHECK (average_project_days > 0),
    CHECK (num_of_teams >= 0)
    -- CHECK (education 0 '无' or education 1 '小学'
    --     or education 2 '初中' or education 3'高中'
    --     or education 4'大专' or education 5'大学'
    --     or education 6 '研究生' or education 7'博士'
    --     or education 8 '博士后')
);

-- Not allowing teams with duplicate names for now
CREATE TABLE Teams (
    team_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    --
    UNIQUE(name),
    CHECK (length(name) > 0)
);

-- Worker may just already know someone outside the scope of this db
CREATE TABLE WorkerKnowsWorker (
    worker_id1 INTEGER NOT NULL REFERENCES Workers(worker_id),
    worker_id2 INTEGER NOT NULL REFERENCES Workers(worker_id),
    starts DATETIME NOT NULL,
    ends DATETIME,
    notes TEXT,
    --
    PRIMARY KEY (worker_id1, worker_id2),
    CHECK (starts < ends),
    CHECK (worker_id1 <> worker_id2)
);

-- a worker could be part of team for multiple times as multiple
-- different positions
-- position 1, 2, 3 means worker, mid-leader, big-leader for now
CREATE TABLE WorkerPartOfTeam (
    worker_id INTEGER NOT NULL REFERENCES Workers(worker_id),
    team_id INTEGER NOT NULL REFERENCES Team(team_id),
    starts DATETIME NOT NULL,
    ends DATETIME,
    position INTEGER NOT NULL DEFAULT 1,
    --
    PRIMARY KEY (worker_id, team_id, starts),
    CHECK (ends is NULL or ends > starts)
);

CREATE TABLE Speciality (
    speciality_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    --
    UNIQUE (name),
    CHECK (length(name) > 0)
);

CREATE TABLE TeamNeedsSpeciality (
    speciality_id INTEGER NOT NULL REFERENCES Speciality(speciality_id),
    team_id INTEGER NOT NULL REFERENCES Team(team_id),
    count INTEGER NOT NULL DEFAULT 1,
    --
    UNIQUE (team_id, speciality_id),
    CHECK (count > 0)
);

-- certificate must be tied to a speciality
-- 六级木匠 （相当于中级知识分子）
CREATE TABLE Certificate (
    cert_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    speciality_id INTEGER NOT NULL REFERENCES Speciality(speciality_id),
    level INTEGER NOT NULL DEFAULT 0, # 0 none 1 初级 2 中级 3 高级 4 技师
    --
    UNIQUE (name),
    UNIQUE (speciality_id, level),
    -- CHECK (length(name) > 0),
    CHECK (level >= 0)
);

CREATE TABLE WorkerHasCert (
    worker_id INTEGER NOT NULL REFERENCES Workers(worker_id),
    cert_id INTEGER NOT NULL REFERENCES Certificate(cert_id),
    achieved DATETIME,
    --
    PRIMARY KEY (worker_id, cert_id)
);

CREATE TABLE WorkerHasSpeciality (
    worker_id INTEGER NOT NULL REFERENCES Workers(worker_id),
    speciality_id INTEGER NOT NULL REFERENCES Speciality(speciality_id),
    --
    PRIMARY KEY (worker_id, speciality_id)
);

-- 沈阳奥体，北京奥体
CREATE TABLE Projects (
    project_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    place_id INTEGER NOT NULL REFERENCES Places(place_id),
    --
    UNIQUE (name, place_id),
    CHECK (length(name) > 0)
);

-- position 1, 2, 3 means worker, mid-leader, big-leader for now
-- some big-leader may not have a clear speciality during this project
CREATE TABLE TeamParticipateProject (
    team_id INTEGER NOT NULL REFERENCES Team(team_id),
    project_id INTEGER NOT NULL REFERENCES Projects(project_id),
    starts DATETIME NOT NULL,
    ends DATETIME,
    --
    PRIMARY KEY (team_id, project_id, starts),
    CHECK (ends is NULL or ends > starts)
);

CREATE TABLE MatchedWorkers (
    worker_id1 INTEGER NOT NULL,
    worker_id2 INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    reason TEXT NOT NULL,
    --
    PRIMARY KEY (worker_id1, worker_id2),
    CHECK (score >= 0 and score <= 100)
);

CREATE TABLE MatchedWorkerTeam (
    worker_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    reason TEXT NOT NULL,
    --
    PRIMARY KEY (team_id, worker_id),
    CHECK (score >= 0 and score <= 100)
);