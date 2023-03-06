# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 04:12:26 2023

@author: Stephen Kim

Note: Do not use function addTeamWins more than once. Otherwise teams wins columns
will be added.



"""


from collections import Counter
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
           
    
    def simulateMatchup(self, teamA, teamB,):
        '''Function that takes two lists as parameters, one representing each team.
        
        *** Home team is teamA, Away team is teamB ***
        
        First element in list is the team seeding.
        Second element in list is a list containing team name and distribution.
        
        Calculate the winner using ratio of strength values and home/away split.
        
        Home team win percentage is 55%, while away team win percentage is 46%
        https://plus.fangraphs.com/does-home-field-matter-in-the-playoffs/
        
        Returns the losing team seed.'''
        
        random = np.random.uniform(0,1)             # Get random num between 0 and 1
        
        adv = ((teamA[1] + teamB[1])/100) * 5       # Home field advantage is 4% of total power in game
        
        A = teamA[1] + adv                          # Add home field advantage 
        B = teamB[1] - adv                          # Subtract away team disadvantage

        winRatio = A/(A + B)                        # Get odds of winning for home team
        
        if random > winRatio:                       # If random num is greater than winRatio
            return teamA[0], teamA[2]               # Return seed and team name of loser
        else:                                       
            return teamB[0], teamB[2]                         
    
    
    def simulatePlayoffs(self):
        '''Function that simulates each round of the 2022 playoff scenario and returns the World
        Series champion'''
        
        nl = self.nl.copy()
        al = self.al.copy()
        
        nl2, al2 = self.wildCard(nl, al)                     # Simulate wild card round
        nl3, al3 = self.divisionSeries(nl2, al2)             # Simulate divisional series round
        nl4, al4 = self.championshipSeries(nl3, al3)         # Simulate league championship round
        champ = self.worldSeries(nl4, al4)                   # Simulate world series
      
        return champ
    
    
    def runSimulation(self, trials = 1000000):
        '''Function that runs the playoff scenario default 1,000,000 times.
        Tracks the world series winners and plot results'''
        
        championData = []
        teamChamps = []

        for i in range(trials):
            championData.append(self.simulatePlayoffs())
            #teamChamps.append(championData[i][1])
        
        df = pd.DataFrame({'Team':championData})
        self.plotResults(championData, trials)
        
        wins = df['Team'].value_counts()
        self.printResults(wins, trials)
                        
        return championData
    
    
    def plotResults(self, championData, trials):
        '''Function that plots the results in a bargraph'''
        
        df = pd.DataFrame({'Team':championData})
        team = []
        pct = []
        for idx, x in df['Team'].value_counts().items():
            
            pct.append(round((x/trials) * 100, 2))
            team.append(idx)
        
        plt.figure(figsize = (10,5))

        plt.bar(team, pct, color = 'green')
     
  
        self.addlabels(team, pct)
     
        plt.xticks(rotation = 60)
        plt.title('Odds of Winning the World Series 2022 Edition - Pitcher WAR')
        plt.xlabel("Teams")
        plt.ylabel("Win Percentage")
        plt.show()
        
    xy = []
    # function to add value labels
    def addlabels(self, x,y):
        for i in range(len(x)):
            plt.text(i, y[i]//2,y[i], ha = 'center',
                     bbox = dict(boxstyle = 'sawtooth', facecolor = 'yellow', alpha = .6))
    
    
    def printResults(self, wins, trials):
        '''Function to print results'''
        
        print('2022 MLB Playoff Scenario Simulation: {} Trials'.format(trials))
        print()
        
        for idx, x in wins.items():
            print('Team: {:^22s}     World Series Win %: {:.2f}'.format(idx, (x/trials) * 100))
              
        
        return
                  
    
    def wildCard(self, nl, al):
        '''Function that takes a two dictionaries (one for each league) and
        eliminates wild card round losers.
        Higher seeded team has home team advantage for each game.'''
                
        # American League 3/6 matchup
        # Simulate each game with rotating pitcher and track losing team
        loser1 = []
        loser1.append(self.simulateMatchup([3, al[3][1], al[3][0]], [6, al[6][1], al[6][0]])[0])  
        loser1.append(self.simulateMatchup([3, al[3][2], al[3][0]], [6, al[6][2], al[6][0]])[0]) 
        loser1.append(self.simulateMatchup([3, al[3][3], al[3][0]], [6, al[6][3], al[6][0]])[0])
        
        # Remove the team that has lost the most (Lost best of 3)
        l1 = mode(loser1)
        del al[l1]
                 
        
        # American League 4/5 matchup
        loser2 = []
        loser2.append(self.simulateMatchup([4, al[4][1], al[4][0]], [5, al[5][1], al[5][0]])[0])  
        loser2.append(self.simulateMatchup([4, al[4][2], al[4][0]], [5, al[5][2], al[5][0]])[0]) 
        loser2.append(self.simulateMatchup([4, al[4][3], al[4][0]], [5, al[5][3], al[5][0]])[0])
        l2 = mode(loser2)
        del al[l2]
        
        # National League 3/6 matchup
        loser3 = []
        loser3.append(self.simulateMatchup([3, nl[3][1], nl[3][0]], [6, nl[6][1], nl[6][0]])[0])  
        loser3.append(self.simulateMatchup([3, nl[3][2], nl[3][0]], [6, nl[6][2], nl[6][0]])[0]) 
        loser3.append(self.simulateMatchup([3, nl[3][3], nl[3][0]], [6, nl[6][3], nl[6][0]])[0])
        l3 = mode(loser3)
        del nl[l3]
        
        # National League 4/5 matchup
        loser4 = []
        loser4.append(self.simulateMatchup([4, nl[4][1], nl[4][0]], [5, nl[5][1], nl[5][0]])[0])  
        loser4.append(self.simulateMatchup([4, nl[4][2], nl[4][0]], [5, nl[5][2], nl[5][0]])[0]) 
        loser4.append(self.simulateMatchup([4, nl[4][3], nl[4][0]], [5, nl[5][3], nl[5][0]])[0])
        l4 = mode(loser4)
        del nl[l4]
        
        return nl, al
        
        
    def divisionSeries(self, nl, al):
        '''Function that returns the divional round winners in a best of 5 series.
        Higher seed plays home twice, then away twice, then home again if needed.
        Return two dictionaries of the teams left standing in each league'''
        
        # American League 1 vs 4/5 matchup
        loser1 = []
        
        # If 4th ranked team is still alive, simulate 1 vs 4 series
        if 4 in al:                                                     
            loser1.append(self.simulateMatchup([1, al[1][1], al[1][0]], [4, al[4][1], al[4][0]])[0])  
            loser1.append(self.simulateMatchup([1, al[1][2], al[1][0]], [4, al[4][2], al[4][0]])[0]) 
            loser1.append(self.simulateMatchup([4, al[4][3], al[4][0]], [1, al[1][3], al[1][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser1) == 3:
                l1 = mode(loser1)
                del al[l1]
            # Else play game 4
            else:
                loser1.append(self.simulateMatchup([4, al[4][1], al[4][0]], [1, al[1][1], al[1][0]])[0])
                
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser1) == 3:
                    l1 = mode(loser1)
                    del al[l1]
                # Else play game 5
                else:
                    loser1.append(self.simulateMatchup([1, al[1][2], al[1][0]], [4, al[4][2], al[4][0]])[0])
                    l1 = mode(loser1)
                    del al[l1]
        
        # Else if 5th ranked team is still alive, simulate 1 vs 5 series
        else:                                                           
            loser1.append(self.simulateMatchup([1, al[1][1], al[1][0]], [5, al[5][1], al[5][0]])[0])  
            loser1.append(self.simulateMatchup([1, al[1][2], al[1][0]], [5, al[5][2], al[5][0]])[0]) 
            loser1.append(self.simulateMatchup([5, al[5][3], al[5][0]], [1, al[1][3], al[1][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser1) == 3:
                l1 = mode(loser1)
                del al[l1]
            # Else play game 4
            else:
                loser1.append(self.simulateMatchup([5, al[5][1], al[5][0]], [1, al[1][1], al[1][0]])[0])  
                
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser1) == 3:
                    l1 = mode(loser1)
                    del al[l1]
                # Else play game 5
                else:
                    loser1.append(self.simulateMatchup([1, al[1][2], al[1][0]], [5, al[5][2], al[5][0]])[0]) 
                    l1 = mode(loser1)
                    del al[l1]                       
        
        # American League 2 vs 3/6 matchup
        loser2 = []
        
        # If 3th ranked team is still alive, simulate 2 vs 3 series
        if 3 in al:                                                     
            loser2.append(self.simulateMatchup([2, al[2][1], al[2][0]], [3, al[3][1], al[3][0]])[0])  
            loser2.append(self.simulateMatchup([2, al[2][2], al[2][0]], [3, al[3][2], al[3][0]])[0]) 
            loser2.append(self.simulateMatchup([3, al[3][3], al[3][0]], [2, al[2][3], al[2][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser2) == 3:
                l2 = mode(loser2)
                del al[l2]
            # Else play game 4
            else:
                loser2.append(self.simulateMatchup([3, al[3][1], al[3][0]], [2, al[2][1], al[2][0]])[0])  
                
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser2) == 3:
                    l2 = mode(loser2)
                    del al[l2]
                # Else play game 5
                else:
                    loser2.append(self.simulateMatchup([2, al[2][2], al[2][0]], [3, al[3][2], al[3][0]])[0]) 
                    l2 = mode(loser2)
                    del al[l2]
                    
        # Else if 6thth ranked team is still alive, simulate 2 vs 6 series
        else:                                                           
            loser2.append(self.simulateMatchup([2, al[2][1], al[2][0]], [6, al[6][1], al[6][0]])[0])  
            loser2.append(self.simulateMatchup([2, al[2][2], al[2][0]], [6, al[6][2], al[6][0]])[0]) 
            loser2.append(self.simulateMatchup([6, al[6][3], al[6][0]], [2, al[2][3], al[2][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser2) == 3:
                l2 = mode(loser2)
                del al[l2]
            # Else play game 4
            else:
                loser2.append(self.simulateMatchup([6, al[6][1], al[6][0]], [2, al[2][1], al[2][0]])[0])  
            
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser2) == 3:
                    l2 = mode(loser2)
                    del al[l2]
                # Else play game 5
                else:
                    loser2.append(self.simulateMatchup([2, al[2][2], al[2][0]], [6, al[6][2], al[6][0]])[0]) 
                    l2 = mode(loser2)
                    del al[l2]
                    
        
        # National League 1 vs 4/5 matchup
        loser3 = []
        
        # If 4th ranked team is still alive, simulate 1 vs 4 series
        if 4 in nl:                                                     
            loser3.append(self.simulateMatchup([1, nl[1][1], nl[1][0]], [4, nl[4][1], nl[4][0]])[0])  
            loser3.append(self.simulateMatchup([1, nl[1][2], nl[1][0]], [4, nl[4][2], nl[4][0]])[0]) 
            loser3.append(self.simulateMatchup([4, nl[4][3], nl[4][0]], [1, nl[1][3], nl[1][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser3) == 3:
                l3 = mode(loser3)
                del nl[l3]
            # Else play game 4
            else:
                loser3.append(self.simulateMatchup([4, nl[4][1], nl[4][0]], [1, nl[1][1], nl[1][0]])[0])  
            
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser3) == 3:
                    l3 = mode(loser3)
                    del nl[l3]
                # Else play game 5
                else:
                    loser3.append(self.simulateMatchup([1, nl[1][2], nl[1][0]], [4, nl[4][2], nl[4][0]])[0]) 
                    l3 = mode(loser3)
                    del nl[l3]
                
        # Else if 5th ranked team is still alive, simulate 1 vs 5 series
        else:                                                           
            loser3.append(self.simulateMatchup([1, nl[1][1], nl[1][0]], [5, nl[5][1], nl[5][0]])[0])  
            loser3.append(self.simulateMatchup([1, nl[1][2], nl[1][0]], [5, nl[5][2], nl[5][0]])[0]) 
            loser3.append(self.simulateMatchup([5, nl[5][3], nl[5][0]], [1, nl[1][3], nl[1][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser3) == 3:
                l3 = mode(loser3)
                del nl[l3]
            # Else play game 4
            else:
                loser3.append(self.simulateMatchup([5, nl[5][1], nl[5][0]], [1, nl[1][1], nl[1][0]])[0])  
            
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser3) == 3:
                    l3 = mode(loser3)
                    del nl[l3]
                # Else play game 5
                else:
                    loser3.append(self.simulateMatchup([1, nl[1][2], nl[1][0]], [5, nl[5][2], nl[5][0]])[0]) 
                    l3 = mode(loser3)
                    del nl[l3]
                    
        
        # National League 2 vs 3/6 matchup
        loser4 = []
        
        # If 3th ranked team is still alive, simulate 2 vs 3 series
        if 3 in nl:                                                     
            loser4.append(self.simulateMatchup([2, nl[2][1], nl[2][0]], [3, nl[3][1], nl[3][0]])[0])  
            loser4.append(self.simulateMatchup([2, nl[2][2], nl[2][0]], [3, nl[3][2], nl[3][0]])[0]) 
            loser4.append(self.simulateMatchup([3, nl[3][3], nl[3][0]], [2, nl[2][3], nl[2][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser4) == 3:
                l4 = mode(loser4)
                del nl[l4]
            # Else play game 4
            else:
                loser4.append(self.simulateMatchup([3, nl[3][1], nl[3][0]], [2, nl[2][1], nl[2][0]])[0])  
            
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser4) == 3:
                    l4 = mode(loser4)
                    del nl[l4]
                # Else play game 5
                else:
                    loser4.append(self.simulateMatchup([2, nl[2][2], nl[2][0]], [3, nl[3][2], nl[3][0]])[0]) 
                    l4 = mode(loser4)
                    del nl[l4]
        
        # Else if 6th ranked team is still alive, simulate 2 vs 6 series
        else:                                                           
            loser4.append(self.simulateMatchup([2, nl[2][1], nl[2][0]], [6, nl[6][1], nl[6][0]])[0])  
            loser4.append(self.simulateMatchup([2, nl[2][2], nl[2][0]], [6, nl[6][2], nl[6][0]])[0]) 
            loser4.append(self.simulateMatchup([6, nl[6][3], nl[6][0]], [2, nl[2][3], nl[2][0]])[0])
            
            # If one team reaches three losses, they are eliminated
            if self.checkSeries(loser4) == 3:
                l4 = mode(loser4)
                del nl[l4]
            # Else play game 4
            else:
                loser4.append(self.simulateMatchup([6, nl[6][1], nl[6][0]], [2, nl[2][1], nl[2][0]])[0])  
            
                # If one team reaches three losses they are eliminated
                if self.checkSeries(loser4) == 3:
                    l4 = mode(loser4)
                    del nl[l4]
                # Else play game 5
                else:
                    loser4.append(self.simulateMatchup([2, nl[2][2], nl[2][0]], [6, nl[6][2], nl[6][0]])[0]) 
                    l4 = mode(loser4)
                    del nl[l4]
        
        return nl, al
    
    
    def championshipSeries(self, nl, al):
        '''Function that returns the league championship winners 2-3-2 series.'''
        
        # American League Finals matchup
        # Get seedings of two AL teams still alive
        hi1 = min(al)
        low1 = max(al)
        
        loser1 = []
        
        # Simulate best of 7 series, track loser of each game, and remove loser                                                   
        loser1.append(self.simulateMatchup([hi1, al[hi1][1], al[hi1][0]], [low1, al[low1][1], al[low1][0]])[0])  
        loser1.append(self.simulateMatchup([hi1, al[hi1][2], al[hi1][0]], [low1, al[low1][2], al[low1][0]])[0]) 
        loser1.append(self.simulateMatchup([low1, al[low1][3], al[low1][0]], [hi1, al[hi1][3], al[hi1][0]])[0])
        loser1.append(self.simulateMatchup([low1, al[low1][1], al[low1][0]], [hi1, al[hi1][1], al[hi1][0]])[0])
        
        # If one team reaches four losses, they are eliminated
        if self.checkSeries(loser1) == 4:
            l1 = mode(loser1)
            del al[l1]
        # Else play game 4
        else:
            loser1.append(self.simulateMatchup([low1, al[low1][2], al[low1][0]], [hi1, al[hi1][2], al[hi1][0]])[0])
            
            # If one team reaches four losses, they are eliminated
            if self.checkSeries(loser1) == 4:
                l1 = mode(loser1)
                del al[l1]
            # Else play game 4
            else:
                loser1.append(self.simulateMatchup([hi1, al[hi1][3], al[hi1][0]], [low1, al[low1][3], al[low1][0]])[0])
                
                # If one team reaches four losses, they are eliminated
                if self.checkSeries(loser1) == 4:
                    l1 = mode(loser1)
                    del al[l1]
                # Else play game 4
                else:
                    loser1.append(self.simulateMatchup([hi1, al[hi1][1], al[hi1][0]], [low1, al[low1][1], al[low1][0]])[0])  
                    l1 = mode(loser1)
                    del al[l1]
                                           
            
        # National League matchup
        # Get seedings of two AL teams still alive
        hi2 = min(nl)
        low2 = max(nl)

        loser2 = []
        
        # Simulate best of 7 series, track loser of each game, and remove loser                                                   
        loser2.append(self.simulateMatchup([hi2, nl[hi2][1], nl[hi2][0]], [low2, nl[low2][1], nl[low2][0]])[0])  
        loser2.append(self.simulateMatchup([hi2, nl[hi2][2], nl[hi2][0]], [low2, nl[low2][2], nl[low2][0]])[0]) 
        loser2.append(self.simulateMatchup([low2, nl[low2][3], nl[low2][0]], [hi2, nl[hi2][3], nl[hi2][0]])[0])
        loser2.append(self.simulateMatchup([low2, nl[low2][1], nl[low2][0]], [hi2, nl[hi2][1], nl[hi2][0]])[0])
       
        # If one team reaches four losses, they are eliminated
        if self.checkSeries(loser2) == 4:
            l2 = mode(loser2)
            del nl[l2]
        # Else play game 4
        else:
            loser2.append(self.simulateMatchup([low2, nl[low2][2], nl[low2][0]], [hi2, nl[hi2][2], nl[hi2][0]])[0])
        
            # If one team reaches four losses, they are eliminated
            if self.checkSeries(loser2) == 4:
                l2 = mode(loser2)
                del nl[l2]
            # Else play game 4
            else:
                loser2.append(self.simulateMatchup([hi2, nl[hi2][3], nl[hi2][0]], [low2, nl[low2][3], nl[low2][0]])[0])
        
                # If one team reaches four losses, they are eliminated
                if self.checkSeries(loser2) == 4:
                    l2 = mode(loser2)
                    del nl[l2]
                # Else play game 4
                else:
                    loser2.append(self.simulateMatchup([hi2, nl[hi2][1], nl[hi2][0]], [low2, nl[low2][1], nl[low2][0]])[0])  
                    l2 = mode(loser2)
                    del nl[l2]
                    
        return nl, al
        
    
    def worldSeries(self, nl, al):     
        '''Function that returns the world series champion'''
        
        a = list(al.keys())[0]       # Get AL team key
        n = list(nl.keys())[0]       # Get NL team key
        teams = [nl[n][0], al[a][0]]
        loser = []
        
        # If NL team had more regular wins, they are home team
        if nl[n][4] > al[a][4]:
            loser.append(self.simulateMatchup([n, nl[n][1], nl[n][0]], [a, al[a][1], al[a][0]])[1])  
            loser.append(self.simulateMatchup([n, nl[n][2], nl[n][0]], [a, al[a][2], al[a][0]])[1]) 
            loser.append(self.simulateMatchup([a, al[a][3], al[a][0]], [n, nl[n][3], nl[n][0]])[1])
            loser.append(self.simulateMatchup([a, al[a][1], al[a][0]], [n, nl[n][1], nl[n][0]])[1])
            
            # If one team reaches four losses, they are eliminated
            if self.checkSeries(loser) == 4:
                l = mode(loser)
                teams.remove(l)
                return teams[0]
            # Else play game 4
            else:
                loser.append(self.simulateMatchup([a, al[a][2], al[a][0]], [n, nl[n][2], nl[n][0]])[1])
                
                # If one team reaches four losses, they are eliminated
                if self.checkSeries(loser) == 4:
                    l = mode(loser)
                    teams.remove(l)
                    return teams[0]
                # Else play game 4
                else:
                    loser.append(self.simulateMatchup([n, nl[n][3], nl[n][0]], [a, al[a][3], al[a][0]])[1])
                    # If one team reaches four losses, they are eliminated
                    if self.checkSeries(loser) == 4:
                        l = mode(loser)
                        teams.remove(l)
                        return teams[0]
                    # Else play game 4
                    else:
                        loser.append(self.simulateMatchup([n, nl[n][1], nl[n][0]], [a, al[a][1], al[a][0]])[1])
                        l = mode(loser)
                        teams.remove(l)
                        return teams[0]

            
        # Else if AL team had more regular wins, they are home team
        else:
            loser.append(self.simulateMatchup([a, al[a][1], al[a][0]], [n, nl[n][1], nl[n][0]])[1])  
            loser.append(self.simulateMatchup([a, al[a][2], al[a][0]], [n, nl[n][2], nl[n][0]])[1]) 
            loser.append(self.simulateMatchup([n, nl[n][3], nl[n][0]], [a, al[a][3], al[a][0]])[1])
            loser.append(self.simulateMatchup([n, nl[n][1], nl[n][0]], [a, al[a][1], al[a][0]])[1])
            
            # If one team reaches four losses, they are eliminated
            if self.checkSeries(loser) == 4:
                l = mode(loser)
                teams.remove(l)
                return teams[0]
            # Else play game 4
            else:
                loser.append(self.simulateMatchup([n, nl[n][2], nl[n][0]], [a, al[a][2], al[a][0]])[1])
            
                # If one team reaches four losses, they are eliminated
                if self.checkSeries(loser) == 4:
                    l = mode(loser)
                    teams.remove(l)
                    return teams[0]
                # Else play game 4
                else:
                    loser.append(self.simulateMatchup([a, al[a][3], al[a][0]], [n, nl[n][3], nl[n][0]])[1])
            
                    # If one team reaches four losses, they are eliminated
                    if self.checkSeries(loser) == 4:
                        l = mode(loser)
                        teams.remove(l)
                        return teams[0]
                    # Else play game 4
                    else:
                        loser.append(self.simulateMatchup([a, al[a][1], al[a][0]], [n, nl[n][1], nl[n][0]])[1])              
                        l = mode(loser)
                        teams.remove(l)
                        return teams[0]
                        
    
    
    def checkSeries(self, arr):
        '''Function that takes array as parameter and returns count of the mode'''
            
        data = Counter(arr)               # Create counter object with array
        
        return data.most_common(1)[0][1]  # Returns the highest occurring item
    
    
def getPitcherStrength():
    '''Function that creates a dataframe of the team names, top 3 starting pitchers of every team 
    ordered by WAR, and the total WAR of the bullpen, and the team regular season wins'''
    
    

def getPitcherStrength():
    '''Function that creates a dataframe of the top 3 starting pitchers of every team 
    ordered by WAR, and the total WAR of the bullpen'''
    
    # Read file containing pitchers for each team and their WAR
    # https://www.baseball-reference.com/leagues/majors/2022-team-pitching-staffs.shtml
    df = pd.read_csv('2022TeamPitchers.txt')
    data = np.array(df)
    
    # Create dictionary for team pitcher strengths
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
    
    # Get rid of names and parenthesis
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
    
    # Add team win total to end of list
    #p.append(arr[-1])

    return p

def addTeamWins(teamDict):
    '''Function that adds regular season win totals to dictionary of teams'''

    df = pd.read_csv('2022TeamWins.txt')
    data = np.array(df)
    
    for i in data:
        teamDict[i[0]].append(i[1])
        
    return teamDict


# Create dictionary of teams, team wins, and pitcher strengths 
ps = getPitcherStrength()    
ps

# Add regular season wins to each team
d = addTeamWins(ps)
d    
    
# Recreate 2022 Postseason brackets
nationalLeague = {1: ps['Los Angeles Dodgers'], 2: ps['Atlanta Braves'],
                  3: ps['St. Louis Cardinals'], 4: ps['New York Mets'], 
                  5: ps['San Diego Padres'], 6: ps['Philadelphia Phillies']} 

americanLeague = {1: ps['Houston Astros'], 2: ps['New York Yankees'],
                  3: ps['Cleveland Guardians'], 4: ps['Toronto Blue Jays'],
                  5: ps['Seattle Mariners'], 6: ps['Tampa Bay Rays']} 

nationalLeague
americanLeague

# Create baseball simulation object and run simulation, tracking time
b = Baseball(nationalLeague, americanLeague)
start_time = time.time()
results = b.runSimulation(1000000)
print()
print("Unbatched: %s seconds" % (time.time() - start_time))






