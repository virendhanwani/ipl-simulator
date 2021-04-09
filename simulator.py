import streamlit as st
import pandas as pd
import random as rd

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

@st.cache
def load_data():
    matches = pd.read_csv("all_season_summary.csv")
    return matches

df = load_data()
teams = {'Chennai Super Kings': 'CSK', 'Royal Challengers Bangalore': 'RCB', 'Mumbai Indians': 'MI', 'Punjab Kings': 'KXIP', 'Sunrisers Hyederabad': 'SRH', 'Delhi Capitals': 'DC', 'Rajasthan Royals': 'RR', 'Kolkata Knight Riders': 'KKR'}
team_list = list(teams.keys())
home_team = st.selectbox('Home Team:', team_list)
team_list.remove(home_team)
away_team = st.selectbox('Away Team:', team_list)

sim = sim_game(teams[home_team], teams[away_team])
st.write(sim)