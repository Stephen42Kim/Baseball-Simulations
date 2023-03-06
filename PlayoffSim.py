# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 04:12:26 2023

@author: Stephen Kim
"""


import re
import pandas as pd
import time
import numpy as np
from matplotlib import pyplot as plt
from statistics import mode

class Baseball():
    
    
    def __init__(self, nationalLeague, americanLeague):
        self.nl = nationalLeague
        self.al = americanLeague
           
    
    def simulateMatchup(self, teamA, teamB):
        '''Function that takes two lists as parameters, one representing each team.
        First element in list is the team seeding.
        Second element in list is a list containing team name and distribution.
        Returns the losing team seed.'''
        
        random = np.random.uniform(0,1)             # Get random num between 0 and 1

        winRatio = teamA[1]/(teamA[1] + teamB[1])            # Get ratio of teamA to teamB
        
        if random > winRatio:                       # If random num is greater than winRatio
            return teamA[0]                         # Loser is teamA
        else:                                       # If random num is lower than winRatio
            return teamB[0]                         # Loser is teamB
    
    
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
        '''Function that runs the playoff scenario default 1,000,000 times.
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
        # Simulate each game with rotating pitcher and track losing team
        loser1 = []
        loser1.append(self.simulateMatchup([3, al[3][1]], [6, al[6][1]]))  
        loser1.append(self.simulateMatchup([3, al[3][2]], [6, al[6][2]])) 
        loser1.append(self.simulateMatchup([3, al[3][3]], [6, al[6][3]]))
        
        # Remove the team that has lost the most (Lost best of 3)
        l1 = mode(loser1)
        del al[l1]
                 
        
        # American League 4/5 matchup
        loser2 = []
        loser2.append(self.simulateMatchup([4, al[4][1]], [5, al[5][1]]))  
        loser2.append(self.simulateMatchup([4, al[4][2]], [5, al[5][2]])) 
        loser2.append(self.simulateMatchup([4, al[4][3]], [5, al[5][3]]))
        l2 = mode(loser2)
        del al[l2]
        
        # National League 3/6 matchup
        loser3 = []
        loser3.append(self.simulateMatchup([3, nl[3][1]], [6, nl[6][1]]))  
        loser3.append(self.simulateMatchup([3, nl[3][2]], [6, nl[6][2]])) 
        loser3.append(self.simulateMatchup([3, nl[3][3]], [6, nl[6][3]]))
        l3 = mode(loser3)
        del nl[l3]
        
        # National League 4/5 matchup
        loser4 = []
        loser4.append(self.simulateMatchup([4, nl[4][1]], [5, nl[5][1]]))  
        loser4.append(self.simulateMatchup([4, nl[4][2]], [5, nl[5][2]])) 
        loser4.append(self.simulateMatchup([4, nl[4][3]], [5, nl[5][3]]))
        l4 = mode(loser4)
        del nl[l4]
        
        return nl, al
        
        
    def divisionSeries(self, nl, al):
        '''Function that returns the divional round winners'''
        
        # American League 1 vs 4/5 matchup
        loser1 = []
        
        # If 4th ranked team is still alive, simulate 1 vs 4 series
        if 4 in al:                                                     
            loser1.append(self.simulateMatchup([1, al[1][1]], [4, al[4][1]]))  
            loser1.append(self.simulateMatchup([1, al[1][2]], [4, al[4][2]])) 
            loser1.append(self.simulateMatchup([1, al[1][3]], [4, al[4][3]]))
            loser1.append(self.simulateMatchup([1, al[1][1]], [4, al[4][1]]))  
            loser1.append(self.simulateMatchup([1, al[1][2]], [4, al[4][2]])) 
        
        # Else if 5th ranked team is still alive, simulate 1 vs 5 series
        else:                                                           
            loser1.append(self.simulateMatchup([1, al[1][1]], [5, al[5][1]]))  
            loser1.append(self.simulateMatchup([1, al[1][2]], [5, al[5][2]])) 
            loser1.append(self.simulateMatchup([1, al[1][3]], [5, al[5][3]]))
            loser1.append(self.simulateMatchup([1, al[1][1]], [5, al[5][1]]))  
            loser1.append(self.simulateMatchup([1, al[1][2]], [5, al[5][2]])) 
        # Remove team with most losses from playoffs
        l1 = mode(loser1)
        del al[l1]                                                  
        
        # American League 2 vs 3/6 matchup
        loser2 = []
        
        # If 3th ranked team is still alive, simulate 2 vs 3 series
        if 3 in al:                                                     
            loser2.append(self.simulateMatchup([2, al[2][1]], [3, al[3][1]]))  
            loser2.append(self.simulateMatchup([2, al[2][2]], [3, al[3][2]])) 
            loser2.append(self.simulateMatchup([2, al[2][3]], [3, al[3][3]]))
            loser2.append(self.simulateMatchup([2, al[2][1]], [3, al[3][1]]))  
            loser2.append(self.simulateMatchup([2, al[2][2]], [3, al[3][2]])) 
        
        # Else if 6thth ranked team is still alive, simulate 2 vs 6 series
        else:                                                           
            loser2.append(self.simulateMatchup([2, al[2][1]], [6, al[6][1]]))  
            loser2.append(self.simulateMatchup([2, al[2][2]], [6, al[6][2]])) 
            loser2.append(self.simulateMatchup([2, al[2][3]], [6, al[6][3]]))
            loser2.append(self.simulateMatchup([2, al[2][1]], [6, al[6][1]]))  
            loser2.append(self.simulateMatchup([2, al[2][2]], [6, al[6][2]])) 
        # Remove team with most losses from playoffs
        l2 = mode(loser2)
        del al[l2]  
        
        # National League 1 vs 4/5 matchup
        loser3 = []
        
        # If 4th ranked team is still alive, simulate 1 vs 4 series
        if 4 in nl:                                                     
            loser3.append(self.simulateMatchup([1, nl[1][1]], [4, nl[4][1]]))  
            loser3.append(self.simulateMatchup([1, nl[1][2]], [4, nl[4][2]])) 
            loser3.append(self.simulateMatchup([1, nl[1][3]], [4, nl[4][3]]))
            loser3.append(self.simulateMatchup([1, nl[1][1]], [4, nl[4][1]]))  
            loser3.append(self.simulateMatchup([1, nl[1][2]], [4, nl[4][2]])) 
        
        # Else if 5th ranked team is still alive, simulate 1 vs 5 series
        else:                                                           
            loser3.append(self.simulateMatchup([1, nl[1][1]], [5, nl[5][1]]))  
            loser3.append(self.simulateMatchup([1, nl[1][2]], [5, nl[5][2]])) 
            loser3.append(self.simulateMatchup([1, nl[1][3]], [5, nl[5][3]]))
            loser3.append(self.simulateMatchup([1, nl[1][1]], [5, nl[5][1]]))  
            loser3.append(self.simulateMatchup([1, nl[1][2]], [5, nl[5][2]])) 
        # Remove team with most losses from playoffs
        l3 = mode(loser3)
        del nl[l3]  
        
        # National League 2 vs 3/6 matchup
        loser4 = []
        
        # If 3th ranked team is still alive, simulate 2 vs 3 series
        if 3 in nl:                                                     
            loser4.append(self.simulateMatchup([2, nl[2][1]], [3, nl[3][1]]))  
            loser4.append(self.simulateMatchup([2, nl[2][2]], [3, nl[3][2]])) 
            loser4.append(self.simulateMatchup([2, nl[2][3]], [3, nl[3][3]]))
            loser4.append(self.simulateMatchup([2, nl[2][1]], [3, nl[3][1]]))  
            loser4.append(self.simulateMatchup([2, nl[2][2]], [3, nl[3][2]])) 
        
        # Else if 6thth ranked team is still alive, simulate 2 vs 6 series
        else:                                                           
            loser4.append(self.simulateMatchup([2, nl[2][1]], [6, nl[6][1]]))  
            loser4.append(self.simulateMatchup([2, nl[2][2]], [6, nl[6][2]])) 
            loser4.append(self.simulateMatchup([2, nl[2][3]], [6, nl[6][3]]))
            loser4.append(self.simulateMatchup([2, nl[2][1]], [6, nl[6][1]]))  
            loser4.append(self.simulateMatchup([2, nl[2][2]], [6, nl[6][2]])) 
        # Remove team with most losses from playoffs
        l4 = mode(loser4)
        del nl[l4]  
        
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
    

def getPitcherStrength():
    '''Function that creates a dataframe of the top 3 starting pitchers of every team 
    ordered by WAR, and the total WAR of the bullpen'''
    
    # Read file containing pitchers for each team and their WAR
    # https://www.baseball-reference.com/leagues/majors/2022-team-pitching-staffs.shtml
    df = pd.read_csv('2022TeamPitchers.txt')
    data = np.array(df)
    
    # Create dictionary for pitchers
    pitchers = {}
    
    # Create dictionary for each team 
    for i in range(len(data)):
        
        pitchers[data[i][1]] = extractWAR(data[i])
     
    return pitchers


def extractWAR(arr):
    '''Function that takes an array of team pitching data and converts the strings
    to float WAR values and returns a list of the top 3 pitchers sorted and the 
    total WAR of the bullpen'''

    # Create array for teams and pitching WARs
    pitchers = []
    numbers = re.compile(r'-*\d+\.\d{2}')

    # Get top three starting pitcher WARs
    for i in range(2, 7):
        war = numbers.findall(arr[i])
        #print(war)
        pitchers.append(float(war[0]))
    pitchers.sort(reverse = True)
    del pitchers[4]
    del pitchers[3]
    
    # Add combined bullpen WAR
    for i in range(7, 11):
        bp = []
        war = numbers.findall(arr[i])
        bp.append(float(war[0]))
    bullpen = np.array(bp)
    mb = np.mean(bullpen)
    #print(mb)
    # Combine mean of bullpen WAR with each pitcher WAR
    pitchers = pitchers + mb
    p = list(np.round(pitchers, decimals = 2))
    
    #print(pitchers + mb)

    # Add team name to beginning of list
    p.insert(0, arr[1])    

    return p    


# Create dictionary of teams and pitcher strengths 
ps = getPitcherStrength()    
ps
    
nationalLeague = {1: ps['Los Angeles Dodgers'], 2: ps['Atlanta Braves'],
                  3: ps['St. Louis Cardinals'], 4: ps['New York Mets'], 
                  5: ps['San Diego Padres'], 6: ps['Philadelphia Phillies']} 

americanLeague = {1: ps['Houston Astros'], 2: ps['New York Yankees'],
                  3: ps['Cleveland Guardians'], 4: ps['Toronto Blue Jays'],
                  5: ps['Seattle Mariners'], 6: ps['Tampa Bay Rays']} 

nationalLeague
americanLeague

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