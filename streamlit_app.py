import streamlit as st
import os
import sys

PROMPT_PREFIX = '''
Info: "With over 100 active members, TUM.ai is Germany's leading AI student initiative, located in Munich. 🎓

Together with our highly talented members, we run projects with industry partners, workshops and so called "Makeathon" product development competitions all around the topic of Artificial Intelligence and Data Analytics. We thrive to deploy AI solutions into new fields and industries! Do not hesitate to reach out to us, we are looking forward to ambitious collaborations. "

User: "What is it?"
Bot: "TUM.ai is a student initiative."
User: "How many active members do you have?"
Bot: "Over 100."
User: "'''

PROMPT_POSTFIX = '''"
Bot: "'''


import requests
import openai

import configparser


# CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
# API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'openaiapirc')



def initialize_openai_api():
    """
    Initialize the OpenAI API
    """

    openai.organization_id = st.secrets['organization_id']
    openai.api_key = st.secrets['secret_key']




st.title('TUM.ai Chatbot')

initialize_openai_api()
user_input = st.text_input("", "")

if not user_input:
    st.stop()

prompt = PROMPT_PREFIX + user_input + PROMPT_POSTFIX

SUFFIX = '''"
User: "Thank you so much, that answered my question!"'''

# MODEL = 'text-davinci-002'
MODEL = 'text-ada-001'

if int(MODEL[-3:]) >= 2:
    suffix = SUFFIX
else:
    suffix = None

response = openai.Completion.create(engine=MODEL, prompt=prompt, suffix=suffix, temperature=0.7, stream=True, stop='User: "', max_tokens=200)

completion_all = ''
response_text_field = st.empty()

while True:
    next_response = next(response)
    print("next_response:", next_response)
    completion = next_response['choices'][0]['text']
    if next_response['choices'][0]['finish_reason']:
        if completion_all[-1] == '"':
            completion_all = completion_all.strip()[:-1]

    completion_all += completion
    print("completion_all:", completion_all)
    # response_text_field.text(completion_all)
    response_text_field.markdown(completion_all)
    if next_response['choices'][0]['finish_reason']:
        break


