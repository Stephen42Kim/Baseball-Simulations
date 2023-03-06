# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 03:58:53 2023

@author: Stephen Kim
"""

import eloSimulation
import PlayoffSim
import parseText
import pandas as pd

class MLBFullSeason():
    
    def __init__(self, statsDict, teamELO, teamWins):
        '''MLBFullSeason class takes three parameters.
        Dictionary of game logs from Retrosheet.com
        Dictionary of team ELO values generated from preseason from 538.com
        Dictionary of team wins with each team starting at 0'''
        
        self.statsDict = statsDict                  # Dict of game stats
        self.teamELO = teamELO                      # Dict of elo values from preseason 
        self.teamWins = teamWins                    # Dict of team wins reset to 0
        
        return
    
    def SimulateRegularSeason(self, nTrials = 1000):
        '''Function that takes number of trials as parameter with default set at 10_000.
        Return for each team the end of season predicted wins and predicted ELO'''
        
        sim = eloSimulation.eloSim(self.teamELO)
        eloAvg, winsAvg = sim.runManySeasons(nTrials, self.statsDict, self.teamELO, self.teamWins)
        df = sim.dataframe(winsAvg, eloAvg)
        
        return df
    
    
    def PlayoffTeamPredictor2022(self, df):
        '''Function that takes dictionary of average predicted wins per team and returns 
        two dictionaries for the NL and AL playoff teams with seeding and power ranking'''
                
        ALEast = self.getALEast(df)
        ALCentral = self.getALCentral(df)
        ALWest = self.getALWest(df)
        NLEast = self.getNLEast(df)
        NLCentral = self.getNLCentral(df)
        NLWest = self.getNLWest(df)
        
        playoffAL = self.ALPlayoffTeams(ALEast, ALCentral, ALWest)
        playoffNL = self.NLPlayoffTeams(NLEast, NLCentral, NLWest)
        
        return playoffAL, playoffNL
    
    
    def SimulatePlayoffs(self, nl, al, nTrials = 100000):
        '''Function that takes a dict of nl playoff teams and a dict of al playoff
        teams (that both contain the seeding, name, and ELO rating of each team) and 
        number of nTrials as parameters, then runs the playoff
        simulation nTrials times and returns the odds of each playoff team winning
        the World Series'''
        
        sim = PlayoffSim.Baseball(nl, al)
        winners = sim.runSimulation(nTrials)   
        
        return winners
    
    
    
    
    
    def ALPlayoffTeams(self, ALEast, ALCentral, ALWest):
        '''Function that takes AL division dataframes and returns dictionary
        for AL playoff teams with seeding, name, and ELO rating'''
        
        al = {}
        
        # Concatenate AL divisions and order by predicted wins
        dfMerge = pd.concat([ALEast, ALCentral, ALWest])
        dfMerge = dfMerge.sort_values(by = 'Predicted Wins', ascending = False)
        #print(dfMerge)
        
        # Get AL division winners and order by predicted wins
        divWinners = pd.DataFrame([ALEast.iloc[0], ALCentral.iloc[0], ALWest.iloc[0]])
        divWinners = divWinners.sort_values(by = 'Predicted Wins', ascending = False)
        #print(divWinners)
        
        # Get AL wild card teams
        wildCard = dfMerge.reset_index().merge(divWinners, how = 'left', indicator = True).set_index('index').loc[lambda x: x['_merge']=='left_only']
        #print(wildCard)
        
        # No. 1 seed is team with best league record
        al[1] = [str(divWinners.index[0]), divWinners.iloc[0]['Predicted Elo']]
        
        # No. 2 seed is second best division winner
        al[2] = [str(divWinners.index[1]), divWinners.iloc[1]['Predicted Elo']]
        
        # No. 3 seed is third best division winner
        al[3] = [str(divWinners.index[2]), divWinners.iloc[2]['Predicted Elo']]
        
        # No. 4 - 6 seeds are top three wild card teams
        al[4] = [str(wildCard.index[0]), wildCard.iloc[0]['Predicted Elo']]
        
        al[5] = [str(wildCard.index[1]), wildCard.iloc[1]['Predicted Elo']]
        
        al[6] = [str(wildCard.index[2]), wildCard.iloc[2]['Predicted Elo']]
        
        return al
    
    def NLPlayoffTeams(self, NLEast, NLCentral, NLWest):
        '''Function that takes NL division dataframes and returns dictionary
        for AL playoff teams with seeding, name, and ELO rating'''
        
        nl = {}
        
        # Concatenate NL divisions and order by predicted wins
        dfMerge = pd.concat([NLEast, NLCentral, NLWest])
        dfMerge = dfMerge.sort_values(by = 'Predicted Wins', ascending = False)
        #print(dfMerge)
        
        # Get NL division winners and order by predicted wins
        divWinners = pd.DataFrame([NLEast.iloc[0], NLCentral.iloc[0], NLWest.iloc[0]])
        divWinners = divWinners.sort_values(by = 'Predicted Wins', ascending = False)
        #print(divWinners)
        
        # Get the NL WildCard teams
        wildCard = dfMerge.reset_index().merge(divWinners, how = 'left', indicator = True).set_index('index').loc[lambda x: x['_merge']=='left_only']
        #print(wildCard)
        
        # No. 1 seed is team with best league record
        nl[1] = [str(divWinners.index[0]), divWinners.iloc[0]['Predicted Elo']]
        
        # No. 2 seed is second best division winner
        nl[2] = [str(divWinners.index[1]), divWinners.iloc[1]['Predicted Elo']]
        
        # No. 3 seed is third best division winner
        nl[3] = [str(divWinners.index[2]), divWinners.iloc[2]['Predicted Elo']]
        
        # No. 4 - 6 seeds are top three wild card teams
        nl[4] = [str(wildCard.index[0]), wildCard.iloc[0]['Predicted Elo']]
        
        nl[5] = [str(wildCard.index[1]), wildCard.iloc[1]['Predicted Elo']]
        
        nl[6] = [str(wildCard.index[2]), wildCard.iloc[2]['Predicted Elo']]
        
        return nl
        
    
    def getALEast(self, df):
        '''Return pandas dataframe of ALEast predicted wins and elo rating'''
        
        alEast = df[df.index.str.startswith(('BAL', 'BOS', 'NYA', 'TBA', 'TOR'))]
        
        #print(alEast)
        
        return alEast
    
    
    def getALCentral(self, df):
        '''Return pandas dataframe of ALCentral predicted wins and elo rating'''
        
        alCentral = df[df.index.str.startswith(('CHA', 'CLE', 'DET', 'KCA', 'MIN'))]
        
        #print(alCentral)
        
        return alCentral
    
    
    def getALWest(self, df):
        '''Return pandas dataframe of ALWest predicted wins and elo rating'''
        
        alWest = df[df.index.str.startswith(('HOU', 'ANA', 'OAK', 'SEA', 'TEX'))]
        
        #print(alWest)
        
        return alWest
    
    
    def getNLEast(self, df):
        '''Return pandas dataframe of NLEast predicted wins and elo rating'''
        
        nlEast = df[df.index.str.startswith(('ATL', 'MIA', 'NYN', 'PHI', 'WAS'))]
        
        #print(nlEast)
        
        return nlEast
    
    
    def getNLCentral(self, df):
        '''Return pandas dataframe of NLCentral predicted wins and elo rating'''
        
        nlCentral = df[df.index.str.startswith(('CHN', 'CIN', 'MIL', 'PIT', 'SLN'))]
        
        #print(nlCentral)
        
        return nlCentral
    
    
    def getNLWest(self, df):
        '''Return pandas dataframe of NLWest predicted wins and elo rating'''
        
        nlWest = df[df.index.str.startswith(('LAN', 'SDN', 'SFN', 'COL', 'ARI'))]
        
        #print(nlWest)
        
        return nlWest
    
    
    
    
    
    
    
    
    
# Game logs found at https://www.retrosheet.org/gamelogs/index.html    
statFile = 'stats-2022.txt'
gameStats = parseText.parseTextFile(statFile) # Returns a dictionary    

# Starting elo values from 2022 preseason 
teamELO2022 = {
    'LAN': 1581,
    'ATL': 1555,
    'NYA': 1554,
    'TOR': 1553,
    'HOU': 1544,
    'CHA': 1541,
    'MIL': 1542,
    'SDN': 1531,
    'TBA': 1531,
    'BOS': 1530,
    'PHI': 1522,
    'NYN': 1520,
    'ANA': 1518,
    'SFN': 1518,
    'MIN': 1514,
    'SLN': 1501,
    'SEA': 1501,
    'CIN': 1499,
    'CLE': 1493,
    'MIA': 1488,
    'CHN': 1479,
    'DET': 1471,
    'KCA': 1472, 
    'WAS': 1469,
    'TEX': 1467,
    'COL': 1464,
    'ARI': 1459,
    'OAK': 1456,
    'PIT': 1446,
    'BAL': 1430,
}

# Starting team wins all at 0
teamWins = {key: 0 for key in teamELO2022}    
    
# Create MLB Simulator object
mlb = MLBFullSeason(gameStats, teamELO2022, teamWins)


# Simulate regular season (optional paramater is number of trials - default is 10_000)
df = mlb.SimulateRegularSeason()
type(df)
#print(df)
#print(df.index)

# Extract playoff teams
nl, al = mlb.PlayoffTeamPredictor2022(df)
#print(nl)
#print(al)

# Simulate playoffs
winners = mlb.SimulatePlayoffs(nl, al, 1000000)
#print(winners)
# Show odds of winning world series