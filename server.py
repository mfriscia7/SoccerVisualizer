from flask import Flask, render_template, request
from epl_methods import *
import os
import pickle
import json
import sys, logging

'''
Stats:
home
goals_scored
goals_conceded
goals_scored_1st_half
goals_scored_2nd_half
goals_conceded_1st_half
goals_conceded_2nd_half
points
points_at_half
shots
opponent_shots
shots_on_target
opponent_shots_on_target
fouls
opponent_fouls
yellow_cards
opponent_yellow_cards
red_cards
opponent_red_cards
corners_taken
corners_conceded
referee
'''

#  seasons[league][season number]['Team Name'][Game Number][Stat.stat]



app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

#f = file('epl_full', 'rb')
#seasons = pickle.load(f)
#f.close()

#games = [0,1,2,3,4,5,6,7]
#data = get_stat(seasons[11], games, Stat.opponent_shots_on_target, "false")
#data1 = get_stat(seasons[11], games, Stat.goals_conceded, "false")

#data = plot_from_dict(data, data1, [])
f = file('stats_full', 'rb')
seasons = pickle.load(f)
f.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_teams/', methods=['POST'])
def get_teams():
    to_return = []
    league = int(request.form['league'])
    season = int(request.form['season'])
    for key in seasons[league][season].iteritems():
        to_return.append(key[0])
    to_return.sort()
    # add season len on end
    to_return.append(len(seasons[league][season][seasons[league][season].iteritems().next()[0]]))
    return ','.join(str(v) for v in to_return)

@app.route('/make_graph/', methods=['POST', 'GET'])
def make_graph():
    x_data = json.loads(request.form['x_data'])
    y_data = json.loads(request.form['y_data'])
    season_num = int(request.form['season_num'])
    season_start = int(request.form['season_start']) - 1
    league = int(request.form['league'])
    season_len = min([len(v) for v in seasons[league][season_num].values()]) - 1
    img_array = []
    teams_excluded = json.loads(request.form['teams_excluded'])
    is_per_game = request.form['per_game']
    x_text = request.form['x_text']
    y_text = request.form['y_text']

    x_final = []
    y_final = []

    # x data
    for j in range(season_start, season_len+1):
        to_append = get_stat(seasons[league][season_num], range(season_start, j+1),  stat_dict[x_data[0].lower().replace(' ', '_')], str(is_per_game))
        for statistic in x_data[1:]:
            to_append = per(to_append, get_stat(seasons[league][season_num], range(season_start, j),  stat_dict[statistic.lower().replace(' ', '_')], str(is_per_game)))
        x_final.append(to_append)

    # y data
    for j in range(season_start, season_len+1):
        to_append = get_stat(seasons[league][season_num], range(season_start, j+1),  stat_dict[y_data[0].lower().replace(' ', '_')], str(is_per_game))
        for statistic in y_data[1:]:
            to_append = per(to_append, get_stat(seasons[league][season_num], range(season_start, j+1),  stat_dict[statistic.lower().replace(' ', '_')], str(is_per_game)))
        y_final.append(to_append)

    for x, y in zip(x_final, y_final):
        img_array.append(plot_from_dict(x, y, teams_excluded, x_text, y_text, str(is_per_game)))

    return json.dumps(img_array)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)