# -*- coding: utf-8 -*-
from pprint import pprint

from pandas import set_option
from pandas.io.json import json_normalize

from seoapi import Wordstat

set_option('display.max_columns', 100)
set_option('display.width', 1500)

with open('../token.txt', 'r') as f:
    TOKEN = f.read()

with open('../host.txt', 'r') as f:
    HOST = f.read()

api = Wordstat(token=TOKEN, base_url=f'http://{HOST}/')

SESSION_ID = 'b7ffef9926074740db249d3fdbccb155f7b81c9a892b5aabd24b0ef776ef48e0'


def test_get_daily_report():
    r = api.get_report(**{'year': 2019, 'month': 12})
    print(r)
    print(sum([i["total"] for i in r]))


def test_generate_config_sessions():
    config_sessions = api.generate_config_sessions(
        search_phrases=["[!билеты !на !самолет]"],
        pages=[1],
        regions=[225],
        devices=[""],
    )
    print(config_sessions)


def test_load_tasks():
    data = {'session_id': 'b7ffef9926074740db249d3fdbccb155f7b81c9a892b5aabd24b0ef776ef48e0', 'region': 225, 'page': 1,
            'device': '',
            'queries': [{'query': '[!билеты !на !самолет]', 'query_id': 'f00cc0b917a844b1ac12c8bd114b1b56'}],
            'source': 'wordstat'}
    r = api.load_tasks(data)
    pprint(r)


def test_get_session_status():
    r = api.get_session_status(SESSION_ID)
    pprint(r)


def test_get_results():
    r = api.get_results(SESSION_ID)
    pprint(r)


def test_get_results_by_limit():
    r = api.get_results_by_limit(SESSION_ID, 1)
    print(r[0].keys())
    pprint(r)


def test_get_results_as_datarame():
    r = api.get_results_by_limit(SESSION_ID, 1)
    [i.update(i.pop('data')) for i in r]
    df = json_normalize(r)
    print(df)
