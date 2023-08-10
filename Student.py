import streamlit as st
import pandas as pd
from sqlFunctions import insert_student
from sqlFunctions import validate_student
from sqlFunctions import show_quizzes
from sqlFunctions import get_quiz
from sqlFunctions import submit_score
from sqlFunctions import show_score_student
from sqlFunctions import change_Password_student
from sqlFunctions import validate_date

st.header("**Welcome Student**")

# st.tabs(["1","2"])
if 'login_boolean' not in st.session_state:
    st.session_state['login_boolean'] = False
if 'username' not in st.session_state:
    st.session_state['username']=None
# login_boolean=False
# sb=st.sidebar.radio("Choose",["Login","Signup"])
sb=st.sidebar.selectbox("Navigate",["Login","Signup","Take Test","Show Scores","Change Password"])
username=None

if sb=='Login':
    st.header("**Login**")
    # user=st.selectbox("Select Role",["Student","Staff"])
    username=st.text_input("UserName")
    password=st.text_input("Password",type="password")
    if st.button("Login"):
        # st.write("Username:",username)
        # st.write("Password:",password)
        if username=='' or password=='':
            st.warning("Bad Credentials")
        elif (validate_student(username,password)):
            st.success("Logged in successfully,PLEASE NAVIGATE TO OTHER TAB",icon="✅")
            # st.sidebar.selectbox("Navigate",["Home","Take Test","Show Scores"])
            # login_boolean=True\
            st.session_state['username']=username
            st.session_state["login_boolean"]=True
            st.balloons()
        else:
            st.warning("Bad Credentials")

elif sb=='Signup':
    st.header("**Signup**")
    # user_type=st.radio("Choose",["Student","Staff"])
    # st.subheader("Student")
    name=st.text_input("Name")
    usn=st.text_input("USN")
    email=st.text_input("Email")
        # phno=st.text_input("PhoneNumber")
    phno=st.number_input("Phone Number",format="%s")
    dept=st.selectbox("Department",["CSE","ECE","MECH"])
    dob=st.date_input("Enter Date Of Birth")
    gender=st.radio("Gender",["Male","Female"])
    password=st.text_input("Password",type="password")
    confirm_password=st.text_input("Confirm Password",type="password")
    signup_submit=st.button("Sign Up")
    l=[email,name,usn,dept,phno,gender,dob,password]
    if signup_submit:
        if(validate_date(dob)[0][0]=='INVALID'):
            st.warning("DOB Should be before today")
        else:
            if password==confirm_password and confirm_password!="":
                st.success("Registered successfully.Please Login Again")
                insert_student(l)
                # st.write(l)
        # mydb = mysql.connector.connect(host="localhost",user="root",database="project_test2")
        # cur=mydb.cursor()
        # cur.execute("INSERT INTO Student VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7]))
        # mydb.commit()

                st.balloons()
            else:
                st.warning("Enter same password in both fields")

elif sb=="Take Test" and st.session_state['login_boolean']:
    st.subheader("Take Test")
    available_quizzes=show_quizzes()
    sbq=st.selectbox("Select from The following",["Show Available quizzes","Take a Quiz"])
    if sbq=="Show Available quizzes":
        av=pd.DataFrame(available_quizzes)
        av.columns=["Quiz ID","Quiz Name"]
        st.table(av)
    elif sbq=="Take a Quiz":
        q_id=[]
        for i in available_quizzes:
            q_id.append(i[0])
        quiz_selection=st.selectbox("Choose a quiz",q_id)
        quiz_questions=get_quiz(quiz_selection)
        ques_opt_id=[]
        ans=[]
        ind=0
        # st.write(quiz_questions)
        for i in quiz_questions.keys():
            # st.write(i)
            st.text("{}".format(quiz_questions[i][0][0]))
            # st.markdown("<h2>{}</h2>".format(quiz_questions[i][0][0]))
            ques_opt_id.append(st.radio("Choose a option",quiz_questions[i][1]))
            ans.append(quiz_questions[i][2][0])
            ind+=1
        # st.write(ques_opt_id)
        # st.write(ans)
        score=0
        # st.write(st.session_state['username'])
        if st.button("Submit"):
            for i in range(len(ques_opt_id)):
                if ques_opt_id[i]==ans[i]:
                    score+=1
            st.subheader("Score:{}".format(score))
            submit_score(score,quiz_selection,st.session_state['username'])

elif sb=="Show Scores" and st.session_state['login_boolean']:
    st.subheader("Show Scores")
    score=show_score_student(st.session_state['username'])
    score=pd.DataFrame(score)
    score.columns=['Quiz Id', 'Score']
    st.dataframe(score)

elif sb=="Change Password" and st.session_state['login_boolean']:
    np=st.text_input("Enter new Password")
    cnp=st.text_input("Confirm new Password")
    if st.button("Submit"):
        if np==cnp and np!="":
            change_Password_student(np,st.session_state["username"])
            st.success("Password Changed Successfully")
        else:
            st.warning("Enter same password in both fields")