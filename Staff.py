import streamlit as st
import pandas as pd
from sqlFunctions import insert_staff
from sqlFunctions import validate_staff
from sqlFunctions import show_score_staff
from sqlFunctions import insert_to_questions
from sqlFunctions import create_quiz
from sqlFunctions import show_quizid
from sqlFunctions import show_quizzes
from sqlFunctions import change_Password_staff
from sqlFunctions import get_students_attended
from sqlFunctions import get_average_score
from sqlFunctions import delete_Question
from sqlFunctions import get_questions
from sqlFunctions import show_questions_staff


st.header("**Welcome Staff**")

if 'login_boolean' not in st.session_state:
    st.session_state['login_boolean'] = False
if 'username' not in st.session_state:
    st.session_state['username']=None

# sb=st.sidebar.radio("Choose",["Login","Signup"])
sb=st.sidebar.selectbox("Navigate",["Login","Signup","Create Test","Delete Questions","Stats","Change Password"])
# opt=st.sidebar.selectbox("Navigate",["Home","SignOut"],disabled=st.session_state['selectState'])

if sb=='Login':
    st.header("**Login**")
    # user=st.selectbox("Select Role",["Student","Staff"])
    username=st.text_input("UserName")
    password=st.text_input("Password",type="password")
    if st.button("Login"):
        # st.write("Username:",username)
        # st.write("Password:",password)
        # st.success("Logged in successfully",icon="✅")
        # st.session_state['selectState']=False
        if username=='' or password=='':
            st.warning("Bad Credentials")
        elif (validate_staff(username,password)):
            st.success("Logged in successfully,PLEASE NAVIGATE TO OTHER TAB",icon="✅")
            # sb1=st.sidebar.selectbox("Navigate",["Home","Create Test","Show Scores"])
            # if(sb1=="Create Test"):
            #     st.header("Create")
            st.session_state['username']=username
            st.session_state['login_boolean'] = True
            st.balloons()
        else:
            st.warning("Bad Credentials")

elif sb=='Signup':
    st.header("**Signup**")
    # user_type=st.radio("Choose",["Student","Staff"])
    # st.subheader("Student")
    name=st.text_input("Name")
    usn=st.text_input("Staff Id")
    email=st.text_input("Email")
        # phno=st.text_input("PhoneNumber")
    phno=st.number_input("Phone Number",format="%s")
    dept=st.selectbox("Department",["CSE","ECE","MECH"])
    dob=st.date_input("Enter Date Of Birth")
    gender=st.radio("Gender",["Male","Female"])
    password=st.text_input("Password")
    confirm_password=st.text_input("Confirm Password",type="password")
    signup_submit=st.button("Sign Up")
    l=[email,name,usn,dept,phno,gender,dob,password]
    if signup_submit:
        if password==confirm_password and confirm_password!="":
            st.success("Registered successfully")
            insert_staff(l)
            st.session_state['selectState']=False

            # st.write(l)
        # opt.disabled=False
        # mydb = mysql.connector.connect(host="localhost",user="root",database="project_test2")
        # cur=mydb.cursor()
        # cur.execute("INSERT INTO Student VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7]))
        # mydb.commit()
            st.balloons()
        else:
            st.warning("Enter same password in both fields")

elif sb=="Create Test" and st.session_state['login_boolean']:
    st.subheader("Create Test")
    stsb=st.selectbox("What to do",["Create a new Quiz","Add questions to a Quiz"])
    if stsb=="Create a new Quiz":

        q_id=st.number_input("Enter a new Quiz Id",min_value=1,step=1)
        q_name=st.text_input("Enter new Quiz name")
        if st.button("Done"):
            # create_quiz(q_id,q_name,st.session_state['username'],datetime.now())
            create_quiz(q_id,q_name,st.session_state['username'])
            st.success("New Quiz CreateD!,Go to next tab to add Questions")
        

    elif stsb=="Add questions to a Quiz":
        available_quizzes=show_quizzes()
        quiz_id=st.selectbox("Please select a quiz from below",available_quizzes)[0]
        st.write(quiz_id)
        no_of_questions=st.number_input("Input Number Of Questions For Test",step=1)
        # st.write(no_of_questions)
        col=[]
        ind=0
        # ans_opt=[]
        # ans=[]
        for i in range(no_of_questions):
            ques=st.text_input("Enter Question {}".format(i+1))
            # col.append(st.columns(4))
            col.append(1)
            col.append(2)
            col.append(3)
            col.append(4)
            col[ind], col[ind+1], col[ind+2] ,col[ind+3] = st.columns(4)
            with col[ind]:
                op1=st.text_input("{} Option1".format(i+1))
            with col[ind+1]:
                op2=st.text_input("{} Option2".format(i+1))
            with col[ind+2]:
                op3=st.text_input("{} Option3".format(i+1))
            with col[ind+3]:
                op4=st.text_input("{} Option4".format(i+1))
            ans_opt=st.number_input("Choose Correct Option FOR Question {}".format(i+1),min_value=1,max_value=4,step=1)
            if ans_opt==1:
                ans=op1
            elif ans_opt==2:
                ans=op2
            elif ans_opt==3:
                ans=op3
            elif ans_opt==4:
                ans=op4
            if st.button("Done for Question {}".format(i+1)):
                # st.write(ques,op1,op2,op3,op4,ans,quiz_id)
                insert_to_questions(ques,op1,op2,op3,op4,ans,quiz_id)
                ques_inserted=show_questions_staff(quiz_id)
                ques_inserted=pd.DataFrame(ques_inserted)
                ques_inserted.columns=['Questions','Option1','Option2','Option3','option4','Ans','Quiz ID']
                st.table(ques_inserted)
            ind+=4
        
elif sb=="Delete Questions" and st.session_state['login_boolean']:
    st.subheader("Delete Questions")
    available_quizzes=show_quizzes()
    q_id=[]
    for i in available_quizzes:
        q_id.append(i[0])
    quiz=st.selectbox("Select Quiz",q_id)
    questions=get_questions(quiz)
    ques_id=[]
    for i in questions:
        ques_id.append(i[0])
    ques=st.selectbox("Select Question",ques_id)
    if st.button("Delete"):
        delete_Question(ques)

elif sb=="Stats" and st.session_state['login_boolean']:
    available_quizzes=show_quizzes()
    q_id=[]
    for i in available_quizzes:
        q_id.append(i[0])

    choose=st.selectbox("Select one",["Show Scores","Number of students attended","Average Score"])

    if choose=="Show Scores":
        st.subheader("Show Scores")
        available_quizzes=show_quizid()
        qid=st.selectbox("Enter Quiz ID:",available_quizzes)
        n1=get_students_attended(qid[0])
        if(n1[0][0]==0):
            st.subheader("No Attempts")
        else:
            score=show_score_staff(qid[0])
            score=pd.DataFrame(score)
            score.columns=["Email","Name","USN","Department","Ph_No","Quiz ID","Score"]
            st.table(score)
    
    elif choose=="Number of students attended":
        q_id_select=st.selectbox("Please select a Quiz",q_id)
        n1=get_students_attended(q_id_select)
        st.subheader(n1[0][0])
    elif choose=="Average Score":
        q_id_select2=st.selectbox("Please select a Quiz",q_id)
        n2=get_average_score(q_id_select2)
        st.subheader(n2[0][0])

elif sb=="Change Password" and st.session_state['login_boolean']:
    np=st.text_input("Enter new Password")
    cnp=st.text_input("Confirm new Password")
    if st.button("Submit"):
        if np==cnp and np!="":
            change_Password_staff(np,st.session_state["username"])
            st.success("Password Changed Successfully")
        else:
            st.warning("Enter same password in both fields")