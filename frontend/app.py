import streamlit as st
import requests

st.title('DevDocs')

# Define Thread
thread_id = 'thread-1'

# Define session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
# Showing the whole message history before writing the current message
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Input Box
user_input = st.chat_input('Ask a question about your documentation')

if user_input:
    
    # Add the message to session state first
    st.session_state['message_history'].append({'role':'user','content':user_input})
    
    with st.chat_message('user'):
        st.text(user_input)

    # The question goes to backend
    response = requests.post(
        "http://localhost:8000/query",
        json = {'query':user_input,'thread_id':thread_id},
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
        
    else:
        st.error('Something went wrong')