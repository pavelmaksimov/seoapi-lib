# -*- coding: utf-8 -*-
from pprint import pprint
from pandas.io.json import json_normalize
from pandas import set_option
from seoapi import Serp
import pandas as pd

set_option('display.max_columns', 100)
set_option('display.width', 1500)

with open('../token.txt', 'r') as f:
    TOKEN = f.read()

with open('../host.txt', 'r') as f:
    HOST = f.read()

SOURCE = Serp.YANDEX
SESSION_ID = 'aba51f11140f4c703256211d7cda67642b3075c79bb3d875d5e95343bb0e89ff'

api = Serp(source=SOURCE, token=TOKEN, base_url=f'http://{HOST}/')


def test_get_regions():
    r = api.get_regions(**{'q': 'А'})
    print(r)


def test_get_daily_report():
    r = api.get_report(**{'year': 2019, 'month': 8})
    print(r)
    print(sum([i["total"] for i in r]))


def test_generate_config_sessions():
    config_sessions = api.generate_config_sessions(
        search_phrases=["[!билеты !на !самолет]"],
        regions=[1],
        is_mobile=[0],
        count_results=50,
    )
    print(config_sessions)


def test_load_tasks():
    data = {
        'total_pages': 1,
        'region': 1,
        'source': 'yandex',
        'numdoc': 50,
        'is_mobile': 0,
        'domain': 'yandex.ru',
        'session_id': 'aba51f11140f4c703256211d7cda67642b3075c79bb3d875d5e95343bb0e89ff1',
        'queries': [{'query': '[!билеты !на !самолет]',
                     'query_id': '4bcbe299531547ea90c9aeaaa2076d34'}]
    }
    r = api.load_tasks(data)
    print(r)


def test_get_session_status():
    r = api.get_session_status(SESSION_ID)
    pprint(r)


def test_is_finish_session():
    r = api.is_finish_session(SESSION_ID)
    print(r)


def test_get_results():
    r = api.get_results(SESSION_ID)
    print([pprint(i["query"]) for i in r["results"]])
    print('\n', len(r))
    pprint(r)


def test_get_results_by_limit():
    r = api.get_results_by_limit(
        SESSION_ID,
        limit_in_request=100
    )
    pprint(r)


def test_get_results_as_df():
    r = api.get_results(SESSION_ID)
    df = json_normalize(
        r,
        record_path=['organic'],
        meta=['parsed_at', 'query', 'is_mobile', 'count_results',
              'is_found', 'is_misspell', 'numdoc',
              'query_id', 'region', 'se_domain', 'se_url',
              'source', 'total_pages'])
    print(df.columns)
    print(df)
    df.to_excel('экспорт фраз.xlsx')
