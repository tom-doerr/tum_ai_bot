import streamlit as st

def apply_design():

    # Design implement changes to the standard streamlit UI/UX
    st.set_page_config(page_title="TUM.ai ChatBot")

    # Design move app further up and remove top padding
    st.markdown('''<style>.css-1wrcr25 {margin-top: -11rem;}</style>''',
        unsafe_allow_html=True)

    # Design change hyperlink href link color
    st.markdown('''<style>.css-1offfwp a {color: #660cf3;}</style>''',
        unsafe_allow_html=True)  # lightmode

    # Design change height of text input fields headers
    st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
        unsafe_allow_html=True)

    # Design change spinner color to primary color
    st.markdown('''<style>.stSpinner > div > div {border-top-color: #660cf3;}</style>''',
        unsafe_allow_html=True)

    # Design change min height of text input box
    st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
        unsafe_allow_html=True)

    # Design hide top header line
    hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Design hide "made with streamlit" footer menu area
    hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                            footer {visibility: hidden;}</style>"""
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)
