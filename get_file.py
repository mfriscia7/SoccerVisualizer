import csv
import pickle
from enum import Enum

class Stat(Enum):

    home = 0

    goals_scored = 1
    goals_conceded = 2
    goals_scored_1st_half = 3
    goals_scored_2nd_half = 4
    goals_conceded_1st_half = 5
    goals_conceded_2nd_half = 6

    points = 7
    points_at_half = 8

    shots = 9
    opponent_shots = 10
    shots_on_target = 11
    opponent_shots_on_target = 12

    fouls = 13
    opponent_fouls = 14
    yellow_cards = 15
    opponent_yellow_cards = 16
    red_cards = 17
    opponent_red_cards = 18

    corners_taken = 19
    corners_conceded = 20

    referee = 21

def add_stats(teams, row):

    home_team = row['HomeTeam']
    away_team = row['AwayTeam']

    if not teams.has_key(home_team):
        teams[home_team] = []
    if not teams.has_key(away_team):
        teams[away_team] = []

    teams[home_team].append([
        1,  # home
        row['FTHG'],  # goals_scored
        row['FTAG'],  # goals_conceded
        row['HTHG'],  # goals_scored_1st_half
        str(int(row['FTHG']) - int(row['HTHG'])),  # goals_scored_2nd_half
        row['HTAG'],  # goals_conceded_1st_half
        str(int(row['FTAG']) - int(row['HTAG'])),  # goals_conceded_2nd_half
        3 if row['FTR'] is 'H' else 1 if row['FTR'] is 'D' else 0,  # result
        3 if row['HTR'] is 'H' else 1 if row['HTR'] is 'D' else 0,  # result_at_half
        row['HS'],  # shots_for
        row['AS'],  # shots_against
        row['HST'],  # shots_on_target
        row['AST'],  # opponent_shots_on_target_against
        row['HF'],  # fouls_committed
        row['AF'],  # opponent_fouls
        row['HY'],  # yellow_cards
        row['AY'],  # opponent_yellow_cards
        row['HR'],  # red_cards
        row['AR'],  # opponent_red_cards
        row['HC'],  # corners_taken
        row['AC'],  # corners_conceded
        'N/A' if not row.has_key('Referee') else row['Referee']  # referee
        ])


    teams[away_team].append([
        0, # home
        row['FTAG'],  # goals_scored
        row['FTHG'],  # goals_conceded
        row['HTAG'],  # goals_scored_1st_half
        str(int(row['FTAG']) - int(row['HTAG'])),  # goals_scored_2nd_half
        row['HTHG'],  # goals_conceded_1st_half
        str(int(row['FTHG']) - int(row['HTHG'])),  # goals_conceded_2nd_half
        3 if row['FTR'] is 'A' else 1 if row['FTR'] is 'D' else 0,  # result
        3 if row['HTR'] is 'A' else 1 if row['HTR'] is 'D' else 0,  # result_at_half
        row['AS'],  # shots_for
        row['HS'],  # shots_against
        row['AST'],  # shots_on_target
        row['HST'],  # opponent_shots_on_target_against
        row['AF'],  # fouls_committed
        row['HF'],  # opponent_fouls
        row['AY'],  # yellow_cards
        row['HY'],  # opponent_yellow_cards
        row['AR'],  # red_cards
        row['HR'],  # opponent_red_cards
        row['AC'],  # corners_taken
        row['HC'],  # corners_conceded
        'N/A' if not row.has_key('Referee') else row['Referee']  # referee
    ])

file_ext = ['EPL', 'Ligue1', 'Bundesliga', 'SerieA', 'LaLiga']
seasons = []

for ext in file_ext:
    if ext == 'EPL':
        season = [{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
        file_name = ['_02-03.csv', '_03-04.csv', '_04-05.csv','_05-06.csv', '_06-07.csv', '_07-08.csv',
             '_08-09.csv', '_09-10.csv','_10-11.csv','_11-12.csv',
             '_12-13.csv', '_13-14.csv', '_14-15.csv', '_15-16.csv']
    elif ext == 'Ligue1':
        season = [{},{},{},{},{},{},{},{},{}]
        file_name = ['_07-08.csv',
             '_08-09.csv','_09-10.csv','_10-11.csv','_11-12.csv',
             '_12-13.csv','_13-14.csv','_14-15.csv','_15-16.csv']
    elif ext == 'Bundesliga' or ext == 'SerieA':
        season = [{},{},{},{},{},{},{},{},{},{}]
        file_name = ['_06-07.csv','_07-08.csv',
             '_08-09.csv','_09-10.csv','_10-11.csv','_11-12.csv',
             '_12-13.csv','_13-14.csv','_14-15.csv','_15-16.csv']
    else:
        season = [{},{},{},{},{},{},{},{},{},{},{}]
        file_name = ['_05-06.csv','_06-07.csv','_07-08.csv',
             '_08-09.csv','_09-10.csv','_10-11.csv','_11-12.csv',
             '_12-13.csv','_13-14.csv','_14-15.csv','_15-16.csv']

    for arr, filename in zip(season, file_name):
        with open(ext + '/' + ext.lower() + filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                add_stats(arr, row)

    seasons.append(season)

#  print seasons[0][-1]['Tottenham'][7][Stat.goals_conceded_half]
f = open("stats_full", 'wb')
pickle.dump(seasons, f)
f.close()

