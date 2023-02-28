# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 04:12:26 2023

@author: Stephen Kim
"""

import pandas as pd
import time
import numpy as np
from matplotlib import pyplot as plt

class Baseball():
    
    
    def __init__(self, nationalLeague, americanLeague):
        self.nl = nationalLeague
        self.al = americanLeague
           
    
    def simulateMatchup(self, teamA, teamB):
        '''Function that takes two teams and weights as parameters.
        The stronger team should be teamA, the weaker as teamB.
        Returns the values of the loser'''
        
        random = np.random.uniform(0,1)             # Get random num between 0 and 1

        winRatio = teamA[1]/(teamA[1] + teamB[1])   # Get ratio of stronger team vs weaker team
        if random > winRatio:                       # If random num is greater than winRatio
            loser = [teamA[0], teamA[1]]            # Loser is stronger team
        else:                                       # If random num is lower than winRatio
            loser = [teamB[0], teamB[1]]            # Loser is weaker team
      
        return loser                                # Return loser
    
    
    def simulatePlayoffs(self):
        '''Function that simulates 2022 playoff scenario'''
        
        nl = self.nl.copy()
        al = self.al.copy()
        
        nl2, al2 = self.wildCard(nl, al)                     # Simulate wild card round
        nl3, al3 = self.divisionSeries(nl2, al2)             # Simulate divisional series round
        nl4, al4 = self.championshipSeries(nl3, al3)         # Simulate league championship round
        champ = self.worldSeries(nl4, al4)                   # Simulate world series
                
        return champ
    
    
    def runSimulation(self, trials = 1000000):
        '''Function that runs the playoff scenario a default 1,000,000 times.
        Track the world series winners and plot results'''
        
        championData = []
        teamChamps = []

        for i in range(trials):
            championData.append(self.simulatePlayoffs())
            teamChamps.append(championData[i][1])
        
        fig, ax = plt.subplots()
        df = pd.DataFrame({'Team':teamChamps})
        df['Team'].value_counts().plot(ax = ax, kind = 'bar', xlabel = 'Team', ylabel = 'Wins')
        plt.show()
        
        wins = df['Team'].value_counts()
        self.printResults(wins)
                        
        return teamChamps
    
    
    def printResults(self, wins):
        '''Function to print results'''
        
        print(wins)                
        
        return
                  
    
    def wildCard(self, nl, al):
        '''Function that eliminates wild card round losers'''
                
        # American League 3/6 matchup
        am1 = self.simulateMatchup(al[3], al[6])                  # Simulate matchup and return loser values
        value1 = list(al.keys())[list(al.values()).index(am1)]    # Get key from loser values
        del al[value1]                                                 # Remove loser from playoffs
        
        # American League 4/5 matchup
        am2 = self.simulateMatchup(al[4], al[5])
        value2 = list(al.keys())[list(al.values()).index(am2)]
        del al[value2]
        
        # National League 3/6 matchup
        am3 = self.simulateMatchup(nl[3], nl[6])
        value3 = list(nl.keys())[list(nl.values()).index(am3)]
        del nl[value3]
        
        # National League 4/5 matchup
        am4 = self.simulateMatchup(nl[4], nl[5])
        value4 = list(nl.keys())[list(nl.values()).index(am4)]
        del nl[value4]
        
        return nl, al
        
        
    def divisionSeries(self, nl, al):
        '''Function that returns the divional round winners'''
        
        # American League 1 vs 4/5 matchup
        if 4 in al:                                                    # If 4th ranked team is still alive
            am1 = self.simulateMatchup(al[1], al[4])              # Simulate 1 v 4 matchup
        else:                                                               # If 5th ranked team is still alive
            am1 = self.simulateMatchup(al[1], al[5])              # Simulate 1 v 5 matchup
        value1 = list(al.keys())[list(al.values()).index(am1)]    # Get key of loser
        del al[value1]                                                 # Remove loser from playoffs
        
        # American League 2 vs 3/6 matchup
        if 3 in al:
            am2 = self.simulateMatchup(al[2], al[3])
        else:
            am2 = self.simulateMatchup(al[2], al[6])
        value2 = list(al.keys())[list(al.values()).index(am2)]
        del al[value2]
        
        # National League 1 vs 4/5 matchup
        if 4 in nl:
            am3 = self.simulateMatchup(nl[1], nl[4])
        else:
            am3 = self.simulateMatchup(nl[1], nl[5])
        value3 = list(nl.keys())[list(nl.values()).index(am3)]
        del nl[value3]
        
        # National League 2 vs 3/6 matchup
        if 3 in nl:
            am4 = self.simulateMatchup(nl[2], nl[3])
        else:
            am4 = self.simulateMatchup(nl[2], nl[6])
        value4 = list(nl.keys())[list(nl.values()).index(am4)]
        del nl[value4]
        
        return nl, al
    
    
    def championshipSeries(self, nl, al):
        '''Function that returns the league championship winners'''
        
        # American League matchup
        alTeams = list(al.keys())                                              # Get list of keys of playoff teams left
        if alTeams[0] > alTeams[1]:                                                 # Find the higher ranked team
            am1 = self.simulateMatchup(al[alTeams[0]], al[alTeams[1]])    # Simulate matchup with higher ranked team input first
        else:
            am1 = self.simulateMatchup(al[alTeams[1]], al[alTeams[0]])
            value1 = list(al.keys())[list(al.values()).index(am1)]        # Get key of loser
            del al[value1]                                                     # Remove loser from playoffs
            
        # National League matchup
        nlTeams = list(nl.keys())
        if nlTeams[0] > nlTeams[1]:
            am2 = self.simulateMatchup(nl[nlTeams[0]], nl[nlTeams[1]])
        else:
            am2 = self.simulateMatchup(nl[nlTeams[1]], nl[nlTeams[0]])
            value2 = list(nl.keys())[list(nl.values()).index(am2)]
            del nl[value2]
        
        return nl, al
        
    
    def worldSeries(self, nl, al):     
        '''Function that returns the world series champion'''
        
        alTeam = list(al.keys())       # Get AL team key
        nlTeam = list(nl.keys())       # Get NL team key
        
        if nlTeam[0] > alTeam[0]:                                                   # If NL team is stronger
            am = self.simulateMatchup(nl[nlTeam[0]], al[alTeam[0]])       # Simulate match with NL team input first
        else:                                                                       # Else input AL team first
            am = self.simulateMatchup(al[alTeam[0]], nl[nlTeam[0]])       # Get world series winner
        
        if am in nl.values():                                                  # If winner is in NL
            value = list(nl.keys())[list(nl.values()).index(am)]          # Get ranking from value
        else:                                                                       # Else get AL winner
            value = list(al.keys())[list(al.values()).index(am)]
            
        winner = []
        winner.append(value)
        winner.append(am[0])
        winner.append(am[1])
            
        return winner
    

    
    
    
nationalLeague = {1: ['Dodgers', 0.91], 2: ['Braves', 0.82],
                  3: ['Cardinals', 0.75], 4: ['Mets', 0.71], 
                  5: ['Padres', 0.66], 6: ['Phillies', 0.73]} 

americanLeague = {1: ['Astros', 0.88], 2: ['Yankees', 0.87],
                  3: ['Guardians', 0.75], 4: ['Blue Jays', 0.72],
                  5: ['Mariners', 0.69], 6: ['Mariners', 0.66]} 

b = Baseball(nationalLeague, americanLeague)
r = b.simulatePlayoffs()
r
start_time = time.time()
results = b.runSimulation()
print()
print("Unbatched: %s seconds" % (time.time() - start_time))

#winner = b.simulateOneGame(teamA, teamB)
#print("The {} are victorious".format(winner))
#season = b.simulateSeason()
#print(season)