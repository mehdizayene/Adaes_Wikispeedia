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
from PIL import Image
 

st.set_page_config(page_title="Data Story", page_icon="📰")#, layout="wide")


st.markdown(
    "<h1 style='text-align: center; color: grey;'>The untold truth behind Wikispeedia  👨‍💻️</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<h2 style='text-align: center; color: grey;'>AdaEs Team </h2>",
    unsafe_allow_html=True,
)
title_image = Image.open("viz/wikispeedia.png")
col1, col2, col3 = st.columns([1.8, 2, 1])
with col2:
    st.image(title_image)
st.write("##")


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
        subplot_titles=["<b>{} to {} <br> ({} games)</b>".format(key[0], key[1], value[4]) for key, value in values.items()],

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

    
    fig.update_layout(height=900, width=1200, title_text=u'\xa0'*55+"Evolution of {} measure on players path".format(str(measure)),title_x=1)
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
.title-font {
    font-size:35px !important;
    text-align: center;
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
    In light of this, we articulate our story around three main chapters :</p>', unsafe_allow_html=True)
st.write("##")

col1, col2, col3 = st.columns([1,1,1])
with col1 :
    st.markdown('<p class="mid-font"><b>1- Can this behavior be generalized?</b></p>', unsafe_allow_html=True)
with col2:
    st.markdown('<p class="mid-font"><b>2- What is the semantic meaning of the played games paths?</b></p>', unsafe_allow_html=True)
with col3:
    st.markdown('<p class="mid-font"><b>3- Are there any strategies to avoid ?</b></p>', unsafe_allow_html=True)


st.write("##")
st.write("##")
st.markdown("***")
st.write("##")

st.markdown('<p class="title-font-left"><b>1. Can this behavior be generalized?🤔</b></p>', unsafe_allow_html=True)
st.markdown("##")

st.write("To start our analysis, we needed to understand how the paths are changing. In other words, what makes a player <b>choose</b> his next article.",unsafe_allow_html=True)
st.write("Since almost all articles are connected together, the first thing we did was to compute, for every single article from Wikipedia, a centrality \
    metric that can be used to distinguish different nodes based on their level of connectivity.")
st.write("For this, we considered different centrality measures such as : Out-degree centrality, Closeness, PageRank and Betweness.")



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

st.write("We can see from the table above (figure 1), that all the metrics used correlate with the actual number of clicks (i.e: visits) on that article.\
    For example, “United States” is the top 1 node based on whatever measure we choose. The rest is ordered slightly differently without affecting \
    the overall correlation.")

st.write("This confirms our intuition about players' strategy and the fact that they have a tendency to visit more central nodes.\
    Continuing our analysis, for simplicity reasons we still needed to focus on a single centrality measure.\
    For this matter, we computed the 3 following error distances from centrality measure to number of visits : Wasserstein distance, mean squared error & mean absolute error.\
    Finally, we chose the one that minimises these distances which was the <i>outdegree</i> measure." , unsafe_allow_html = True)

st.write("#")
st.markdown('<p class="big-font-left"><b>What is the evolution of the centrality of the nodes visited in the players\' path ?</b></p>', unsafe_allow_html=True)

st.write("Now that we have selected our measure, let’s have a deeper look at the evolution of this centrality metric in the players’ paths.\
    To further simplify the analysis without losing relevant insights, we decided to work on the top 12 games that were played the most, since they \
    best represent the overall behavior of players.") 


st.write("It’s worth mentioning that we only consider the winners paths since our goal is to predict a successful strategy.\
    Moreover, games do not have the same number of hops so it would not be possible to display the centrality evolution hop by hop but an overall average path \
    progression from 0-1 is rather preferred. So, we computed the average on this range along with the confidence intervals from the different games.")

st.write("Displaying the plots as a matrix yields a global view and helps us showcase underlying patterns, if any.")

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

with open('viz/unfinished_evolution.pkl', 'rb') as f:
    unfinished_evolution = pkl.load(f)


plot_ply(evolution_data,"Out degree")



st.markdown("##")
st.write("This study confirms our intuition about players' strategy.\
    We can clearly observe a recurrent pattern in the evolution of the centrality\
    measure along the path(of course with a couple exceptions) which consists of :")
st.write("* first moving towards central nodes ( seen from centrality going up)")
st.write("* focusing back on the target        ( centrality decreasing )")
st.write("This conclusion draws its statistical significance from the <b> confidence \
    intervals </b> of the curves as each curve was obtained by averaging many paths played. \
    Moreover,<b> 2736 players </b>were involved in this study. Both those arguments make a solid \
    statement that this behaviour is <b>generalisable</b> as we observe a great number of players converging \
    towards the same strategy.",unsafe_allow_html=True)

st.write("It’s important to note at this level that the final strategy that we will uncover relates to random paths \
    and not ones that have a high centrality target. Indeed and as it is often the case in real world networks, \
    outdegree distribution over the nodes tends to be skewed. As this fact is of high interest to our analysis, \
    we decided to visualise it.")

plot_distribution(out_degree_nodes)


st.write("If we take a step back, we remember that the real goal was to find out good strategies \
    and not only the ones used by players. So how can we be sure that this is a strategy worth following?")
st.write("For this, we can analyse the shortest paths possible and compare the two results since that is \
    the optimal path we want to follow at the end. ")
st.markdown("#")
st.markdown('<p class="big-font-left"><b>Is there a similar pattern in the actual shortest paths ?</b></p>', unsafe_allow_html=True)

st.write("Only one way to find out: let’s try to analyse the same plot using the shortest paths.")

plot_ply_sp(sp_shortest_path,"Out degree")

st.write("We observe that the evolution of the centrality of the nodes visited, along the shortest path, follow a similar behavior to the players. \
    This can be explained by properties of real world networks. Degree distribution tends to be skewed, and some nodes effectively act as hubs and \
    allow for very short paths to be found. Moreover, in such networks, short paths are easily discoverable via greedy decentralized routing.")


st.write("So, to wrap up everything we said so far, the shortest paths, as well as the players paths, both follow the same strategy regarding the \
    centrality of the nodes visited which is something to keep in mind.")

st.write("Moving further with our analysis, an interesting approach for players would be to consider the semantics of every choice they make\
    relative to the current article. So, let’s try to investigate this game plan.")

st.markdown("#")
st.markdown("***")
st.markdown("#")
st.markdown('<p class="title-font-left"><b>2. What is the semantic meaning of the played games paths?</b></p>', unsafe_allow_html=True)


st.write("Naturally, one might argue that, as we move forward, we try to get closer semantically to our goal. However, is this something \
    we consider at the very end of the game, when we are very close to the target, or is it requisite to determine the whole path from the start ?")

st.markdown('<p class="big-font-left"><b>What is the semantic meaning of the players\' paths?</b></p>', unsafe_allow_html=True)


st.write("To answer this question, we should explore the <b>evolution of semantic closeness</b>, along the path to the target article. ",unsafe_allow_html=True)

st.write("To do so, we take advantage of a <b>pre-trained sBERT model</b> that we use to embed our 4604 articles. \
    The embeddings have been done at the <b>document level</b> (up to 512 tokens). Semantic similarity between \
    articles (between each article and the target) has now become possible by computing <b>cosine similarities</b> between the corresponding embedded vectors.",unsafe_allow_html=True)

st.write("Similarly to what we did earlier with centrality evolution, let’s have a global look of this evolution in the top 10 paths to see \
    if we can identify a pattern.")
st.write("")
plot_ply(semantic_evolution,"Semantic")

st.markdown("##")
st.write("Just as we have expected, we have a crystal clear evolution of the semantics in all these paths.\
    This means that the players are choosing their next hop based on close semantics.\
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
    As a matter of fact, shortest paths do not seem to follow semantic order along the path. \
    We can clearly notice an evolution increasing in some graphs, decreasing in others, and even both in a couple of them.\
    But before jumping to conclusions only based on 25 paths, let’s explore the rest of the shortest paths and see if we can generalise this fact.")



st.write("For this purpose, we went through all the shortest paths and computed the percentage of the increasing ones versus the \
    non increasing (i.e: decreasing or not monotone) and found the following results: <b> 40% strictly increasing VS 60% not increasing </b> \
    These computations finally prove our observed statement.",unsafe_allow_html=True)



st.write("As a matter of fact, this is what keeps the players from following an optimal strategy. \
    In fact, it’s counter intuitive for humans to act not in accordance with a specific meaning or interpretation \
    because this is the opposite of how the brain was trained to operate. At the same time, this is exactly what allows \
    algorithms to find the optimal routing with a global view of the network without being biased by the meanings.")

st.write("To sum up, a human being will never be able to perform according to the perfect strategy, in a consistent way, \
    because of how the brain functions facing semantics.")

st.write("Now that we have unveiled deeper insights about players' behavior and what keeps them from reaching optimality in the Wikispeedia game, \
    we decide to investigate further improvements that can help players get closer to the shortest path.")


st.markdown("#")
st.markdown("***")
st.markdown("#")
st.markdown('<p class="title-font-left"><b>3. Are there any strategies to avoid ?</b></p>', unsafe_allow_html=True)

st.write("It’s relevant to notice that so far, we were only analysing the games of players who won the game and found their assigned target. \
    What if we take a step back and investigate the unfinished paths to try and find out what went wrong ?")

st.write("Let’s try to use this available data to draw stronger conclusions about what we have been already talking about. \
    First, we can revisit the centrality evolution using the out degree metric on the unfinished paths. This yields the following graph:")


plot_ply(unfinished_evolution,"Out degree")

st.markdown("#")

st.write("We notice that the losers did not stick to the same strategy that consists of finding a central node then following more specific articles \
    until you find the goal. Looking at the graphs, we can see a few different patterns: some players go all the way to a central node, then \
    they either keep on choosing articles with similar high centrality metrics, or they keep on oscillating between high and low metrics. ")

st.write("Another thing to observe is that the confidence intervals for the losers paths are way larger which suggests that they all have different unclear strategies.")

st.write("Moving on, one might wonder how the time spent on the game may affect the overall performance so let’s investigate that.\
    Since we can’t possibly have data of an optimal time spent, aka time spent on shortest paths, because they are not computed with human capacities,\
    we will be comparing both the duration of the losers, and winners games.")

st.write("We found that : \xa0<u><b>Winners</b> have 24.89s on average per hop against 45.97s for <b>Losers</b></u> .",unsafe_allow_html=True)

st.write("So we wanted to test the hypothesis that winners spend on average less time per hop than losers. Performing independant <b>t-test</b> \
    on the means, with the alternative hypothesis being that winners spend <b>less time</b> than losers, \
    we computed the p-value = 6.021e-239 which makes us pretty confident with our assumption. ",unsafe_allow_html=True)

st.write("However, it’s arguable that we test on different sets of data. In other words, the winners and losers may have not played the same games, \
    or even more, they did not play the same number of games so our test may be biased.")

st.write("For this particular reason, we decided to be go deeper and perform a multiple hypothesis testing on the \
    same set of games (i.e: 10 most played games). We used the <b>Benjamini-Hochberg correction</b> to account for the multiplicity of \
    the tests and these are the results:",unsafe_allow_html=True)

col1,col2 = st.columns([0.25,1])
with col2:
    st.markdown("""
 <style type="text/css">
.tg  {border-collapse:collapse;border-color:#ccc;border-spacing:0;}
.tg td{background-color:#fff;border-color:#ccc;border-style:solid;border-width:1px;color:#333;
  font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{background-color:#f0f0f0;border-color:#ccc;border-style:solid;border-width:1px;color:#333;
  font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-if4e{background-color:#f9f9f9;border-color:inherit;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-fymr{border-color:inherit;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-btxf{background-color:#f9f9f9;border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-fymr"></th>
    <th class="tg-fymr"><span style="font-style:normal;text-decoration:none">p_value</span></th>
    <th class="tg-fymr"><span style="font-style:normal;text-decoration:none">reject_null</span></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-if4e">Brain to Telephone</td>
    <td class="tg-btxf">0.000</td>
    <td class="tg-btxf">True</td>
  </tr>
  <tr>
    <td class="tg-fymr">Pyramid to Bean</td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">0.000</span></td>
    <td class="tg-0pky">True</td>
  </tr>
  <tr>
    <td class="tg-if4e">Asteroid to Viking</td>
    <td class="tg-btxf">0.000</td>
    <td class="tg-btxf">True</td>
  </tr>
  <tr>
    <td class="tg-fymr">Batman to Wood</td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">0.000</span></td>
    <td class="tg-0pky">True<br></td>
  </tr>
  <tr>
    <td class="tg-if4e">Cat to Computer</td>
    <td class="tg-btxf"><span style="font-weight:normal;font-style:normal;text-decoration:none">0.003</span></td>
    <td class="tg-btxf">True</td>
  </tr>
  <tr>
    <td class="tg-fymr">Beer to Sun</td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">0.005</span></td>
    <td class="tg-0pky">True</td>
  </tr>
  <tr>
    <td class="tg-if4e"><span style="font-style:normal;text-decoration:none">Bird to Adolf_Hitler</span></td>
    <td class="tg-btxf">0.007</td>
    <td class="tg-btxf">True</td>
  </tr>
  <tr>
    <td class="tg-fymr">Batman to Banana<br></td>
    <td class="tg-0pky">0.016</td>
    <td class="tg-0pky">True</td>
  </tr>
  <tr>
    <td class="tg-if4e">Cat to Microsoft</td>
    <td class="tg-btxf">0.022</td>
    <td class="tg-btxf">True</td>
  </tr>
  <tr>
    <td class="tg-fymr">Batman to The_Holocaust</td>
    <td class="tg-0pky">0.027</td>
    <td class="tg-0pky">True</td>
  </tr>
  <tr>
    <td class="tg-if4e">Theatre to Zebra</td>
    <td class="tg-btxf">0.028</td>
    <td class="tg-btxf">True</td>
  </tr>
  <tr>
    <td class="tg-fymr">Bird to Great_white_shark</td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">0.061</span></td>
    <td class="tg-0pky"><span style="font-weight:normal;font-style:normal;text-decoration:none">False</span></td>
  </tr>
</tbody>
</table>
    """,unsafe_allow_html=True)

_,col2= st.columns([0.2,1])
with col2:
    st.write('Fig2: Hypothesis testing results for time spent per article')

st.markdown("#")


st.write("All the hypothesis testing points towards the fact that winners spend less time per article than losers. \
    This yields insights about their decision making. If you spend less time per article, you have less time to focus on semantics and \
    choose the \"perfect\" next node. If you oblige yourself to go fast, then it is the best way for you to make choices that are not \
    semantically perfect. In that sense, you get closer to the behaviour of the shortest path.")

st.markdown("#")
st.markdown("***")
st.markdown("#")
st.markdown('<p class="title-font"><b>Conclusion</b></p>', unsafe_allow_html=True)

st.write("Now that we have analysed every potential aspect of the game using the data available, \
    let’s wrap up all what we have found. To get an optimal path, it’s crucial to first attain a general article from \
    which you can reach more specific articles. Examples of such articles include “Earth”, “USA”,”Europe”. To find a similar one,\
    you might ask yourself the following question: By accessing this article, will I have a wide range of options from which to choose my next hop? \
    If the answer is yes, then you got it. Once you find such an article, you should immediately start going more specific and try to get closer to your target. \
    Obviously, if your target is of a general topic like “United Kingdom”, you don’t need to go through this step. This is, however, very rare due to \
    skewed degree distribution of nodes in the graph, the reason for which we did not base our analysis on such outliers.")

st.write("Going through the article’s text, you might naturally find yourself attempting to get closer to your target semantically. That is you try to find \
    articles that have similar connotations and talk about close topics. Just don’t do it! In fact, you will waste a lot of time reading the articles just to \
    follow a strategy which is not even optimal. Instead, it’s better to just skim through the first lines of the article and quickly choose your next hop.\
    Following these tips is guaranteed and proven by our data to work and to actually yield the optimal path. Now that you have mastered the art of Wikispeedia, \
    why don’t you try again and see how these tips will improve your game.")

st.markdown("#")
st.write("Now do you feel more confident to [play again](https://mehdizayene-adaes-wikispeedia-homepage-67asrh.streamlit.app/) ?")
