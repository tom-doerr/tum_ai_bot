import streamlit as st
import os
import sys
import time
import math

import app_design

# apply design changes
app_design.apply_design()

PROMPT_PREFIX_FOR_ALL = '''
Info: "I am a highly intelligent question answering bot of student initative TUM.ai. I'll answer all questions in regard to the application process and the key aspects of why you should join us. I will answer the questions based on the context below, and if the question can't be answered based on the context, I'll say 'I don't know'.
With over 170 active members, TUM.ai is Germany's leading AI student initiative, located in Munich. 🎓
 "'''

PROMPT_POSTFIX = '''"
Bot: "'''

import requests
import openai

import configparser

# CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
# API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'openaiapirc')

PROMPTS_LOG_CSV = 'propmts.csv'
RESPONSES_LOG_CSV = 'responses.csv'
CHARACTERS_TOKEN_RATIO_ESTIMATE = 4.66
PROMPT_FILE = 'prompt.txt'
with open(PROMPT_FILE, 'r') as f:
    PROMPT_PREFIX = f.read()

if (('log' in st.experimental_get_query_params()) and st.experimental_get_query_params()['log'][0] == 'true'):
    st.title('Showing log')
    try:
        st.write(f'{PROMPTS_LOG_CSV}:')
        with open(PROMPTS_LOG_CSV, 'r') as f:
            st.code(f.read())

        st.write(f'{RESPONSES_LOG_CSV}:')
        with open(RESPONSES_LOG_CSV, 'r') as f:
            st.code(f.read())
    except FileNotFoundError:
        st.write('No log found')


def get_roughly_n_tokens_section(text, n_tokens):
    text_split_empty_lines = text.split('\n\n')
    num_target_chars = n_tokens * CHARACTERS_TOKEN_RATIO_ESTIMATE
    line_num_last_added = 0
    section_texts = []

    while True:
        out_text = ''
        # for i, line in enumerate(text_split_empty_lines[i:]):
        for i in range(line_num_last_added + 1, len(text_split_empty_lines)):
            print("i:", i)
            line = text_split_empty_lines[i]
            if len(out_text) + len(line) > num_target_chars:
                break

            if i >= len(text_split_empty_lines) - 1:
                break

            out_text += line + '\n\n'
            line_num_last_added = i

        section_texts.append(out_text)
        if i >= len(text_split_empty_lines) - 1:
            break

    return section_texts


def write_page_load_stats():
    with open(LOG_FILE_LOAD_STATS, 'a') as f:
        f.write(f'{time.time()}\n')


def log_prompt(prompt):
    with open(PROMPTS_LOG_CSV, 'a') as f:
        f.write(f'{time.time()},{prompt}\n')


def log_response(response):
    with open(RESPONSES_LOG_CSV, 'a') as f:
        f.write(f'{time.time()},{response}\n')


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
    prompts_with_times = [prompt_with_time for prompt_with_time in prompts_with_times if
                          time.time() - float(prompt_with_time[0]) < mins * 60]
    num_prompts = len(prompts_with_times)
    print(f'{num_prompts} prompts in the last {mins} minutes')
    return num_prompts


MINUTES_TO_CONSIDER = 60
MAX_REQUESTS_PER_MINUTE = 12

num_prompts_last_x_min = get_num_prompts_last_x_min(MINUTES_TO_CONSIDER)

print("num_prompts_last_x_min:", num_prompts_last_x_min)
if num_prompts_last_x_min >= MAX_REQUESTS_PER_MINUTE * MINUTES_TO_CONSIDER:
    st.info('Hit the rate limit, please try again in a few minutes.')
    st.stop()


# from dotenv import load_dotenv
# load_dotenv()

def initialize_openai_api():
    """
    Initialize the OpenAI API
    """
    # openai.api_key = os.environ["SECRET_KEY"]
    # openai.organization_id = os.environ["ORGANIZATION_ID"]

    openai.organization_id = st.secrets['organization_id']
    openai.api_key = st.secrets['secret_key']


# added header with question and logprob
# "Hi, how can I help you today? + logo"
st.image('header_logo.png')
st.write("This bot is AI-based, we do NOT guarantee for the correctness of its answers - your TUM.ai DEV Team")

initialize_openai_api()
user_input = st.text_input("Please enter your question here", "")

if not user_input:
    st.stop()

log_prompt(user_input)
print('creating sections ...')
sections = get_roughly_n_tokens_section(PROMPT_PREFIX, 1000)
print('sections created')
print("sections:", sections)

print("user_input:", user_input)

SUFFIX = '''"
User: "Thank you so much, that answered my question!"'''

# MODEL = 'text-davinci-002'
MODEL = 'text-curie-001'

if int(MODEL[-3:]) >= 2:
    suffix = SUFFIX
else:
    suffix = None

with st.spinner('Thinking about possible answers...'):
    responses = []
    columns = st.columns(len(sections))
    for section_num, section in enumerate(sections):
        prompt_prefix = section
        prompt = prompt_prefix + user_input + PROMPT_POSTFIX
        response = openai.Completion.create(engine=MODEL, prompt=prompt, suffix=suffix, temperature=0.35, stream=True,
                                            stop='User: "', max_tokens=250, logprobs=1)

        completion_all = ''
        logprob_values = []

        with columns[section_num]:
            response_text_field = st.empty()
            while True:
                try:
                    next_response = next(response)
                except StopIteration:
                    break
                print("next_response:", next_response)
                completion = next_response['choices'][0]['text']
                logprob_values.append(next_response['choices'][0]['logprobs']['token_logprobs'][0])
                if next_response['choices'][0]['finish_reason']:
                    if completion_all[-1] == '"':
                        completion_all = completion_all.strip()[:-1]

                completion_all += completion
                # print("completion_all:", completion_all)
                # response_text_field.text(completion_all)
                # response_text_field.markdown(completion_all)
                if next_response['choices'][0]['finish_reason']:
                    break

            print("completion_all:", completion_all)
            logprob_avg = sum(logprob_values) / len(logprob_values)
            # st.write(f'Average logprob: {logprob_avg}')
            # st.write(f'Certainty: {math.exp(logprob_avg)}')
            # response_text_field.markdown(completion_all + f'\n\nCertainty: {math.exp(logprob_avg)}')
            responses.append({'completion': completion_all, 'logprob_avg': logprob_avg})

        log_response(completion_all)
max_response = max(responses, key=lambda x: x['logprob_avg'])
certainty = round(math.exp(max_response["logprob_avg"]) * 100, 4)
print(max_response['completion'] + f'\n\nCertainty: {math.exp(max_response["logprob_avg"])}')
st.markdown(max_response['completion'] + f'\n\n_Certainty: {certainty}%_')
