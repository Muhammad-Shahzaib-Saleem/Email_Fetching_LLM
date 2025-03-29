import streamlit as st
import pandas as pd
import os



st.title("Email Reader App")
st.divider()
st.title("Email in table Formats")
st.write("Email Data Frames")

if st.button("Go back to Home"):
    st.switch_page("Home.py")


# Function to read and parse emails with caching
email_info = None
def load_emails(file_path):
    email_data = {
        "Subject": [],
        "From": [],
        "To": [],
        "Date": [],
        "Body": []
    }

    with open(file_path, 'r') as file:
        content = file.read()
        emails = content.split('=========================')

        for email in emails:
            lines = email.strip().split('\n')
            subject = None
            from_ = None
            to = None
            date = None
            body = None

            for i, line in enumerate(lines):
                if line.startswith("Subject:"):
                    subject = line.replace("Subject: ", "").strip()
                elif line.startswith("From:"):
                    from_ = line.replace("From: ", "").strip()
                elif line.startswith("To:"):
                    to = line.replace("To: ", "").strip()
                elif line.startswith("Date:"):
                    date = line.replace("Date: ", "").strip()
                elif line.lower().startswith("body:"):
                    body = "\n".join(lines[i + 1:]).strip()
                    break

            if any([subject, from_, to, date, body]):  # Only add if we have data
                email_data["Subject"].append(subject)
                email_data["From"].append(from_)
                email_data["To"].append(to)
                email_data["Date"].append(date)
                email_data["Body"].append(body)

    return email_data



# Load the data
file_path = '../Read_Email/emails.txt'
email_data = load_emails(file_path)

#state of session email_data
st.session_state['email_data'] = email_data
email_info = email_data
# Display the dataframe
df = pd.DataFrame(email_data)
st.dataframe(df)

st.divider()

