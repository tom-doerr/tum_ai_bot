import streamlit as st
import os
import sys
import time

PROMPT_PREFIX = '''
Info: "With over 100 active members, TUM.ai is Germany's leading AI student initiative, located in Munich. 🎓
Together with our highly talented members, we run projects with industry partners, workshops and so called "Makeathon" product development competitions all around the topic of Artificial Intelligence and Data Analytics. We thrive to deploy AI solutions into new fields and industries! Do not hesitate to reach out to us, we are looking forward to ambitious collaborations. All information is in https://www.tum-ai.com"

User: "What is it?"
Bot: "TUM.ai is a student initiative located in Munich."
User: "What is amazing about TUM.ai?"
Bot: "A great diverse Community of inspiring people. You can learn from each other. You can drive and develop the AI ecosystem. Network with Members, Partners, Alumni, industry leaders and other initiatives. Get out as much as you give into it."
User: "What we expect from you as a TUM.ai Member?"
Bot: "Passion for AI. Motivation to push our initiative forward. To be available and react on topics within a short timeframe. To invest a time of at least 6h per week for the initiative and its projects. To be committed. You should be Munich-based to attend in-person meetings and events."
User: "What should I know about TUM.ai?"
Bot: "We are not an educational program. That means you are not only joining to learn, but also to contribute to the development of the organization. We don’t give in-depth lectures or crash courses in AI and coding yet - to learn things you need to interact with other members. Help is always given to those who ask. We do a lot of organizational work - the AI ecosystem is not ready and you will be part of building it up. We expect you to work min. 6h per week for the initiative and its projects, for your personal involvement and learning you need to spend time on top."
User: "Why should I join TUM.ai?"
Bot: "You should join TUM.ai if you are passionate about AI and want to contribute to the development of the organization. You should also join TUM.ai when you want to learn from other members and be a part of a great diverse community."
User: "Which departments do you have?"
Bot: "TUM.ai is student initiative in form of a non-profit organization with AI focus. We are structured into departments. We have 2 kinds of departments, the mission-based and the functional departments. The mission-based departments focus their work on realizing out mission. The functional departments provide resources for them. Check out the details about each department! Our departments are Software development, Marketing, Finance & Legal, Community, Partners & Sponsors, Makeathon, Venture, Industry, Education."
User: "How much time should I invest?"
Bot: "We expect you to work min. 6h per week for the initiative and its projects."
User: "Who is the president of TUM.ai?"
Bot:: "TUM.ai is currently lead by 3 co-presidents: Luca, Leonie,  Toaha."
User: "What is the mission of TUM.ai?"
Bot: "TUM.ai connects students and all relevant stakeholders to facilitate the application of AI across domains to drive positive societal impact through interdisciplinary projects.Bring together companies and students through projects and events about AI. Offer students practical experience through projects with peers from the group. Learn more about AI by exchanging with peers and companies, conducting workshops and research. We aim at lowering the entry-bar to AI-creation and -usage for people of every domain by establishing a platform to make practical experience through a diverse set of applied AI projects. We therefore educate and connect students from diverse backgrounds to incentivize new interdisciplinary AI projects and push the creation and usage of applicable and safe AI in all domains."
User: "Where do I get more information?"
Bot: "Slack, Instagram (tum.ai_official), and Linkedin."
User: "How many members does TUM.ai have?"
Bot: "TUM.ai currently has about more than 100 members."
User: "How can I participate in Makeathon?
Bot: "TUM.ai Makeathon is a two-day event where teams of four work on challenges provided by partner companies and develop MVP applications, as well as corresponding business concepts and pitches. If you want to participate, you can apply here: https://join-us.tum-ai.com/makeathon/"
User: "How can I get more information about a department?"
Bot: "You can visit our website (https://join-us.tum-ai.com/) to find more information about the departments."
User: "What are TUM.ai events about?"
Bot: "During the semester we partner with selected companies to form symbiotic relationships where our talented students work on real industry projects and provide consulting to push AI  solutions into new domains.  TUM.ai regularly hosts speaker events where our ambitious members, as well as interested followers, get the chance to learn from professional AI engineers, business specialists and various domain experts. At the beginning of every semester, we organize an AI Makeathon. In teams of four, participants work on challenges provided by partner companies and develop MVP  applications, as well as corresponding business concepts and pitches."
User: "What are the values of TUM.ai?"
Bot: "TUM.ai connects students and all relevant stakeholders to facilitate the application of AI across domains to drive positive social impact through interdisciplinary projects. Love for Education: We continuously strive to learn more and stay up to date with the latest trends and technologies surrounding AI. We embrace our diversity and collaborate together in cross-functional settings to exchange and acquire information in order to have a profound role in unfolding AI’s fullest potential in every domain. Trust and Transparency: We enable everyone to voice their opinions and invite open communication. We aim to support one another and work in harmony together as a whole to reach our goals. As a community, we respect and trust one another, knowing we can rely on each other's honesty. Offer students practical experience through projects with peers from the group. Action and Ambition: Setting objectives and moving forward is vital for us in everything we do. We continuously aim to improve and set the bar a little higher each time. We feel responsible and accountable for the delivery of an outcome, even when others are involved and have different roles to fulfill. Diversity and Inclusiveness: Our club consists of students from 20+ various majors who come from different parts of the world. We recognize and embrace the power of collaborative teams consisting of unique individuals which help us foster better decision making and the stimulation of new ideas."

User: "'''

PROMPT_POSTFIX = '''"
Bot: "'''

#The following involves lots of questions about TUM.ai, we should definitely check the content of this following text and above
#
# Q: How much does it cost to be a member of TUM.ai?
# A: We have a membership fee of €2/month (24€ per year) for everyone.
#
# Q: Should I join the Venture or the Industry department?
# A: If you want to join a department that is mainly focused on bridging the gap between idea and building the next successful venture, you should join the Venture department. They are responsible for providing help in entrepreneurial activities for all members. If you want to join a department that is responsible for finding and developing relationships with industry partners and kick-off great industry phases, then you should join the Industry department.
#
# Q:  What about the Marketing department?
# A: The Marketing department is about promoting the vision and mission of TUM.ai, serve as the face of our community as well as coordinating and producing all materials representing TUM.ai. Additionally, we reach out to the community, customers, and aspiring members while creating an overarching image that represents our initiative in a professional way. This is all done with the help of our brand new and exciting corporate identity as well with a really nice team spirit! Our duties are maintaining and managing our social media channels, as well as working closely with our internal designers to create new and thrilling content within the context of AI and to make it available for all different kinds of people from all around the world.
#
# Q: What skills are required for joining the marketing department?
# A: For joining the marketing department, you should be interested in design, social media, and writing. Additionally, it is helpful if you are familiar with AI and have some basic knowledge about Photoshop, Illustrator, and InDesign. However, these skills are not required, as we are always willing to teach you everything you need to know!
#
# Q:  What about the Finance and Legal department?
# A: The Finance & Legal department aims to support all departments of TUM.ai with legal and financial issues. Among others, this includes financial planning and accounting, ensuring TUM.ai’s non-profit status, data protection, contracts/invoices for partnerships, communication with all legal stakeholders and answering the inquiries of the other departments. In the last year, we successfully implemented all finance-related processes and were able to provide the final annual statement for 2021. We aim to increase the legal knowledge so our department can act more independently from our lawyers and tax consultants.
#
# Q: What skills are required for joining the  Finance and Legal department?
# A: We are looking for law and accounting students or people with a high interest and knowledge in legal and accounting matters. Profound German language skills are a big plus, since most of the available resources are in German only.
#
# Q: What is an example event that TUM.ai held in the past?
# A: TUM.ai meets Early Bird VC (Uni-X): Recently, Earlybird raised their first UNI-X fund which is specialized in university spinoffs. The experienced VC  investors Michael Schmitt and Michael Hoeck joined us for an online workshop covering Earlybird's latest investment hypotheses in tech, their experience with AI startup teams, and which ideas they would love to see built by TUM.ai members in the future. It was on March 2022.
#
# Q: What about industry projects?
# A: Do you want to put your AI skills to the test in real industry projects with high impact and at the same time make valuable contacts, get to know potential employers and earn some extra money? Then the Industry projects of TUM.ai are exactly the right opportunity for you! For our upcoming industry phase, starting on April 04, we are collaborating with four partners who have prepared exciting challenges.

# Q: How can I participate in the Makeathon department?
# A: You have to apply to TUM.ai in the next application phase (around October/April) to become a member of the Makeathon department.
#
# Q: What about Education department?
# A: The education department’s goal is to equip everyone with the AI knowledge to pro-actively contribute in an AI project (e.g E-Labs or Industry Phase). To do this we are preparing an overview of state of the art applications and models of deep learning in NLP, Speech and CV. We reference to learning resources where interested participants can learn more about these advanced topics. The paper reading circle is one option for interested members to learn about current development in the field of AI. Our current focus is the TUM.ai School that should take place the first time around the end of May. We are planning interactive technical workshops to introduce basic machine learning concepts via computational notebooks where participants can code along an example. The goal is to demonstrate how easy it is to start developing “AI” using existing libraries and algorithms. The second goal is introduce members to the AI-value-chain and how this technology is currently used to drive business impact. We partner with industry experts to provide real world examples of developing an AI-infused product.
#
# Q: What about the Community department?
# A: The Community department is responsible for enhancing the community spirit within TUM.ai and keeping our members happy. We are organizing and hosting fun community events, like the Christmas party, the Stammtisch, bowling sessions, or the Get-Active Day. Thereby, we want to connect the TUM.ai members with each other. Since last semester, this also spans beyond TUM.ai as we are now part of the Entreprenow network, which gives us the chance to also interact more with other student initiatives in Munich. Also, we are aiming at getting the best people onboard TUM.ai during each semester's recruiting phase. In the upcoming time, we would like to refine the onboarding process for our new joiners to make them feel connected to the community after their first month with TUM.ai.
#
# Q: What about the Partners and Sponsors department?
# A: The Partners & Sponsors department stablishes partnerships with companies, other initiatives and institutions that create the basis for educating and inspiring our members and provide project opportunities. We are the first touchpoint of companies that want to cooperate with TUM.ai and convert them as partners. We have established collaborations with many well known companies from different sectors and have implemented a strong partner sourcing force for our signature projects and the other departments.
#
# Q: What about the Makeathon department?
# A: The Makeathon department aims to organise the Makeathon, a 48-hour challenge where participants from all backgrounds work on a real-world business cases involving AI. Our goal is to raise awareness about possible AI applications, provide AI access and knowledge to non-techies and create the starting point for AI startups. Participants work in interdisciplinary teams and have a chance to show their expertise in AI, business modelling or specific domain, but also to learn from workshops and business talks held by industry and research partners. Every team gets exclusive access to the most powerful AI models. Assistance is provided from mentors and industry experts.
#
# Q: What about the Industry department?
# A: The Industry department is focusing on connecting motivated students with experience in ML/AI fields with companies who are seeking to introduce ML/AI solutions to their ongoing products. This is achieved during our Industry Phase, a biannual 10-week program with teams of 4 to 5 participants taking on partner challenges within different fields of application. During the Industry Phase, we conduct different expert lectures, social events, milestone meetings and pitch days.
#
# Q: What about the Venture department?
# A: The Venture department is mainly focused on bridging the gap between idea and building the next successful venture. We are responsible for providing help in entrepreneurial activities for all members. Our main project is to build the AI Entrepreneurship Lab, the first AI accelerator program for Students. After building the concept in the last months, we are no going full steam ahead to bring the vision to life.
#
# Q: Which partners do you have?
# A: We have partnerships with companies, other initiatives and institutions that create the basis for educating and inspiring our members and provide project opportunities. We have established collaborations with many well known companies (e.g. AppliedAI, Google, Microsoft ...) from different sectors and have implemented a strong partner sourcing force for our signature projects and the other departments.
#
# Started to shorthen the prompt texts of the departments:
# User: "What about the Marketing department?"
# Bot: "The Marketing department is about promoting the vision and mission of TUM.ai, serve as the face of our community as well as coordinating and producing all materials representing TUM.ai. Additionally, we reach out to the community, customers, and aspiring members while creating an overarching image that represents our initiative professionally."
# User: "What about the Finance and Legal department?"
# Bot: "The Finance & Legal department aims to support all departments of TUM.ai with legal and financial issues. Among others, this includes financial planning and accounting, ensuring TUM.ai’s non-profit status, data protection, contracts/invoices for partnerships, communication with all legal stakeholders and answering the inquiries of the other departments."
# User: "What about the Education department?"
# Bot: "The education department’s goal is to equip everyone with the AI knowledge to pro-actively contribute in an AI project (e.g E-Labs or Industry Phase). To do this we are preparing an overview of state of the art applications and models of deep learning in NLP, Speech and CV."

import requests
import openai

import configparser


# CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
# API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'openaiapirc')

PROMPTS_LOG_CSV = 'propmts.csv'
RESPONSES_LOG_CSV = 'responses.csv'

if (('log' in st.experimental_get_query_params())  and st.experimental_get_query_params()['log'][0] == 'true'):
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
    prompts_with_times = [prompt_with_time for prompt_with_time in prompts_with_times if time.time() - float(prompt_with_time[0]) < mins * 60]
    num_prompts = len(prompts_with_times)
    print(f'{num_prompts} prompts in the last {mins} minutes')
    return num_prompts



MINUTES_TO_CONSIDER = 10
MAX_REQUESTS_PER_MINUTE = 5

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
print("user_input:", user_input)

SUFFIX = '''"
User: "Thank you so much, that answered my question!"'''

# MODEL = 'text-davinci-002'
MODEL = 'text-curie-001'

if int(MODEL[-3:]) >= 2:
    suffix = SUFFIX
else:
    suffix = None

response = openai.Completion.create(engine=MODEL, prompt=prompt, suffix=suffix, temperature=0.5, stream=True, stop='User: "', max_tokens=250)

completion_all = ''
response_text_field = st.empty()

while True:
    next_response = next(response)
    completion = next_response['choices'][0]['text']
    if next_response['choices'][0]['finish_reason']:
        if completion_all[-1] == '"':
            completion_all = completion_all.strip()[:-1]

    completion_all += completion
    # print("completion_all:", completion_all)
    # response_text_field.text(completion_all)
    response_text_field.markdown(completion_all)
    if next_response['choices'][0]['finish_reason']:
        break

print("completion_all:", completion_all)

log_response(completion_all)


