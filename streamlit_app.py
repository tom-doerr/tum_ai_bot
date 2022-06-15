import streamlit as st
import os
import sys
import time

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



PROMPTS_LOG_CSV = 'propmts.csv'

def write_page_load_stats():
    with open(LOG_FILE_LOAD_STATS, 'a') as f:
        f.write(f'{time.time()}\n')


def log_prompt(prompt):
    with open(PROMPTS_LOG_CSV, 'a') as f:
        f.write(f'{time.time()},{prompt}\n')


def load_prompts_with_times():
    if not os.path.isfile(PROMPTS_LOG_CSV):
        return []
    with open(PROMPTS_LOG_CSV, 'r') as f:
        lines = f.readlines()

    lines = [line.strip().split(',') for line in lines]
    lines = [line for line in lines if len(line) == 2]
    lines = [line for line in lines if line[1] != '']
    lines = [line for line in lines if line[0] != '']

    return lines


def get_num_prompts_last_x_min(mins):
    prompts_with_times = load_prompts_with_times()
    prompts_with_times = [prompt_with_time for prompt_with_time in prompts_with_times if time.time() - float(prompt_with_time[0]) < mins * 60]
    num_prompts = len(prompts_with_times)
    print(f'{num_prompts} prompts in the last {mins} minutes')
    return num_prompts



MINUTES_TO_CONSIDER = 10
MAX_REQUESTS_PER_MINUTE = 2

num_prompts_last_x_min = get_num_prompts_last_x_min(MINUTES_TO_CONSIDER)

print("num_prompts_last_x_min:", num_prompts_last_x_min)
if num_prompts_last_x_min >= MAX_REQUESTS_PER_MINUTE:
    st.info('Hit the rate limit, please try again in a few minutes.')
    st.stop()







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

log_prompt(user_input)

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


