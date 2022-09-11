import json
import sqlite3
from timeit import default_timer as timer


def players_list():
    for v in db.values():
        try:
            v['age(dob)'] = v['age']
            del v['age']
        except:
            pass
    for v in db.values():
        try:
            v['age(dob)'] = v['dob']
            del v['dob']
        except:
            pass
    values = []
    for k, v in db.items():
        values.append(v)
    field_players = []
    gk_players = []
    for value in values:
        position = list(value.values())[4]
        if position == 'GK':
            gk_players.append(value)
        else:
            field_players.append(value)
    return {
        'field': field_players,
        'gk': gk_players
    }


def headers(position):
    _headers = []
    for row in players_list()[position][:1]:
        for k in row.keys():
            _headers.append(k)
    return str(_headers[1:]).replace('[', '').replace(']', '')


def value_string(_list):
    column_numbers = len(_list) - 1
    string = '?'
    string += str(',?')*column_numbers
    return string


def db_import(position):
    try:
        for row in players_list()[position]:
            _headers = []
            for r in row.keys():
                _headers.append(r)
            values = []
            for r in row.values():
                values.append(r)
            cursor.execute(f"insert into {position}_players {tuple(_headers)} values{tuple(values)}")
    except Exception as ex:
        print(row)
        print(ex)
        pass


if __name__ == '__main__':
    start = timer()
    # with open('data.json', 'r') as file:
    with open('../db/data.json', 'r') as file:
        db = json.load(file)
    connect = sqlite3.connect('../db/players_db.db')
    cursor = connect.cursor()
    cursor.execute(f"drop table if exists field_players")
    cursor.execute(f"drop table if exists gk_players")
    print('import is started')
    cursor.execute(
        f"create table if not exists field_players (guid primary key, {headers('field')})")
    db_import('field')
    cursor.execute(
        f"create table if not exists gk_players (guid primary key, {headers('gk')})")
    db_import('gk')

    end = timer()
    print("Time taken:", end - start)
    connect.commit()
    connect.close()
