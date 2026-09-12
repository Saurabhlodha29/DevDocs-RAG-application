import requests
import streamlit as st
from uuid import uuid4


# ----------------------------------------
# 1.Utility Functions 
# ----------------------------------------

# Generate new thread
def generate_thread_id():
    thread_id = uuid4()
    return thread_id

# Create a new chat
def reset_chat():
    thread_id = generate_thread_id()
    
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []
    
# Add the new thread to session state
def add_thread(thread_id):
    if thread_id not in st.session_state['conversations']:
        st.session_state['conversations'].append(thread_id)
    
# Load the older conversation
def load_conversation(thread_id):
    
    response = requests.get(
        f"http://localhost:8000/conversation/{thread_id}"
    )
    
    if response.status_code != 200:
        return []
    
    return response.json()['messages']

# Load all the conversations for sidebar display
def load_conversations():
    
    response = requests.get(
        "http://localhost:8000/conversations"
    )
    
    if response.status_code != 200:
        return []
    
    return response.json()['conversations']

# ----------------------------------------
# 2.Session Setup 
# ----------------------------------------

# Define session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
if 'conversations' not in st.session_state:
    st.session_state['conversations'] = load_conversations()


# ----------------------------------------
# 3.Sidebar UI 
# ----------------------------------------

st.sidebar.title('DevDocs')

st.sidebar.header('My Conversations')

if st.sidebar.button('New Chat'):
    reset_chat()
    
for conversation in st.session_state['conversations']:
    
    thread_id = conversation['thread_id']
    title = conversation['title']
    
    if st.sidebar.button(title):
        
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        temp_messages = []
        
        for message in messages:
            
            if message['type'] == 'human':
                role = 'user'
            else:
                role = 'assistant'
            
            temp_messages.append({
                'role' : role,
                'content' : message['content']
            })
            
        st.session_state['message_history'] = temp_messages
        
        st.rerun()


# ----------------------------------------
# 4.Main UI 
# ----------------------------------------


# Showing the whole message history before writing the current message
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Input Box
user_input = st.chat_input('Ask a question about your documentation')

if user_input:
    
    # Add the message to session state first
    st.session_state['message_history'].append({'role':'user','content':user_input})
    
    # Config
    CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}
    
    with st.chat_message('user'):
        st.text(user_input)

    # The question goes to backend
    response = requests.post(
        "http://localhost:8000/query",
        json = {'query':user_input,'thread_id':str(CONFIG['configurable']['thread_id'])},
        stream = True
    )
    
    # Showing the LLM response
    if response.status_code == 200:
        ai_message = st.write_stream(
            response.iter_content(
                chunk_size = None,
                decode_unicode = True
            )
        )
        
        # Add AIMessage to message history
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})
        
        # Load the title of the current chat
        st.session_state['conversations'] = load_conversations()
        
        # Streamlit needs to rerun the script for the sidebar to be rebuilt using the newly loaded conversations
        st.rerun()
        
    else:
        st.error('Something went wrong')