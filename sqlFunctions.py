from numpy import insert
import streamlit as st
import mysql.connector

mydb = mysql.connector.connect(host="localhost",user="root",database="Project_Final")
cur=mydb.cursor()

def insert_student(l):
    
    cur.execute("INSERT INTO Student VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7]))
    mydb.commit()
    # l.sort()

def insert_staff(l):

    # mydb = mysql.connector.connect(host="localhost",user="root",database="project_test2")
    # cur=mydb.cursor()
    cur.execute("INSERT INTO Staff VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7]))
    mydb.commit()

def validate_student(username,password):
        cur.execute("Select Email,Password from Student where Email='{}';".format(username))
        # c.execute('SELECT * FROM Train WHERE Name="{}"'.format(train_name))

        u=cur.fetchall()
        # st.write(u)
        if(len(u)):
            # cur.execute("Select Email,Password from Student where Email=%s and Password=%s"(username,password))
            # p=cur.fetchall()
            # st.write(p)
            if(password==u[0][1]):
                return True
            else:
                return False

        # st.write(u)
        return 

def validate_staff(username,password):
        cur.execute("Select Email,Password from Staff where Email='{}';".format(username))
        # c.execute('SELECT * FROM Train WHERE Name="{}"'.format(train_name))

        u=cur.fetchall()
        # st.write(u)
        if(len(u)):
            # cur.execute("Select Email,Password from Student where Email=%s and Password=%s"(username,password))
            # p=cur.fetchall()
            # st.write(p)
            if(password==u[0][1]):
                return True
            else:
                return False

        # st.write(u)
        return False

def show_quizzes():
    cur.execute("select Quizid,Quizname from Quiz;")
    available_quizzes=cur.fetchall()
    return available_quizzes

def show_quizid():
    cur.execute("select Quizid from Quiz;")
    available_quizzes=cur.fetchall()
    return available_quizzes

def get_quiz(quiz_id):
    cur.execute("select Question,Op1,Op2,Op3,Op4,Answer from Questions where Quiz_id={};".format(quiz_id))
    get_questions=cur.fetchall()
    # st.write(get_questions)
    ques={}
    for i in range(len(get_questions)):
        ques[i]=[[get_questions[i][0]],[get_questions[i][1],get_questions[i][2],get_questions[i][3],get_questions[i][4]],[get_questions[i][5]]]
    # st.write(ques)
    return ques

def submit_score(score,quiz_id,email):
    cur.execute("INSERT INTO Score(Score,Quizid,Email) VALUES(%s,%s,%s);",(score,quiz_id,email))
    mydb.commit()

def show_score_student(email):
    cur.execute("select Quizid,Score from Score WHERE Email='{}';".format(email))
    score=cur.fetchall()
    return score
    # st.dataframe(score)

def show_score_staff(qid):
    # cur.execute("select * from Score2;")
    cur.execute("select Email,Name,USN,Department,Ph_No,Quizid,Score FROM Student NATURAL JOIN Score where Quizid='{}';".format(qid))
    score=cur.fetchall()
    return score
    # st.dataframe(score)

def insert_to_questions(ques,op1,op2,op3,op4,ans,quiz_id):
    cur.execute("INSERT INTO Questions VALUES(%s,%s,%s,%s,%s,%s,%s);",(ques,op1,op2,op3,op4,ans,quiz_id))
    mydb.commit()

# def create_quiz(q_id,q_name,user,date):
#     cur.execute("INSERT INTO Quiz VALUES(%s,%s,%s,%s);",(q_id,q_name,date,user))
#     mydb.commit()

def create_quiz(q_id,q_name,user):
    cur.execute("INSERT INTO Quiz(Quizid,Quizname,Mail) VALUES(%s,%s,%s);",(q_id,q_name,user))
    mydb.commit()

def change_Password_staff(password,email):
    cur.execute("update Staff set Password='{}' where Email='{}';".format(password,email))
    mydb.commit()

def change_Password_student(password,email):
    cur.execute("update Student set Password='{}' where Email='{}';".format(password,email))
    mydb.commit()

def get_students_attended(qid):
    cur.execute("Select Total_Students_2({});".format(qid))
    number=cur.fetchall()
    return number

def get_average_score(qid):
    cur.execute("Select Avg_Score_2({});".format(qid))
    number=cur.fetchall()
    return number

def validate_date(date):
    cur.execute("call Check_Date_2('{}',@ans);".format(date))
    cur.execute("select @ans")
    validity=cur.fetchall()
    return validity

def delete_Question(q):
    cur.execute("delete from questionS where Question='{}';".format(q))
    mydb.commit()

def get_questions(qid):
    cur.execute("Select Question from Questions where Quiz_id={}".format(qid))
    ans=cur.fetchall()
    return ans

def show_questions_staff(qid):
    cur.execute("Select * from Questions where Quiz_id={}".format(qid))
    ans=cur.fetchall()
    return ans
