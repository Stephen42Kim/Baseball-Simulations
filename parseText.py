# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 00:19:29 2023

@author: Stephen
"""

def parseTextFile(file) -> dict:

    gameLog = {}

    with open(file, 'r') as infile:
        gameNum = 1
        for line in infile:
            info = line.split(',')

            vScore = int(info[9])
            hScore = int(info[10])
            vTeam = info[3].strip('\"')
            hTeam = info[6].strip('\"')

            gameLog[gameNum] = {
                'Home': {
                    'Score': hScore,
                    'Team': hTeam
                },
                'Away': {
                    'Score': vScore,
                    'Team': vTeam
                }
            }

            gameNum += 1

    return gameLog



def main():
    testFile = 'stats-2022.txt'
    parsedText = parseTextFile(testFile)
    #print(parseTextFile[1])

    # 9 -> visting team score
    # 10 -> home team score
    # 3 -> visiting team name
    # 6 -> Home team

if __name__ == '__main__':
    main()