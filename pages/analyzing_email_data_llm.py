import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import pages.table_format as tf

load_dotenv()
# Set up the app



st.set_page_config(page_title="Email Data Chat", page_icon="📊")
st.title("📊 Chat with Your Email Data")
st.caption("Ask questions about your data")

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))




if 'email_data' in st.session_state:
    tf.email_info = st.session_state['email_data']


# File upload

uploaded_file = tf.email_info
print(uploaded_file)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process CSV if uploaded
df = None
if uploaded_file is not None:
    try:
        df = pd.DataFrame(uploaded_file)
        st.success(f"✅ Loaded Emails txt with {len(df)} rows")

        # Show preview
        with st.expander("👀 View first 10 rows"):
            st.dataframe(df.head(10))

        # Add system message with data structure
        if len(st.session_state.messages) == 0:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"I'm ready to analyze your Email file. It has {len(df.columns)} columns: {', '.join(df.columns)}. Ask me anything about this data!"
            })

    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")

# Chat input
if prompt := st.chat_input("Ask about your data..."):
    if df is None:
        st.warning("Please check your emails file or df file first")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare data sample for LLM (first 100 rows)
    sample_data = df.head(100).to_string()

    # Create full prompt with context
    full_prompt = f"""
    Email Data :
    Columns: {', '.join(df.columns)}
    First 100 rows:
    {sample_data}

    User Question: {prompt}

    Answer concisely but thoroughly. If the question requires calculations, 
    explain your approach before giving the final answer.
    """

    # Get LLM response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": full_prompt}],
                    model="llama3-8b-8192",
                    temperature=0.3
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error getting LLM response: {str(e)}")