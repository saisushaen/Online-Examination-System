create table Student(
  Email varchar(60) NOT NULL PRIMARY KEY,
  Name varchar(60) NOT NULL,
  USN varchar(30) NOT NULL,
  Department varchar(10),
  Ph_No varchar(30),
  Gender varchar(15),
  DOB date,
  Password varchar(200) NOT NULL);

create table Staff(
  Email varchar(60) NOT NULL PRIMARY KEY,
  Name varchar(60) NOT NULL,
  Staff_id varchar(30) NOT NULL,
  Department varchar(10),
  Ph_No varchar(30),
  Gender varchar(15),
  DOB date,
  Password varchar(200) NOT NULL);

CREATE TABLE IF NOT EXISTS Quiz (
  Quizid int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Quizname varchar(50) NOT NULL,
  Date_created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Mail varchar(60) DEFAULT NULL,
  FOREIGN KEY(Mail) REFERENCES staff(Email));

INSERT INTO Quiz VALUES
(4, 'c quiz', '2019-11-18 16:13:50', 'NSGMAIL'),
(5, 'c++ quiz', '2019-11-18 16:17:13', 'rakeshmr723@gmail.com'),
(6, 'english', '2019-11-18 17:04:12', 'BHATVINAYAK94@GMAIL.COM');

CREATE TABLE IF NOT EXISTS Questions (
  Question varchar(700) PRIMARY KEY NOT NULL,
  Op1 varchar(50) NOT NULL,
  Op2 varchar(50),
  Op3 varchar(50),
  Op4 varchar(50),
  Answer varchar(50) NOT NULL,
  Quiz_id int NOT NULL,
  FOREIGN KEY(Quiz_id) REFERENCES Quiz(Quizid)
);

INSERT INTO Questions VALUES
('C primiarily developed as..', 'General purpose language', 'Data processing language D.', 'None of the above.', 'System programming language  ','System programming language  ', 4),
('C programs converted into machine language with the help of..', 'An Editor  ', 'An operating system', ' None of these.', 'A compiler  ','A compiler  ', 4),
('No. of consonant in english language is..', '20', '22', '28', '21','21', 4),
('No. of vowels in english language is..', '3', '4', '7', '5','5', 4),
('Total no of letters in english language is..', '23', '24', '25', '26','26', 4),
('When a copy constructor may be called?', 'When an object of the class is', 'When an object of the class is', 'When an object is constructed ', 'All of the above','All of the above', 4),
('Which of the following functions must use reference.', 'Assignment operator function', 'Destructor', 'Parameterized constructor', 'Copy Constructor','Copy Constructor', 4),
('Which of the following is FALSE about references in C++', 'References cannot be NULL', 'A reference must be initialize', 'Once a reference is created, i', 'References cannot refer to con','References cannot refer to con', 4),
('Which of the following operators cannot be overloaded', '. (Member Access or Dot operat', '?: (Ternary or Conditional Ope', ':: (Scope Resolution Operator)', 'All of the above','All of the above', 4),
('Which of the followings is/are automatically added to every class, if we do not write our own.', 'Copy Constructor', 'Assignment Operator', 'A constructor without any para', 'All of the above','All of the above', 4),
('Who is the father of C language?', 'Bjarne Stroustrup', 'James A. Gosling  ', 'Dr. E.F. Codd', 'Dennis Ritchie  ','Dennis Ritchie  ', 4);


CREATE TABLE Score(
  Slno int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  Score int NOT NULL,
  Quizid int NOT NULL,
  Email varchar(60) NOT NULL,
  FOREIGN KEY(Email) REFERENCES Student(Email),
  FOREIGN KEY(Quizid) REFERENCES Quiz(Quizid)
);



-- select Email,Name,USN,Department,Ph_No,Quizid,Score FROM Student NATURAL JOIN Score;

--TRIGGER
DELIMITER $$
create trigger trig before insert on Quiz for each row
begin
  declare dt datetime;
  SELECT NOW() INTO dt;
  SET NEW.Date_created=dt;
end
$$
DELIMITER ;

--FUNCTION
DELIMITER $$
CREATE FUNCTION Total_Students_2(Qid int) RETURNS INT
begin
  declare Cnt int;
  select count(*) INTO Cnt from Score where Quizid=Qid;
  return Cnt;
end
$$
DELIMITER ;
---
DELIMITER $$
CREATE FUNCTION Avg_Score_2(Qid int) RETURNS INT
begin
  declare avgg int;
  select avg(Score) INTO avgg from Score where Quizid=Qid;
  return avgg;
end
$$
DELIMITER ;

--procedure
DELIMITER $$
CREATE PROCEDURE Check_Date_2(IN dob date,OUT msg varchar(10))
BEGIN
  IF dob>CURRENT_DATE THEN
    SET msg="INVALID";
  ELSE
    SET msg="VALID";
  END IF;
END;
$$
DELIMITER ;
--------

DELIMITER $$
CREATE PROCEDURE Check_Ppl_2(IN e varchar(20),OUT msg varchar(10))
BEGIN
  IF e in (select Email from Student) THEN
  -- IF dob>CURRENT_DATE THEN
    SET msg="INVALID";
  ELSE
    SET msg="VALID";
  END IF;
END;
$$
DELIMITER ;