-- Constructure 1.0
-- Bojun Wang, May 2018
-- Sqlite3

CREATE TABLE Todos (
    worker_id INTEGER NOT NULL,
    --
    UNIQUE(worker_id)
);