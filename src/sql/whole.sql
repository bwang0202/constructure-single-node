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
    card_id TEXT NOT NULL,
    pwd TEXT NOT NULL,
    place_id INTEGER NOT NULL REFERENCES Places(place_id),
    picture TEXT,
    certified INTEGER NOT NULL DEFAULT 0,
    --
    UNIQUE (card_id),
    CHECK (length(card_id) > 0),
    CHECK (length(pwd) > 0)
    -- CHECK (education = '无' or education = '小学'
    --     or education = '初中' or education = '高中'
    --     or education = '大专' or education = '大学'
    --     or education = '研究生' or education = '博士'
    --     or education = '博士后')
);

-- Not allowing teams with duplicate names for now
CREATE TABLE Teams (
    team_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pwd TEXT NOT NULL,
    registration_id TEXT NOT NULL,
    picture TEXT,
    --
    UNIQUE(name),
    CHECK (length(name) > 0),
    CHECK (length(registration_id) > 0),
    CHECK (length(pwd) > 0)
);

-- Labor teams
CREATE TABLE LaborTeams (
    laborteam_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    picture TEXT NOT NULL,
    --
    UNIQUE(name),
    CHECK (length(name) > 0),
    CHECK (length(picture) > 0)
);

CREATE TABLE TeamWorksWithLaborTeams (
    team_id INTEGER NOT NULL REFERENCES Teams(team_id),
    laborteam_id INTEGER NOT NULL REFERENCES LaborTeams(laborteam_id),
    --
    PRIMARY KEY (team_id, laborteam_id)
);

CREATE TABLE Specialty (
    specialty_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    --
    UNIQUE (name),
    CHECK (length(name) > 0)
);

CREATE TABLE TeamNeedsSpecialty (
    specialty_id INTEGER NOT NULL REFERENCES Specialty(specialty_id),
    team_id INTEGER NOT NULL REFERENCES Team(team_id),
    count INTEGER NOT NULL DEFAULT 1,
    --
    UNIQUE (team_id, specialty_id),
    CHECK (count > 0)
);

CREATE TABLE WorkerHasSpecialty (
    worker_id INTEGER NOT NULL REFERENCES Workers(worker_id),
    specialty_id INTEGER NOT NULL REFERENCES Specialty(specialty_id),
    --
    PRIMARY KEY (worker_id, specialty_id)
);

CREATE TABLE Projects (
    project_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    picture TEXT,
    --
    CHECK (length(name) > 0)
);

CREATE TABLE WorkerTeamProject (
    worker_id INTEGER NOT NULL REFERENCES Workers(worker_id),
    team_id INTEGER NOT NULL REFERENCES Team(team_id),
    project_id INTEGER NOT NULL REFERENCES Projects(project_id),
    starts DATETIME NOT NULL,
    ends DATETIME,
    --
    PRIMARY KEY (worker_id, team_id, project_id),
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
