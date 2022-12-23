import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import random
from datetime import date, timedelta
from random import choices
import networkx as nx
import pickle as pkl
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import math
import plotly.figure_factory as ff
 

st.set_page_config(page_title="Data Story", page_icon="📰")#, layout="wide")

#values should be a dictionnary : [name,x,y ]
def plot_ply_sp(values,measure):
    num_rows = math.floor(math.sqrt(len(values)))
    num_cols = len(values) // num_rows
    num_cols = num_cols if len(values) % num_rows == 0 else num_cols + 1

    fig = make_subplots(
        rows=num_rows,
        cols=num_cols,
        subplot_titles= [value[0]  for value in values],
        horizontal_spacing=0.15
    )

    for i,  value in enumerate(values):
        row = i // num_cols + 1
        col = i % num_cols + 1
        fig.update_xaxes(title_text="hop number",row=row,col=col,tickfont_size=9,titlefont_size=10)
        fig.update_yaxes(title_text="{} measure".format(measure),row=row,col=col,tickfont_size=9,titlefont_size=10,ticksuffix=" ")
        fig.add_trace(
            go.Scatter(
                x=value[1], 
                y=value[2], 
                mode='lines',
                showlegend=False
            ),
            row=row,
            col=col
        )
    
    fig.update_layout(height=900, width=1200, title_text=u'\xa0'*55+"Evolution of {} measure on shortest path ".format(str(measure)),title_x=0.5)
    fig.update_annotations(font_size=13)

    st.plotly_chart(fig,use_container_width=True)

def plot_distribution(out_degree_nodes) -> None:
    fig = ff.create_distplot([out_degree_nodes], ['out_degree'], bin_size=1)
    fig.update_layout(title_text=u'\xa0'*75+'Distribution of out_degree', title_x=0.5)
    fig.update_xaxes(type="log", range=[0, 3], title_text='out_degree'),
    fig.update_yaxes(title_text='density')

def plot_ply(values,measure):
    num_rows = math.floor(math.sqrt(len(values)))
    num_cols = len(values) // num_rows
    num_cols = num_cols if len(values) % num_rows == 0 else num_cols + 1

    fig = make_subplots(
        rows=num_rows,
        cols=num_cols,
        subplot_titles=["<b>{} to {} <br> ({} games</b>)".format(key[0], key[1], value[4]) for key, value in values.items()],

        horizontal_spacing=0.15
    )

    for i, (key, value) in enumerate(values.items()):
        row = i // num_cols + 1
        col = i % num_cols + 1
        fig.update_xaxes(title_text="path proportion",row=row,col=col,tickfont_size=9,titlefont_size=10)
        fig.update_yaxes(title_text="{} measure".format(measure),row=row,col=col,tickfont_size=9,titlefont_size=10,ticksuffix=" ")
        fig.add_trace(
            go.Scatter(
                x=value[0], 
                y=value[1], 
                mode='lines',
                showlegend=False
            ),
            row=row,
            col=col
        )
        fig.add_trace(
            go.Scatter(
                x=value[0], 
                y=value[2], 
                mode='none', 
                fill='tonexty',
                showlegend=False
            ),
            row=row,
            col=col
        )
        fig.add_trace(
            go.Scatter(
                x=value[0], 
                y=value[3], 
                mode='none', 
                fill='tonexty',
                showlegend=False
            ),
            row=row,
            col=col
        )

    
    fig.update_layout(height=900, width=1200, title_text=u'\xa0'*55+"Evolution of {} measure on shortest path".format(str(measure)),title_x=1)
    fig.update_annotations(font_size=13)
    st.plotly_chart(fig,use_container_width=True)

st.markdown("""
<style>
.big-font {
    font-size:25px !important;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.big-font-left {
    font-size:25px !important;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.title-font-left {
    font-size:35px !important;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.mid-font {
    font-size:20px !important;
    text-align: center;
    color: grey;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.mid-font-black {
    font-size:20px !important;
    text-align: center;
    
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.plot-font-black {
    font-size:15px !important;
    text-align: center;
    
}
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="big-font">The idea behind this study takes its roots in an observation of the behavior of Wikispeedia’s players.\
    While carefully studying some rounds of this game, we noticed a variety of patterns and strategies followed by most players.\
    In light of this, we articulate our story around four main chapters :</p>', unsafe_allow_html=True)
st.write("##")

col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1 :
    st.markdown('<p class="mid-font"><b>1- Can this behavior be generalized?</b></p>', unsafe_allow_html=True)
with col2:
    st.markdown('<p class="mid-font"><b>2- What is the semantic meaning of the players paths?</b></p>', unsafe_allow_html=True)
with col3:
    st.markdown('<p class="mid-font"><b>3- Is there any optimal strategy?</b></p>', unsafe_allow_html=True)
with col4:
    st.markdown('<p class="mid-font"><b>4- Are there any strategies to avoid ?</b></p>', unsafe_allow_html=True)


st.write("##")
st.write("##")
st.markdown("***")
st.write("##")

st.markdown('<p class="title-font-left"><b>Can this behavior be generalized?🤔</b></p>', unsafe_allow_html=True)
st.markdown("##")

st.write("To start our analysis, we needed to understand how the paths are changing. In other words, what makes\
    a player choose his next article. Since almost all articles are connected together, the first thing we did was to compute for every single \
    article from Wikipedia an centrality metric that can be used to distinguish different nodes based on their level of connectivity.\
    For this, we considered different centrality measures such as : Out degree, Betweenness, Closeness & PageRank. We can see from the table below, that all the metrics used match almost perfectly with the actual number of clicks (i.e: visits) on that article.")





###################################### writing ranked metrics here ###############################
st.markdown("#")

col1,col2 = st.columns([0.1,2])
with col2:
    st.markdown("""
    <style type="text/css">
    .tg  {border-collapse:collapse;border-color:#ccc;border-spacing:0;}
    .tg td{background-color:#fff;border-bottom-width:1px;border-color:#ccc;border-style:solid;border-top-width:1px;
    border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;
    word-break:normal;}
    .tg th{background-color:#f0f0f0;border-bottom-width:1px;border-color:#ccc;border-style:solid;border-top-width:1px;
    border-width:0px;color:#333;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;
    padding:10px 5px;word-break:normal;}
    .tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
    .tg .tg-7btt{border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
    .tg .tg-abip{background-color:#f9f9f9;border-color:inherit;text-align:center;vertical-align:top}
    .tg .tg-zwlc{background-color:#f9f9f9;border-color:inherit;font-weight:bold;text-align:center;vertical-align:top}
    </style>
    <table class="tg">
    <thead>
    <tr>
        <th class="tg-c3ow"></th>
        <th class="tg-7btt" colspan="5">Centrality Measures</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td class="tg-abip"></td>
        <td class="tg-zwlc">Visits</td>
        <td class="tg-zwlc">Out Degree</td>
        <td class="tg-zwlc">Closeness</td>
        <td class="tg-zwlc">Pagerank</td>
        <td class="tg-zwlc">Betweenness</td>
    </tr>
    <tr>
        <td class="tg-7btt">Rank 1</td>
        <td class="tg-c3ow">United States</td>
        <td class="tg-c3ow">United States</td>
        <td class="tg-c3ow">United States</td>
        <td class="tg-c3ow">United States</td>
        <td class="tg-c3ow">United States</td>
    </tr>
    <tr>
        <td class="tg-zwlc">Rank 2</td>
        <td class="tg-abip">Europe</td>
        <td class="tg-abip">United Kingdom</td>
        <td class="tg-abip">Europe</td>
        <td class="tg-abip">France</td>
        <td class="tg-abip">United Kingdom</td>
    </tr>
    <tr>
        <td class="tg-7btt">Rank 3</td>
        <td class="tg-c3ow">United Kingdom</td>
        <td class="tg-c3ow">France </td>
        <td class="tg-c3ow">United Kingdom </td>
        <td class="tg-c3ow">Europe</td>
        <td class="tg-c3ow">England</td>
    </tr>
    <tr>
        <td class="tg-zwlc">Rank 4</td>
        <td class="tg-abip">England</td>
        <td class="tg-abip">Europe</td>
        <td class="tg-abip">France</td>
        <td class="tg-abip">United Kingdom</td>
        <td class="tg-abip">Europe</td>
    </tr>
    <tr>
        <td class="tg-7btt">Rank 5</td>
        <td class="tg-c3ow">Earth</td>
        <td class="tg-c3ow">England</td>
        <td class="tg-c3ow">Germany</td>
        <td class="tg-c3ow">English Language</td>
        <td class="tg-c3ow">Africa</td>
    </tr>
    <tr>
        <td class="tg-zwlc">Rank 6</td>
        <td class="tg-abip">Africa</td>
        <td class="tg-abip">World War II</td>
        <td class="tg-abip"><span style="font-weight:400;font-style:normal">World War II</span></td>
        <td class="tg-abip">Germany</td>
        <td class="tg-abip"><span style="font-weight:400;font-style:normal">Germany</span></td>
    </tr>
    </tbody>
    </table>""",unsafe_allow_html=True)

_,col2= st.columns([0.35,1])
with col2:
    st.write('Fig1: Top 6 nodes with highest centrality measures')

st.markdown("#")

st.write("This confirms our intuition about players' strategy and the fact that they have a tendency to visit more central nodes. Continuing our analysis, we still needed to focus on a single centrality measure \
so we chose the one with highest correlation to the number of visits (as well as least error) which was the number of <i>out degrees</i>.",unsafe_allow_html=True)

st.write("#")
st.markdown('<p class="big-font-left"><b>What is the evolution of the centrality of the nodes visited in the players\' path ?</b></p>', unsafe_allow_html=True)
st.write("Now that we have selected our measure, let’s have a deeper look at the evolution of this centrality metric in the players’ paths. \
    Displaying the plots as a matrix yields a global view and helps us showcase underlying patterns, if any.  ")




with open('viz/centrality_evolution.pkl', 'rb') as f:
    evolution_data = pkl.load(f)
st.write("#")

with open('viz/semantic_evolution.pkl', 'rb') as f:
    semantic_evolution = pkl.load(f)

with open('viz/sp_centrality.pkl','rb') as f:
    sp_shortest_path = pkl.load(f)

with open('viz/sp_semantic (1).pkl','rb') as f:
    sp_shortest_path_semantic = pkl.load(f)

with open('viz/out_degree.pkl', 'rb') as f:
    out_degree_nodes = pkl.load(f)


plot_ply(evolution_data,"Out degree")



st.markdown("##")
st.write("This study confirms our intuition about players' strategy.\
    We can clearly observe a recurrent pattern in the evolution of the centrality\
    measure along the path(of course with a couple exceptions) which consists of :")
st.write("* first moving towards central nodes ( seen from centrality going up)")
st.write("* focusing back on the target        ( centrality decreasing )")
st.write("This conclusion draws its statistical significance from the <b> confidence \
    intervals </b> of the curves as each curve was obtained by averaging many paths played. \
    Moreover,<b> 2693 players </b>were involved in this study. Both those arguments make a solid \
    statement that this behaviour is <b>generalisable</b> as we observe a great number of players converging \
    towards the same strategy.",unsafe_allow_html=True)
st.write("However, if we take a step back, we remember that the real goal was to find out good strategies \
    and not only the ones used by players. So how can we be sure that this is a strategy worth following?")
st.write("For this, we can analyse the shortest paths possible and compare the two results since that is \
    the optimal path we want to follow at the end. ")
st.write("So, we should ask ourselves:")
st.markdown("#")
st.markdown('<p class="big-font-left"><b>Is there a similar pattern in the actual shortest paths ?</b></p>', unsafe_allow_html=True)

st.write("Only one way to find out: let’s try to analyse the same plot using the shortest paths.")

plot_ply_sp(sp_shortest_path,"Out degree")

st.write("We observe that the evolution of the centrality of the nodes visited, along the shortest path, follow a similar behavior to the players. \
    This can be explained by properties of real world networks. Degree distribution tends to be skewed, and some nodes effectively act as hubs \
    and allow for very short paths to be found. Moreover, in such networks, short paths are easily discoverable via greedy decentralized routing. ")
st.write("So, to wrap up everything we said so far, the shortest paths, as well as the players paths, both follow the same strategy regarding \
    the centrality of the nodes visited which is something to keep in mind.")

st.write("Moving further with our analysis, an interesting approach for players would be to consider the semantics of every choice they \
    make relative to the current article. So, let’s try to investigate this game plan.")
st.markdown("##")

st.markdown('<p class="title-font-left"><b>What is the semantic meaning of the players\' paths?</b></p>', unsafe_allow_html=True)


st.write("Naturally, one might argue that, as we move forward, we try to get closer semantically to our goal. However, is this something \
    we consider at the very end of the game, when we are very close to the target, or is it requisite to determine the whole path from the start ?")
st.write("To answer this question, we should explore the evolution of semantic closeness, going from one node to another in the player's paths. \
    Similarly to what we did earlier with centrality evolution, let’s have a global look of this evolution in the top 10 paths to see \
    if we can identify a pattern.")


plot_ply(semantic_evolution,"Semantic")

st.markdown("##")
st.write("Just as we have expected, we have a crystal clear evolution of the semantics in all these paths.\
    This means that the players are choosing their next hop based on similar meanings and interpretation.\
    This is actually predictable, since as human beings, that is how our brains work. We try to reason logically\
    about our choices and relate them to either our previous choices, or our next goals.")

st.write("This unveils the full strategy of the players as not only do they tend to go through central nodes, \
    but they also factor in semantic closeness to the target when making their choice.")
st.write("As always, we need to keep asking ourselves whether following this strategy yields the optimal behavior to win the Wikispeedia game, or not. ")

st.markdown("#")
st.markdown('<p class="big-font-left"><b>Do shortest paths reflect semantic closeness/similarity ?</b></p>', unsafe_allow_html=True)
st.write("This naturally brings us again to the comparison with the optimal paths so let’s explore the semantics evolution in the shortest paths.")

plot_ply_sp(sp_shortest_path_semantic,"Semantic")

st.write("From the above plots, we discover an interesting difference from the previous graphs of the players. \
    As a matter of fact, shortest paths do not seem to follow semantic distance all along the path. \
    We can clearly notice an evolution increasing in some graphs, decreasing in others, and even both in a couple of them.")
st.write("This is what keeps the players from reaching the optimal behavior of shortest paths. In fact, it’s counter intuitive \
    for human players to act <b>not in accordance with a specific meaning</b> or interpretation and is actually the opposite of \
    how the brain was trained to operate. At the same time, this is exactly what allows algorithms to find the \
    optimal routing with a global view of the network.",unsafe_allow_html=True)
st.write("To sum up, a human being will never be able to perform according to the perfect strategy, \
    in a consistent way, because of how the brain functions facing semantics.")
st.write("Now that we have unveiled deeper insights about players' behavior and what keeps them from reaching optimality \
    in the Wikispeedia game, we decide to investigate further improvements that can help players get closer to the shortest path.")



plot_distribution(out_degree_nodes)





