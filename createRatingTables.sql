Drop table if exists springWithRatings;
Create table springWithRatings (
Cnum text, 
CTime text, 
CDay text, 
CType text, 
ProfID integer, 
SchoolID integer, 
totalRating float,
CourseCode text);

insert into springWithRatings select Cnum, springSchedule.Time, Days, type, Professor_Ratings.profNum, Professor_Ratings.schoolCode, Professor_Ratings.totRating, courseCode  from springSchedule, Professor_Ratings WHERE springSchedule.Professor = Professor_Ratings.lastWithInitial;

Drop Table IF EXISTS ProfessorInfo;
Create Table ProfessorInfo (
ProfessorID INTEGER,
ProfessorWInitial TEXT,
totalRating float);

insert into ProfessorInfo select Professor_Ratings.profNum, Professor_Ratings.lastWithInitial, Professor_Ratings.totRating from Professor_Ratings;

Drop Table IF Exists CourseTitle;
Create table CourseTitle(
courseCode TEXT,
courseName TEXT);

insert into  CourseTitle select distinct springSchedule.courseCode, springSchedule.courseTitle from springSchedule;