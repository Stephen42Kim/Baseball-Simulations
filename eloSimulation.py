# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 12:39:51 2023

@author: Stephen
"""

from parseText import parseTextFile

import numpy as np
import math
import json
import pandas as pd

class eloSim:
    def __init__(self, teams: dict) -> None:
        '''
        Holding each trials wins and elo for each team
        '''
        self.avgTeamWins = {key: np.array([]) for key in teams}
        self.avgTeamElo = {key: np.array([]) for key in teams}




    def calculateProbability(self, homeTeamElo: int, awayTeamElo: int) -> float:
        '''
        Calculating the win percentage of each team
        team1 - First team's rating
        team2 - Second team's rating
        '''

        homeTeamProb = (1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (awayTeamElo - homeTeamElo) / 400)))
        awayTeamProb = (1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (homeTeamElo - awayTeamElo) / 400)))

        return homeTeamProb, awayTeamProb
    



    def adjustRating(self, currentRating: int, k: int, outcome: int, winProb: float) -> int:
        '''
        k - K-factor
        currentRating - Elo rating of team
        outcome - 1 for win, 0 for loss
        winProb - Probability of beating other team
        '''

        newRating = currentRating + (k * (outcome - winProb))
        return newRating




    def randFloat(self) -> float:
        return np.random.rand()
    


    def dataframe(self, wins: dict, elo: dict):
        return pd.DataFrame({'Predicted Wins':pd.Series(wins), 'Predicted Elo': pd.Series(elo)})




    def simSeason(self, gameStats: dict, teamElo: dict, teamWins: dict) -> dict:

        '''
        gameStats - Game log data 
        teamElo - Used to create a copy for running elo for season
        runningWins - Used to create a copy for running wins for season
        '''

        # Holding the running ELO and win totals for each team
        runningElo = teamElo.copy()
        runningWins = teamWins.copy()

        for i in range(1, len(gameStats)+1):

            homeTeam = gameStats[i]['Home']['Team']
            awayTeam = gameStats[i]['Away']['Team']
            # Actual scores can be used to measure against
            homeScore = gameStats[i]['Home']['Score']
            awayScore = gameStats[i]['Away']['Score']

            homeTeamElo = teamElo[homeTeam]
            awayTeamElo = teamElo[awayTeam]

            homeTeamProb, awayTeamProb = self.calculateProbability(homeTeamElo, awayTeamElo)

            randNum = self.randFloat()

            newHomeRtg = None
            newAwayRtg = None

            # Home team wins
            if randNum <= homeTeamProb: 
                newHomeRtg = self.adjustRating(runningElo[homeTeam], k=32, outcome=1, winProb=homeTeamProb)
                newAwayRtg = self.adjustRating(runningElo[awayTeam], k=32, outcome=0, winProb=awayTeamProb)
                runningWins[homeTeam] += 1
            # Away team wins
            else: 
                newHomeRtg = self.adjustRating(runningElo[homeTeam], k=32, outcome=0, winProb=homeTeamProb)
                newAwayRtg = self.adjustRating(runningElo[awayTeam], k=32, outcome=1, winProb=awayTeamProb)
                runningWins[awayTeam] += 1

            # Updating elo rating for each team
            runningElo[homeTeam] = newHomeRtg
            runningElo[awayTeam] = newAwayRtg

        
        return runningWins, runningElo
    



    def runManySeasons(self, nTrials: int, gameStats: dict, teamElo: dict, teamWins: dict) -> dict:

        '''
        nTrials - Number of trials to be ran
        gameStats - Game log data
        teamElo - Will be passed to simSeason 
        teamWins - Will be passed to simSeason
        '''

        for i in range(nTrials):
            wins, elo = self.simSeason(gameStats, teamElo, teamWins)

            for team in wins.keys():
                self.avgTeamWins[team] = np.append(self.avgTeamWins[team], wins[team])

            for team in elo.keys():
                self.avgTeamElo[team] = np.append(self.avgTeamElo[team], elo[team])

            eloAvg = {team: np.mean(elo) for team, elo in self.avgTeamElo.items()}
            winsAvg = {team: np.mean(wins) for team, wins in self.avgTeamWins.items()}

        return eloAvg, winsAvg




def main():
    '''
    Preseason ELO scores for each team for 2022
    URL: https://projects.fivethirtyeight.com/2022-mlb-predictions/
        - Select preseason from dropdown at bottom of page
    '''
    statFile = 'stats-2022.txt'
    gameStats = parseTextFile(statFile) # Returns a dictionary

    # Starting elo values from 2022 preseason 
    teamElo = {
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
    teamWins = {key: 0 for key in teamElo}

    sim = eloSim(teamWins)
    eloAvg, winsAvg = sim.runManySeasons(1000, gameStats, teamElo, teamWins)
    df = sim.dataframe(wins=winsAvg, elo=eloAvg)

    #print(df)
    #print(json.dumps(dict(sorted(eloAvg.items(), key=lambda x:x[1], reverse=True)), indent=4))
    #print(json.dumps(dict(sorted(winsAvg.items(), key=lambda x:x[1], reverse=True)), indent=4))
    return df  





if __name__ == '__main__':
    df = main()
    print(df)
