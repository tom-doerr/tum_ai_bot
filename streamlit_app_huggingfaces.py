import streamlit as st

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
import time
# r = requests.post(url='https://hf.space/embed/Narrativaai/GPT-J-6B-Demo/+/api/predict/', json={"data": ["Narrativa is an NLP/NLG company that"]})


 
# API_LINK = 'https://hf.space/embed/Narrativaai/GPT-J-6B-Demo/+/api/predict/'
API_LINK = 'https://hf.space/embed/mrm8488/GPT-J-6B/+/api/predict/'
# API_LINK = 'https://hf.space/embed/BigSalmon/GPTJ/+/api/predict/'

def get_cmpletion(text, attempt=0):
    r = requests.post(url=API_LINK, json={"data": [text]})
    json_response = r.json()
    if 'error' in json_response:
        if attempt == 0:
            print('Encountered error, retrying...', end='', flush=True)
        else:
            print('.', end='', flush=True)
        time.sleep(2**attempt)
        return get_cmpletion(text, attempt=attempt+1)
    print("json_response:", json_response)
    response = json_response['data'][0]
    return response

user_input = st.text_input("Type something:")
prompt = PROMPT_PREFIX + user_input + PROMPT_POSTFIX

answer_box = st.empty()

for i in range(100):
    response = get_cmpletion(prompt)
    # clear screen
    # print('\033c', end='')
    print(response)
    prompt = response
    answer_box.text(responses.replace(PROMPT_PREFIX, ''))




