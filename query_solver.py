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

# Function to handle streaming of subprocess output
def stream_subprocess_output(input_data, placeholder):
    process = subprocess.Popen(
        ["python", "query_solver.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Send input data to the subprocess
    process.stdin.write(json.dumps(input_data))
    process.stdin.close()

    # Initialize a variable to store the final result
    final_result = ""

    # Read the output of the subprocess and update the placeholder
    for line in iter(process.stdout.readline, ''):
        placeholder.write(line)
        final_result += line

    process.stdout.close()
    return final_result.strip()
    
# Initialize session state for storing problems and results
if 'problem_history' not in st.session_state:
    st.session_state['problem_history'] = []
if 'result_history' not in st.session_state:
    st.session_state['result_history'] = []

programming_problem = st.text_area("Enter your programming task:", "Write a program that calculates the number of a Hebrew word using the gematria, and write a test for  יהוה which should be 26", height=100)

# Define file paths
CHAT_HISTORY_PATH = "chat_history.txt"

def save_chat_history(problem, result):
    with open(CHAT_HISTORY_PATH, "a") as file:
        file.write(f"Problem: {problem}\nResult: {result}\n\n")

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_PATH):
        with open(CHAT_HISTORY_PATH, "r") as file:
            return file.read()
    else:
        return "No chat history found."



# Use session state to store and retrieve the programming problem
if 'programming_problem' not in st.session_state:
    st.session_state['programming_problem'] = "Write a program that calculates the number of a Hebrew word using the gematria, and write a test for יהוה which should be 26"


if st.button('Solve'):
    if api_key and programming_problem:
        input_data = {
            "programming_problem": programming_problem,
            "api_key": api_key
        }

        # Create a placeholder for live streaming output
        stream_placeholder = st.empty()

        # Start a thread to handle the streaming of subprocess output
        streaming_thread = threading.Thread(
            target=stream_subprocess_output, 
            args=(input_data, stream_placeholder),
            daemon=True
        )
        streaming_thread.start()
        
        #streaming_thread.join()  # Wait for the thread to finish

        # Retrieve the final output from the thread
        final_result = stream_subprocess_output(input_data, stream_placeholder)
        
        # Save to chat history
        save_chat_history(programming_problem, final_result)
        st.session_state['result_history'].append(final_result)
        st.session_state['problem_history'].append(programming_problem)
        st.write(final_result)

    else:
        st.write("Please provide both Open API key and programming problem.")

# Display previous problems and results
#with st.expander("View Previous Problems and Results"):
#    for problem, result in zip(st.session_state['problem_history'], st.session_state['result_history']):
#        st.write(f"Problem: {problem}")
#        st.write(f"Result: {result}")
#        st.markdown("---")
        
# Display chat history
with st.expander("View Chat History"):
    chat_history = load_chat_history()
    st.text_area("Chat History", chat_history, height=300)
