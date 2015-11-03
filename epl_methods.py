import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from io import BytesIO
import base64
from PIL import Image

stat_dict = {'home': 0, 'goals_scored': 1, 'goals_conceded': 2, 'goals_scored_1st_half': 3, 'goals_scored_2nd_half': 4,
    'goals_conceded_1st_half': 5, 'goals_conceded_2nd_half': 6, 'points': 7, 'points_at_half': 8, 'shots': 9,
    'shots_on_target': 10, 'opponent_shots': 11, 'opponent_shots_on_target': 12, 'fouls': 13,
    'opponent_fouls': 14, 'yellow_cards': 15, 'opponent_yellow_cards': 16, 'red_cards': 17, 'pponent_red_cards': 18,
    'corners_taken': 19, 'corners_conceded': 20, 'referee': 21}



def per(data1, data2):
    to_return = {}
    for num in data1:
        if (data2[num] == 0):
            to_return[num] = data1[num] / 1
        else:
            to_return[num] = data1[num] / data2[num]
    return to_return


def get_stat(season, games, stat, is_per_game):
    data = {}
    for team in season.iteritems():
        data[team[0]] = 0

        for game in games:
            data[team[0]] += float(season[team[0]][game][stat])

    if is_per_game == 'true':
        data = per_game(data, games)

    return data


def per_game(data, games):
    for index in data:
        data[index] /= len(games)
    return data


def plot_from_dict(x, y, teams_excluded, x_text, y_text, per_game):
    assert len(x) == len(y)
    _x = []
    _y = []
    x_labels = []
    y_labels = []
    im_array = []

    for key, value in x.iteritems():
        if key not in teams_excluded:
            _x.append(value)
            _y.append(y[key])
            x_labels.append(key)
            y_labels.append(key)
            im_array.append(Image.open('crests/' + key + '.png'))

    fig, ax = plt.subplots()
    ax.scatter(_x, _y)

    plt.grid(b=True, which='both', color='0.65', linestyle='-')

    if per_game == 'false':
        plt.ylabel(y_text)
        plt.xlabel(x_text)
    else:
        plt.ylabel(y_text + ' / game')
        plt.xlabel(x_text + ' / game')

    #for label, x1, y1 in zip(x_labels, _x, _y):
    #    ax.annotate(label, fontsize='8', xy=(x1, y1), xytext=(-10, -10), textcoords='offset points')

    for im in zip(_x, _y, im_array):
        ax.add_artist(AnnotationBbox(OffsetImage(im[2], zoom=0.5),[im[0],im[1]],xybox=(0.,0.), xycoords='data',boxcoords='offset points', frameon=False))

    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    to_return = base64.b64encode(imgdata.getvalue())
    imgdata.close()
    plt.clf()
    return to_return
