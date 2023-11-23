import streamlit as st
import subprocess
import os
import json
import threading  # Importing the threading module
import queue  # Importing the queue module
# Assuming run_query is imported correctly
from query_solver import run_query


st.title('AutoGen OpenSource Multi-Agent Python Programming Team')
st.markdown('''The CodeCrafters Team roles:
            -> 1. CodeLlama: The Coding Virtuoso. Role: Lead Developer 
            -> 2. Starcoder: The Assistant Maestro. Role: Assistant Developer
            -> 3. Llama 2: The Versatile Visionary. Role: Project Manager and Generalist ''')

# Retrieve the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
api_base = "https://api.deepinfra.com/v1/openai"

programming_problem = st.text_area("Enter your programming task:", "Write a program that calculates the number of a Hebrew word using the gematria, and write a test for  יהוה which should be 26", height=100)


# Use session state to store and retrieve the programming problem
if 'programming_problem' not in st.session_state:
    st.session_state['programming_problem'] = "Write a program that calculates the number of a Hebrew word using the gematria, and write a test for יהוה which should be 26"


if st.button('Solve'):
    if api_key and programming_problem:
        # Update the session state with the current problem
        st.session_state['programming_problem'] = programming_problem
        
        input_data = {
            "programming_problem": programming_problem,
            "api_key": api_key
        }

        result = subprocess.check_output(
            ["python", "query_solver.py"],
            input=json.dumps(input_data),
            text=True
        )
        st.write(result.strip())
    else:
        st.write("Please provide both Open API key and programming problem.")
