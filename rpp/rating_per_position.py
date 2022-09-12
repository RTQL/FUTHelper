import json
import sqlite3
from coefficients import *
from chemistry_styles import styles
import re
from timeit import default_timer as timer

# db = {
#     '93ST_Pépé_959189934882': {'guid': '93ST_Pépé_959189934882', 'futbin_id': '25940', 'overall': '93', 'card_name': 'Pépé', 'position': 'ST', 'card_type': 'shapeshifter', 'card_level': 'gold', 'card_rarity': 'special', 'traits': 'Technical Dribbler (CPU AI),Speed Dribbler (CPU AI),Long Shot Taker (CPU AI),Flair,Finesse Shot', 'name': 'nicolas pépé', 'club': 'arsenal', 'nation': "côte d'ivoire", 'league': 'premier league', 'skills': '4', 'weak_foot': '4', 'intl_rep': '2', 'foot': 'left', 'height': '183', 'weight': '73', 'revision': 'shapeshifters obj', 'att_wr': 'high', 'def_wr': 'low', 'added_on': '2022-06-17', 'origin': 'n\\a', 'rface': '', 'btype': 'unique', 'age': '27 years old', 'id': '226110', 'club_id': '1', 'league_id': '13', '_pace': '95', '_shooting': '91', '_passing': '89', '_dribbling': '93', '_defending': '48', '_physicality': '82', 'acceleration': '95', 'sprint_speed': '95', 'positioning': '90', 'finishing': '91', 'shot_power': '93', 'long_shots': '90', 'volleys': '81', 'penalties': '98', 'vision': '90', 'crossing': '90', 'fk_accuracy': '93', 'short_passing': '90', 'long_passing': '80', 'curve': '95', 'agility': '95', 'balance': '92', 'reactions': '88', 'ball_control': '91', 'dribbling': '95', 'composure': '88', 'interceptions': '44', 'heading_accuracy': '76', 'def_awareness': '48', 'standing_tackle': '45', 'sliding_tackle': '40', 'jumping': '82', 'stamina': '95', 'strength': '85', 'aggression': '60'},
#     '96CB_Diego Carlos_915782859798': {'guid': '96CB_Diego Carlos_915782859798', 'futbin_id': '28020', 'overall': '96', 'card_name': 'Diego Carlos', 'position': 'CB', 'card_type': 'f_moment', 'card_level': 'gold', 'card_rarity': 'special', 'traits': 'Long Passer (CPU AI),Solid Player', 'name': 'diego carlos santos silva', 'club': 'aston villa', 'nation': 'brazil', 'league': 'premier league', 'skills': '3', 'weak_foot': '4', 'intl_rep': '2', 'foot': 'right', 'height': '185', 'weight': '86', 'revision': 'player moments sbc', 'att_wr': 'med', 'def_wr': 'high', 'added_on': '2022-08-29', 'origin': 'n\\a', 'rface': '', 'btype': 'high & stocky', 'age': '29 years old', 'id': '219693', 'club_id': '2', 'league_id': '13', '_pace': '91', '_shooting': '57', '_passing': '82', '_dribbling': '85', '_defending': '97', '_physicality': '98', 'acceleration': '92', 'sprint_speed': '90', 'positioning': '63', 'finishing': '39', 'shot_power': '89', 'long_shots': '69', 'volleys': '41', 'penalties': '50', 'vision': '82', 'crossing': '48', 'fk_accuracy': '91', 'short_passing': '98', 'long_passing': '95', 'curve': '60', 'agility': '84', 'balance': '86', 'reactions': '98', 'ball_control': '88', 'dribbling': '80', 'composure': '93', 'interceptions': '98', 'heading_accuracy': '94', 'def_awareness': '98', 'standing_tackle': '97', 'sliding_tackle': '96', 'jumping': '98', 'stamina': '96', 'strength': '99', 'aggression': '98'},
#     '99LW_Ronaldo_999990975092': {'guid': '99LW_Ronaldo_999990975092', 'futbin_id': '25960', 'overall': '99', 'card_name': 'Ronaldo', 'position': 'LW', 'card_type': 'shapeshifter', 'card_level': 'gold', 'card_rarity': 'special', 'traits': 'Outside Foot Shot,Speed Dribbler (CPU AI),Long Shot Taker (CPU AI),Flair,Power Free-Kick,Set Play Specialist', 'name': 'c. ronaldo dos santos aveiro', 'club': 'manchester utd', 'nation': 'portugal', 'league': 'premier league', 'skills': '5', 'weak_foot': '4', 'intl_rep': '5', 'foot': 'right', 'height': '187', 'weight': '83', 'revision': 'shapeshifters', 'att_wr': 'high', 'def_wr': 'low', 'added_on': '2022-06-24', 'origin': 'shapeshifters2', 'rface': '', 'btype': 'cr7', 'age': '37 years old', 'id': '20801', 'club_id': '11', 'league_id': '13', '_pace': '99', '_shooting': '99', '_passing': '90', '_dribbling': '97', '_defending': '50', '_physicality': '92', 'acceleration': '99', 'sprint_speed': '99', 'positioning': '99', 'finishing': '99', 'shot_power': '99', 'long_shots': '99', 'volleys': '95', 'penalties': '93', 'vision': '91', 'crossing': '94', 'fk_accuracy': '91', 'short_passing': '90', 'long_passing': '85', 'curve': '93', 'agility': '97', 'balance': '90', 'reactions': '99', 'ball_control': '98', 'dribbling': '97', 'composure': '99', 'interceptions': '47', 'heading_accuracy': '99', 'def_awareness': '38', 'standing_tackle': '50', 'sliding_tackle': '39', 'jumping': '99', 'stamina': '95', 'strength': '95', 'aggression': '81'},
#     '98ST_Mané_999695995692': {'guid': '98ST_Mané_999695995692', 'futbin_id': '28025', 'overall': '98', 'card_name': 'Mané', 'position': 'ST', 'card_type': 'f_moment', 'card_level': 'gold', 'card_rarity': 'special', 'traits': 'Outside Foot Shot,Speed Dribbler (CPU AI),Flair,Finesse Shot', 'name': 'sadio mané', 'club': 'fc bayern', 'nation': 'senegal', 'league': 'bundesliga', 'skills': '5', 'weak_foot': '4', 'intl_rep': '4', 'foot': 'right', 'height': '175', 'weight': '69', 'revision': 'player moments sbc', 'att_wr': 'high', 'def_wr': 'low', 'added_on': '2022-09-03', 'origin': 'n\\a', 'rface': '', 'btype': 'unique', 'age': '30 years old', 'id': '208722', 'club_id': '21', 'league_id': '19', '_pace': '99', '_shooting': '96', '_passing': '95', '_dribbling': '99', '_defending': '56', '_physicality': '92', 'acceleration': '99', 'sprint_speed': '99', 'positioning': '99', 'finishing': '99', 'shot_power': '96', 'long_shots': '95', 'volleys': '90', 'penalties': '84', 'vision': '99', 'crossing': '94', 'fk_accuracy': '87', 'short_passing': '99', 'long_passing': '87', 'curve': '93', 'agility': '99', 'balance': '98', 'reactions': '99', 'ball_control': '99', 'dribbling': '99', 'composure': '96', 'interceptions': '45', 'heading_accuracy': '99', 'def_awareness': '53', 'standing_tackle': '53', 'sliding_tackle': '48', 'jumping': '99', 'stamina': '99', 'strength': '88', 'aggression': '92'},
# }
chemistry_style = 'basic'


def headers():
    _headers = []
    for pos in pos_coef:
        _headers.append(pos.lower())
    heads = ','.join(_headers)
    return heads


def rpp_math():
    stat_list = []
    for stat in template:
        stat_list.append(stat)
    _rpp_db = {}
    try:
        for card, info in db.items():
            if info['position'] != 'GK':
                if info['height'] == '':
                    info['height'] = 180
                try:
                    btype = body_type_coef[info['btype']]
                except:
                    btype = body_type_coef['named']
                weak_foot = weak_foot_coef[info['weak_foot']]
                finesse_shot = 1
                outside_foot_shot = 1
                power_header = 1
                if len(re.findall('Finesse Shot', info['traits'])) != 0:
                    finesse_shot = trait_coef['Finesse Shot']
                if len(re.findall('Outside Foot Shot', info['traits'])) != 0:
                    outside_foot_shot = trait_coef['Outside Foot Shot']
                if len(re.findall('Power Header', info['traits'])) != 0:
                    power_header = trait_coef['Power Header']
                rpp = {}
                for pos, value in pos_coef.items():
                    coefs = []
                    for stat, value in value.items():
                        coefs.append(value)
                    values = []
                    outstats = []
                    for key, val in info.items():
                        for k, v in outstats_coef.items():
                            if key == k:
                                val = int(val)
                                val *= v
                                outstats.append(val)
                    for key, val in info.items():
                        for k, v in list(styles[chemistry_style].items()):  # стиль указан вначале кода
                            if key == k:
                                val = int(val)
                                val += v
                        for stat in stat_list:
                            if stat == key:  # условие для обработки только лишь статов
                                val = int(val)
                                if val > 99:
                                    val = 99
                                if key == 'agility':
                                    val *= btype
                                if key == 'dribbling':
                                    val *= btype
                                if key == 'finishing':
                                    val *= weak_foot * outside_foot_shot * finesse_shot
                                if key == 'long_shots':
                                    val *= weak_foot * outside_foot_shot * finesse_shot
                                if key == 'volleys':
                                    val *= weak_foot * outside_foot_shot
                                if key == 'interceptions':
                                    val *= int(info['height']) / 185
                                if key == 'heading_accuracy':
                                    val *= int(info['height']) / 185
                                if key == 'standing_tackle':
                                    val *= int(info['height']) / 185
                                if key == 'jumping':
                                    val *= int(info['height']) / 185
                                if key == 'heading_accuracy':
                                    val *= power_header
                                values.append(val)
                    rates = []
                    for i in range(0, len(coefs)):
                        rates.append(coefs[i] * values[i])
                    rate = (2 * sum(rates) + sum(outstats) + int(info['_pace'])) / 4
                    rpp.update({pos: round(rate, 1)})
                _rpp_db.update({card: rpp})
    except Exception as ex:
        print(card, info, ex)
    return _rpp_db


def rpp_import():
    cards = []
    for k, v in rpp_db.items():
        card = []
        card.append(k)
        for value in v.values():
            card.append(value)
        cards.append(tuple(card))
    for c in cards:
        cursor.execute(f"insert into ratings values {c}")


if __name__ == '__main__':
    start = timer()
    with open('../db/data.json', 'r') as file:
        db = json.load(file)
    rpp_db = rpp_math()
    connect = sqlite3.connect('../db/players_db.db')
    cursor = connect.cursor()
    cursor.execute(f"drop table if exists ratings")
    cursor.execute(
        f"create table if not exists ratings (guid primary key,{headers()})")
    rpp_import()
    connect.commit()
    connect.close()
    end = timer()
    time = end - start
    print(f"Time taken: {time}")