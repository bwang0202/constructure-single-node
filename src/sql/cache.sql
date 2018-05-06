
CREATE TABLE MatchedWorkers (
	worker_id1 INTEGER NOT NULL,
	worker_id2 INTEGER NOT NULL,
	score INTEGER NOT NULL DEFAULT 0,
	--
	PRIMARY KEY (worker_id1, worker_id2),
	CHECK (score >= 0 and score <= 100),
	CHECK (worker_id1 < worker_id2) # No duplicate
);

CREATE TABLE MatchedWorkerTeam (
	worker_id INTEGER NOT NULL,
	team_id INTEGER NOT NULL,
	score INTEGER NOT NULL DEFAULT 0,
	--
	PRIMARY KEY (team_id, worker_id),
	CHECK (score >= 0 and score <= 100)
);