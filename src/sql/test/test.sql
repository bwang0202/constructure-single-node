INSERT INTO Teams (name) VALUES ('HunanTeam1');

INSERT INTO Speciality (name) VALUES ('wood');

INSERT INTO TeamNeedsSpeciality VALUES (1,1,10);

INSERT INTO Places (name) VALUES ('hunan');

INSERT INTO Workers (name, age, work_age, place_id, education) VALUES ("worker1", 25, 5, 1, "zs");
INSERT INTO Workers (name, age, work_age, place_id, education) VALUES ("worker2", 25, 5, 1, "zs");
INSERT INTO Workers (name, age, work_age, place_id, education) VALUES ("worker3", 25, 5, 1, "zs");

INSERT INTO WorkerHasSpeciality VALUES (1, 1);
INSERT INTO WorkerHasSpeciality VALUES (2, 1);
INSERT INTO WorkerHasSpeciality VALUES (3, 1);


INSERT INTO WorkerPartOfTeam VALUES (1, 1, "2010-01-01 00:00:00.000", NULL, 1);

INSERT INTO WorkerPartOfTeam VALUES (2, 1, "2017-01-01 00:00:00.0000", NULL, 1);
INSERT INTO WorkerPartOfTeam VALUES (3, 1, "2010-01-01 00:00:00.000", "2011-01-01 00:00:00.000", 1);
