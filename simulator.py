import streamlit as st
import pandas as pd
import random as rd
import plotly.express as px
import plotly.graph_objects as go

class HomeTeam:
    def __init__(self, team, data):
        self.data = data[data['home_team'] == team].copy()
   
    def getMatchupRuns(self, away_team):
        return self.data[(self.data['away_team'] == away_team)]['home_runs']
    
    def getMatchupWickets(self, away_team):
        return self.data[(self.data['away_team'] == away_team)]['home_wickets']
    
    def getRuns(self):
        return self.data['home_runs']
            
    def getWickets(self):
        return self.data['home_wickets']
                         
class AwayTeam:
    def __init__(self, team, data):
        self.data = data[(data['away_team'] == team)].copy()

    def getMatchupRuns(self, home_team):
        return self.data[(self.data['home_team'] == home_team)]['away_runs']
    
    def getMatchupWickets(self, home_team):
        return self.data[(self.data['home_team'] == home_team)]['away_wickets']
    
    def getRuns(self):
        return self.data['away_runs']
    
        
    def getWickets(self):
        return self.data['away_wickets']

def sim_game(home, away):
    home_team = HomeTeam(home, df)
    away_team = AwayTeam(away, df)
    home_runs = (rd.gauss(home_team.getRuns().mean(), home_team.getRuns().std()) + rd.gauss(home_team.getMatchupRuns(away).mean(), home_team.getMatchupRuns(away).std()))/2
    away_runs = (rd.gauss(away_team.getRuns().mean(), away_team.getRuns().std()) + rd.gauss(away_team.getMatchupRuns(home).mean(), away_team.getMatchupRuns(home).std()))/2
    home_wickets = (rd.gauss(home_team.getWickets().mean(), home_team.getWickets().std()) + rd.gauss(home_team.getMatchupWickets(away).mean(), home_team.getMatchupWickets(away).std()))/2
    away_wickets = (rd.gauss(away_team.getWickets().mean(), away_team.getWickets().std()) + rd.gauss(away_team.getMatchupWickets(home).mean(), away_team.getMatchupWickets(home).std()))/2
    
    home_team_score = home_runs - home_wickets
    away_team_score = away_runs - away_wickets
    if (home_team_score > away_team_score):
        return home
    else:
        return away

def SetColor(x):
        if(x == 'CSK'):
            return '#F9CD05'
        elif(x == 'RCB'):
            return '#EC1C24'
        elif(x == 'SRH'):
            return '#FF822A'
        elif(x == 'KKR'):
            return '#2E0854'
        elif(x == 'KXIP'):
            return '#DCDDDF'
        elif(x == 'RR'):
            return '#254AA5'
        elif(x == 'DC'):
            return '#00008B'
        elif(x == 'MI'):
            return '#004BA0'

st.set_page_config(page_title='IPL Dashboard by Viren', layout="wide", page_icon='favicon.ico')
@st.cache
def load_data():
    matches = pd.read_csv("all_season_summary.csv")
    return matches

df = load_data()

layout = go.Layout(
    template='plotly_dark',
    xaxis=dict(title_text='', showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(title_text=''),
    title=dict(x=0.5, y=0.9),
    width=600
)

new_layout = go.Layout(
    template='plotly_dark',
    xaxis=dict(title_text='', showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(title_text=''),
    title=dict(x=0.5, y=0.9),
    width=600,
    showlegend=False
)

full_layout = go.Layout(
    template='plotly_dark',
    xaxis=dict(title_text='', showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(title_text=''),
    title=dict(x=0.5, y=0.9),
    showlegend=False,
    height=600,
    width=1200
)

ind_layout = go.Layout(
    template='plotly_dark',
    xaxis=dict(title_text='', showgrid=False),
    yaxis=dict(showgrid=False),
    legend=dict(title_text=''),
    title=dict(x=0.5, y=0.9),
    width=300,
    showlegend=False
)

st.markdown("<h1 style='text-align: center;'>Viren's IPL Dashboard  </h1>", unsafe_allow_html=True)
c1, c2 = st.beta_columns((3,2))
c1.header('2021 Analysis')
c1.subheader('This space will be updated regularly during the IPL-2021 season')
new_df = df[df['season']==2021]
new_fig = go.Figure(data=[
    go.Bar(
        x=new_df['short_name'],
        y=df['home_runs'],
        marker=dict(color=list(map(SetColor, new_df['home_team']))),
        width=[0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4]
    ),
    go.Bar(
        x=new_df['short_name'],
        y=df['away_runs'],
        marker=dict(color=list(map(SetColor, new_df['away_team']))),
        width=[0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4]
    )
], layout=new_layout)
new_fig.update_layout(barmode='group')
c1.plotly_chart(new_fig)

c2.header('IPL Simulator')
teams = {'Chennai Super Kings': 'CSK', 'Royal Challengers Bangalore': 'RCB', 'Mumbai Indians': 'MI', 'Punjab Kings': 'KXIP', 'Sunrisers Hyederabad': 'SRH', 'Delhi Capitals': 'DC', 'Rajasthan Royals': 'RR', 'Kolkata Knight Riders': 'KKR'}
team_list = list(teams.keys())
home_team = c2.selectbox('Home Team:', team_list)
team_list.remove(home_team)
away_team = c2.selectbox('Away Team:', team_list)

sim = sim_game(teams[home_team], teams[away_team])
c2.image(f'{sim.lower()}.png', width=200)

c7,c8,c9 = st.beta_columns(3)
bowl_first = (new_df[new_df['decision'] == 'BOWL FIRST'].shape[0] / new_df.shape[0]) * 100
toss_chart = go.Figure(data=[go.Indicator(
    value=bowl_first,
    title= {'text': 'Toss Win & Bowl First %'},
    mode='gauge+number',
    gauge= { 'axis': {'visible': False, 'range': [0,100]}},
)], layout= ind_layout)
c7.plotly_chart(toss_chart)

home_win_percent = (new_df[new_df['winner'] == new_df['home_team']].shape[0] / new_df.shape[0]) * 100
home_win_chart = go.Figure(data=[go.Indicator(
    value=home_win_percent,
    mode='gauge+number',
    title= {'text': 'Home Team Win %'},
    gauge= { 'axis': {'visible': False, 'range': [0,100]}, 'bar': {'color': 'red'}},
)], layout= ind_layout)
c8.plotly_chart(home_win_chart)

bowl_first_win_percent = (new_df[new_df['2nd_in_win'] == True].shape[0] / new_df.shape[0]) * 100
bowl_first_win_chart = go.Figure(data=[go.Indicator(
    value=bowl_first_win_percent,
    mode='gauge+number',
    title= {'text': 'Bowl First Win %'},
    gauge= {'axis': {'visible': False, 'range': [0,100]}, 'bar': {'color': 'yellow'}}
)], layout=ind_layout)
c9.plotly_chart(bowl_first_win_chart)

st.header('Story So Far')
c3, c4 = st.beta_columns(2)
s = df.winner.value_counts()
win_df = pd.DataFrame({'Team': s.index, 'Wins': s.values}).nlargest(8, 'Wins')
win_fig = go.Figure(data=[go.Bar(
    x=win_df['Team'],
    y=win_df['Wins'],
    width=[0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6]
)], layout=layout)
c3.subheader('Total Wins')
c3.plotly_chart(win_fig)

toss_dec = df.decision.value_counts()
toss_dec_df = pd.DataFrame({'Toss': toss_dec.index, 'Count': toss_dec.values})
toss_dec_fig = go.Figure(data=[go.Bar(
    x=toss_dec_df['Toss'],
    y=toss_dec_df['Count'],
    width=[0.2,0.2,0.2]
)], layout=layout)
c4.subheader('Toss Decisions')
c4.plotly_chart(toss_dec_fig)

c5, c6 = st.beta_columns(2)
toss_won = df.toss_won.value_counts()
toss_won_df = pd.DataFrame({'Team': toss_won.index, 'Number of Toss Won': toss_won.values}).nlargest(8, 'Number of Toss Won')
toss_won_fig = go.Figure(data=[go.Bar(
    x=toss_won_df['Team'],
    y=toss_won_df['Number of Toss Won'],
    width=[0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4]
)], layout=layout)
c5.subheader('Toss Wins')
c5.plotly_chart(toss_won_fig)

pom = df.pom.value_counts()
pom_df = pd.DataFrame({'Player': pom.index, 'Wins': pom.values}).nlargest(10, 'Wins')
pom_fig = go.Figure(data=[go.Bar(
    x=pom_df['Player'],
    y=pom_df['Wins'],
    width=[0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.6]
)], layout=layout)
c6.subheader('Player of the Match')
c6.plotly_chart(pom_fig)

venue_boundaries_fig = go.Figure(data=[go.Bar(
    x=df['total_boundaries'],
    y=df['venue_name'],
    orientation='h'
)], layout=full_layout)
st.subheader('Boundaries per Venue')
st.write(venue_boundaries_fig)
