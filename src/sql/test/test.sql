INSERT INTO Teams (team_id, name) VALUES (1, 'Zhejiang No.1 Construction Team');
INSERT INTO Teams (team_id, name) VALUES (2, 'Shanghai Yunfeng Construction Team');
INSERT INTO Teams (team_id, name) VALUES (3, 'Jiangsu University of Architecture Construction Team');
INSERT INTO Teams (team_id, name) VALUES (4, 'Sichuan No.22 Construction Team');
INSERT INTO Teams (team_id, name) VALUES (5, 'Shanghai Engineering Construction Cooperation');

INSERT INTO Speciality (speciality_id, name) VALUES (1, 'general manager');
INSERT INTO Speciality (speciality_id, name) VALUES (2, 'techical advisor');
INSERT INTO Speciality (speciality_id, name) VALUES (3, 'estimate clerks');
INSERT INTO Speciality (speciality_id, name) VALUES (4, 'security officer');
INSERT INTO Speciality (speciality_id, name) VALUES (5, 'elevator driver');
INSERT INTO Speciality (speciality_id, name) VALUES (6, 'construction worker');
INSERT INTO Speciality (speciality_id, name) VALUES (7, 'quality staff');

INSERT INTO TeamNeedsSpeciality VALUES (1,1,2);
INSERT INTO TeamNeedsSpeciality VALUES (2,1,2);
INSERT INTO TeamNeedsSpeciality VALUES (3,1,1);
INSERT INTO TeamNeedsSpeciality VALUES (6,1,20);

INSERT INTO TeamNeedsSpeciality VALUES (3,2,2);
INSERT INTO TeamNeedsSpeciality VALUES (4,2,2);
INSERT INTO TeamNeedsSpeciality VALUES (5,2,1);
INSERT INTO TeamNeedsSpeciality VALUES (6,2,20);

INSERT INTO TeamNeedsSpeciality VALUES (1,3,2);
INSERT INTO TeamNeedsSpeciality VALUES (2,3,2);
INSERT INTO TeamNeedsSpeciality VALUES (3,3,1);
INSERT INTO TeamNeedsSpeciality VALUES (6,3,20);

INSERT INTO TeamNeedsSpeciality VALUES (3,4,2);
INSERT INTO TeamNeedsSpeciality VALUES (4,4,2);
INSERT INTO TeamNeedsSpeciality VALUES (5,4,1);
INSERT INTO TeamNeedsSpeciality VALUES (6,4,20);

INSERT INTO TeamNeedsSpeciality VALUES (1,5,2);
INSERT INTO TeamNeedsSpeciality VALUES (4,5,2);
INSERT INTO TeamNeedsSpeciality VALUES (5,5,1);
INSERT INTO TeamNeedsSpeciality VALUES (6,5,20);

INSERT INTO Places (place_id, name) VALUES (1, 'Zhejiang,Shangyu');
INSERT INTO Places (place_id, name) VALUES (2, 'Shanghai');
INSERT INTO Places (place_id, name) VALUES (3, 'Sichuan,Nanbu');
INSERT INTO Places (place_id, name) VALUES (4, 'Sichuan,Jiangge');
INSERT INTO Places (place_id, name) VALUES (5, 'Zhejiang,Jiangshan');
INSERT INTO Places (place_id, name) VALUES (6, 'Anhui,Yingshang');

-- Place 1
INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (1, "Pan Guodong", 42, 10, 1, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (1, 1);
INSERT INTO WorkerPartOfTeam VALUES (1, 1, "2014-04-05 00:00:00.000", "2016-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (1, 5, "2017-01-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (2, "Dong Jianzhe", 54, 18, 1, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (2, 2);
INSERT INTO WorkerPartOfTeam VALUES (2, 1, "2012-04-05 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (2, 5, "2016-01-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (3, "Feng Zheqi", 30, 8, 1, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (3, 3);
INSERT INTO WorkerPartOfTeam VALUES (3, 2, "2012-08-01 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (3, 5, "2014-01-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (4, "Zhao Jianmu", 32, 11, 1, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (4, 4);
INSERT INTO WorkerPartOfTeam VALUES (4, 2, "2013-12-05 00:00:00.000", "2014-11-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (4, 5, "2018-01-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (5, "Xu Youlin", 44, 21, 1, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (5, 5);
INSERT INTO WorkerPartOfTeam VALUES (5, 3, "2011-04-30 00:00:00.000", "2014-02-18 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (5, 5, "2018-01-01 00:00:00.000", NULL, 1);

-- Place 2
INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (6, "Hu Bihong", 42, 10, 2, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (6, 2);
INSERT INTO WorkerPartOfTeam VALUES (6, 2, "2014-04-08 00:00:00.000", "2016-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (6, 5, "2017-03-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (7, "Zhu Wei", 54, 18, 2, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (7, 3);
INSERT INTO WorkerPartOfTeam VALUES (7, 3, "2012-04-08 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (7, 2, "2016-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (8, "Wang Lijiang", 30, 8, 2, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (8, 4);
INSERT INTO WorkerPartOfTeam VALUES (8, 2, "2012-02-01 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (8, 5, "2014-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (9, "Zhu Jianrong", 32, 11, 2, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (9, 5);
INSERT INTO WorkerPartOfTeam VALUES (9, 3, "2013-11-05 00:00:00.000", "2014-11-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (9, 5, "2018-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (10, "Wang Youlin", 44, 21, 2, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (10, 6);
INSERT INTO WorkerPartOfTeam VALUES (10, 3, "2011-03-30 00:00:00.000", "2014-02-18 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (10, 5, "2018-02-01 00:00:00.000", NULL, 1);

-- Place 3
INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (11, "Fu Zengming", 42, 10, 3, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (11, 2);
INSERT INTO WorkerPartOfTeam VALUES (11, 4, "2014-04-08 00:00:00.000", "2016-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (11, 5, "2017-03-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (12, "Li Junhua", 54, 18, 3, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (12, 3);
INSERT INTO WorkerPartOfTeam VALUES (12, 4, "2012-04-08 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (12, 5, "2016-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (13, "Dong Zhongyuan", 30, 8, 3, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (13, 4);
INSERT INTO WorkerPartOfTeam VALUES (13, 4, "2012-02-01 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (13, 5, "2014-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (14, "Cheng Jianggang", 32, 11, 3, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (14, 5);
INSERT INTO WorkerPartOfTeam VALUES (14, 4, "2013-11-05 00:00:00.000", "2014-11-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (14, 5, "2018-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (15, "Zeng Fuming", 44, 21, 3, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (15, 6);
INSERT INTO WorkerPartOfTeam VALUES (15, 4, "2011-03-30 00:00:00.000", "2014-02-18 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (15, 5, "2018-02-01 00:00:00.000", NULL, 1);

-- Place 4
INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (16, "Zhang Zhikang", 42, 10, 4, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (16, 1);
INSERT INTO WorkerPartOfTeam VALUES (16, 2, "2014-04-08 00:00:00.000", "2016-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (16, 4, "2017-03-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (17, "Xia Mingjie", 54, 18, 4, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (17, 3);
INSERT INTO WorkerPartOfTeam VALUES (17, 3, "2012-04-08 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (17, 4, "2016-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (18, "Zhao Shoutian", 30, 8, 4, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (18, 4);
INSERT INTO WorkerPartOfTeam VALUES (18, 2, "2012-02-01 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (18, 5, "2014-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (19, "Xu Jianyang", 32, 11, 4, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (19, 5);
INSERT INTO WorkerPartOfTeam VALUES (19, 3, "2013-11-05 00:00:00.000", "2014-11-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (19, 4, "2018-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (20, "Gu Xiangwei", 44, 21, 4, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (20, 6);
INSERT INTO WorkerPartOfTeam VALUES (20, 2, "2011-03-30 00:00:00.000", "2014-02-18 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (20, 4, "2018-02-01 00:00:00.000", NULL, 1);


-- Place 5
INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (21, "Huang Yaling", 42, 10, 5, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (21, 1);
INSERT INTO WorkerPartOfTeam VALUES (21, 5, "2014-04-08 00:00:00.000", "2016-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (21, 4, "2017-03-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (22, "Ye Huo", 54, 18, 5, "College");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (22, 3);
INSERT INTO WorkerPartOfTeam VALUES (22, 3, "2012-04-08 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (22, 4, "2016-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (23, "Du Kanshi", 30, 8, 5, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (23, 4);
INSERT INTO WorkerPartOfTeam VALUES (23, 3, "2012-02-01 00:00:00.000", "2013-08-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (23, 4, "2014-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (24, "Yan Chunying", 32, 11, 5, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (24, 5);
INSERT INTO WorkerPartOfTeam VALUES (24, 3, "2013-11-05 00:00:00.000", "2014-11-01 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (24, 4, "2018-02-01 00:00:00.000", NULL, 1);

INSERT INTO Workers (worker_id, name, age, work_age, place_id, education) VALUES (25, "Song Xiaoying", 44, 21, 5, "High School");
INSERT INTO WorkerHasSpeciality (worker_id, speciality_id) VALUES (25, 6);
INSERT INTO WorkerPartOfTeam VALUES (25, 2, "2011-03-30 00:00:00.000", "2014-02-18 00:00:00.000", 1);
INSERT INTO WorkerPartOfTeam VALUES (25, 4, "2018-02-01 00:00:00.000", NULL, 1);



