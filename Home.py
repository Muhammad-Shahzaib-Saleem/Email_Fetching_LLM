import streamlit as st
import email_reading_functionality as erf
import pandas as pd



st.title("Email Reader App")

st.divider()

st.session_state.userEmail = 'shazijutt987@gmail.com'
st.session_state.userPassword = 'odvytziddubmyasc'


user_email = st.text_input("Enter your Email", placeholder="Enter your email",key= "userEmail")
app_password = st.text_input("Enter your Gmail App Generated Password", type="password",
                                 placeholder="Enter app password",  key="userPassword")
from_email = st.text_input("From which email you want see", placeholder="Enter From email", key="fromEmail")


option_map = ["inbox","sent","drafts","trash","starred"]

mail_box = st.pills(label="Mail Box",options=option_map, )


if st.button("Submit",use_container_width=True):

    if not user_email or not app_password or not from_email or not mail_box :
        st.error("All field mandatory,Please input data")

    else:
        if "@" not in user_email or "." not in user_email:
            st.error("Please enter the valid email")
        elif "@" not in from_email or "." not in from_email:
            st.error("Please enter the valid from email")
        else:
            erf.fetching_email(user_email,app_password,from_email,mail_box)

st.divider()







col1, col2 = st.columns(2)
with col1:
    on = st.toggle("Table Format")
    if on:
        st.switch_page("../Read_Email/pages/table_format.py")
with col2:
    on_chat = st.toggle("Chat LLM")
    if on_chat:
        st.switch_page("../Read_Email/pages/analyzing_email_data_llm.py")

st.divider()

with open("/Users/dotenterprises/Desktop/AI-IT Oasis/Read_Email/emails.txt") as f:
        st.write(f.read())





