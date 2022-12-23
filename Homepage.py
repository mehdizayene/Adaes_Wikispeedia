import random
import time
from random import sample
import wikipedia
import networkx as nx
import pandas as pd
import streamlit as st
from PIL import Image
import time
import numpy as np
import pickle as pkl
import requests
import nltk
nltk.download('punkt')
random.seed(200)

# Function to fetch summary from Wikipedia API
def get_summary(title, num_sentences=4): 
    # Fetch summary from Wikipedia API
    params = {
        'format': 'json',
        'action': 'query',
        'prop': 'extracts',
        'exintro': '',
        'explaintext': '',
        'titles': title,
        'redirects': 1,
        'formatversion': 2
    }
    api_url = 'https://en.wikipedia.org/w/api.php'
    response = requests.get(api_url, params=params).json()
    pages = response['query']['pages']
    page = pages[0]
    try:
        summary = page['extract']
    except:
        summary = 'No summary available'
        return summary

    # Tokenize summary into sentences
    sentences = nltk.sent_tokenize(summary)

    # Select first num_sentences sentences
    summary = ' '.join(sentences[:num_sentences])
    
    return summary

def reset_counter():
    st.session_state["num_steps"] = 1
    st.session_state["won"] = False
    st.session_state["abandoned"] = False


# Find to which percent of times your time belongs to
def get_percent(times, your_time):
    times = np.append(times, your_time)
    # Sort times in ascending order
    sorted_times = sorted(times)
    # Find index of your time in sorted array
    index = sorted_times.index(your_time)
    # Calculate percent of times that you belong to
    percent = (index + 1) / len(times) * 100
    return np.ceil(percent)


def increment_counter():
    if "num_steps" not in st.session_state:
        reset_counter()
    st.session_state["num_steps"] += 1


st.set_page_config(
    page_title="AdaEs Wikispeedia App", page_icon="📰"
)  # , layout="wide")
title_image = Image.open("viz/wikispeedia.png")

st.markdown(
    "<h1 style='text-align: center; color: grey;'>The untold truth behind Wikispeedia  👨‍💻️</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<h2 style='text-align: center; color: grey;'>AdaEs Team </h2>",
    unsafe_allow_html=True,
)
col1, col2, col3 = st.columns([1.8, 2, 1])
with col2:
    st.image(title_image)
st.write("##")
st.markdown(
    """
<style>
.big-font {
    font-size:25px !important;
    text-align: center;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
.big-font-left {
    font-size:25px !important;
    text-align: left;
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<style>
.mid-font {
    font-size:20px !important;
    text-align: center;
    color: grey;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
.mid-font-black {
    font-size:20px !important;
    text-align: center;
    
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="big-font"><b>Wikispeedia</b> is a game based on Wikipedia, where you are given a start and end article and they must\
    reach their goal in the fastest time possible only by using Wikipedia hyperlinks.\
    This study aims at analyzing players strategies in order to leverage out insightful conclusions about their navigational behavior.</p>',
    unsafe_allow_html=True,
)


st.write("##")
st.write("##")
st.write("##")

st.markdown("***")

col1, col2, col3 = st.columns([1.1, 1, 1])
with col2:
    st.markdown(
        '<p class="big-font"><b>Dataset Metrics :</b></p>', unsafe_allow_html=True
    )

col0, col1, col2, col3 = st.columns([0.6, 1, 1, 1])
col1.metric("Games Played", "28 713 ")
col2.metric("Users Failed", "3635 ", "12.7 %", delta_color="inverse")
col3.metric("Articles", "4600 ")

st.markdown("***")

st.write("##")

st.markdown(
    '<p class="big-font"><b>Do you think you can do better ?</b></p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="big-font"><b>Try out the game if you are confident enough 😜</b></p>',
    unsafe_allow_html=True,
)

st.write("##")

################### game here ###################

slate = st.empty()
body = slate.container()
with body:
    col1, col2, col3 = st.columns([1.3, 1, 1])
    with col2:
        start_button = st.button(
            "Start the game!",
            on_click=reset_counter,
        )

#################################################
st.write("##")
st.write("##")
st.write("##")


###################################### finished ranked metrics here ###############################


@st.experimental_singleton(show_spinner=False)
def import_graph_articles():
    with st.spinner("Loading dataset ..."):
        return nx.read_gpickle("data/G_articles.gpickle")


@st.experimental_singleton(show_spinner=False)
def import_time():
    with st.spinner("Loading players time ..."):
        with open("viz/times.pkl", "rb") as f:
            players_time = pkl.load(f)
            return players_time


def set_current_node(node, target_node):
    slate.empty()
    st.session_state["current_node"] = node
    st.session_state["target_node"] = target_node
    increment_counter()
    if node == target_node:
        st.session_state["end_game"] = True
    st.experimental_rerun()


def play_round(G_articles, current_node, target_node):

    col1, col2, col3 = st.columns([1.4, 1, 1])
    hint=""
    try :
        hint = str(nx.shortest_path(G_articles,current_node,target_node)[1])
    except :
        hint = "seems like there is no path to the target, Start the game again !"
    with col1:
        st.write(f"**Current aritcle:** {current_node}")
        st.write(f"**Target article:** {target_node}")
    with col2:
        st.write(f"**Nodes count :** {st.session_state.get('num_steps', 0)}")
    
    with col3:
        with st.expander("Get Hint !"):
            hint
    st.write("#")
    st.markdown("***")
    st.write("<b>Snippet article : </b>" + get_summary(current_node),unsafe_allow_html=True)
    neighbors = list(G_articles.neighbors(current_node))

    with st.form("form"):
        selection = st.radio("Selection", neighbors, horizontal=True)
        col1, col2, col3 = st.columns([3.1, 3, 1])

        with col2:
            submit_form = st.form_submit_button("Submit")

        if submit_form and not st.session_state["abandoned"]:
            if not st.session_state["end_game"]:

                print(f"Setting current node to {selection} ...")
                set_current_node(selection, target_node)
                print(f"-> {st.session_state.get('current_node', None)}")
        with col3:
            st.form_submit_button("Abandon")

    return (
        st.session_state.get("current_node", None),
        st.session_state.get("target_node", None),
    )


def run():

    G_articles = import_graph_articles()
    players_time = import_time()
    with body:

        if start_button:
            # rand_idx = random.randrange(len(list_of_nodes))
            current_node = "Asteroid"  # list_of_nodes[rand_idx]
            target_node = "Viking"
            st.session_state["current_node"] = current_node
            st.session_state["target_node"] = target_node
            st.session_state["end_game"] = False
            st.session_state["start_date"] = time.time()
        if "current_node" in st.session_state:
            (source, target) = play_round(
                G_articles,
                st.session_state["current_node"],
                st.session_state["target_node"],
            )
            if source == target:

                diff_nodes = st.session_state["num_steps"] - 4
                fail_str = "Could do better"
                win_str = "Impressive !"
                st.session_state["time_spent"] = (
                    round(time.time() - st.session_state["start_date"], 1)
                    if not st.session_state["won"]
                    else st.session_state["time_spent"]
                )
                st.session_state["won"] = True
                time_ranking = get_percent(players_time, st.session_state["time_spent"])
                time_well = True if time_ranking < 50 else False
                st.markdown(
                    '<p class="big-font"><b>Yeaaaah well done ! 🏆</b></p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<p class="big-font"><b>Here are some statistics about your game 📊: </b></p>',
                    unsafe_allow_html=True,
                )
                col0, col1, col2, col3 = st.columns([0.7, 1, 1, 1])
                col1.metric("Number of hops", st.session_state["num_steps"])
                col2.metric(
                    "\xa0 \xa0 \xa0 \xa0 Time",
                    str(st.session_state["time_spent"]) + " s",
                    "Top " + str(time_ranking) + " %",
                    delta_color="normal" if time_well else "inverse",
                )
                col3.metric(
                    "Difference with shortest path",
                    " \xa0 \xa0 \xa0 \xa0 \xa0" + str(diff_nodes),
                    " \xa0 \xa0 \xa0 \xa0 \xa0"
                    + (fail_str if diff_nodes != 0 else win_str),
                    delta_color="inverse" if diff_nodes != 0 else "normal",
                )
                st.markdown("***")
            elif st.session_state["FormSubmitter:form-Abandon"] or st.session_state["abandoned"]:
                st.session_state["abandoned"] = True
                st.markdown(
                    '<p class="big-font"><b>Well... Don\'t give up yet ! 💪</b></p>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<p class="big-font"><b>Read our data story and learn more about the untold truths about Wikispeedia 🤓</b></p>',
                    unsafe_allow_html=True,
                )

    print(f"Now on {st.session_state.get('current_node', None)}")


run()
