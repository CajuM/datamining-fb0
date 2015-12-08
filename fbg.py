#!/usr/bin/env python3

import facebook
import json
import requests
import arrow
import datetime
import calendar
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import Manager


FB_APP_ID = 'insert-here'
FB_APP_SECRET = 'insert-here'

def jprint(dictObj):
    print(json.dumps(dictObj, indent=4))

def getAll(jsonData):
    data = []
    while True:
        try:
            data += jsonData['data']
            jsonData = requests.get(jsonData['paging']['next']).json()
        except KeyError:
            break
    return data

def comTime(com):
    ct = com['created_time']
    ct = arrow.get(ct).datetime
    return calendar.timegm(ct.timetuple()) + 2 * 3600
    
def fbProcess(fbDict, api):
    dates = []
    jprint(fbDict)
    try:
        objs = getAll(api['graph'].get_connections(fbDict['id'], fbDict['type']))
    except Exception as e:
        print('----')
        print(e)
        jprint(fbDict)
        print('----')
        quit()
    for obj in objs:
        if fbDict['type'] == 'posts' or obj['from']['id'] == api['rootId']:
            dates.append(comTime(obj))

    api['queue'].put([{
        'id': obj['id'],
        'type': 'comments',
    } for obj in objs])

    return (dates, fbDict['type'])


if __name__ == '__main__':
    api = {
        'token': facebook.GraphAPI().get_app_access_token(FB_APP_ID, FB_APP_SECRET),
        'rootId': 'insert-site-id-here',
    }
    m = Manager()
    api['queue'] = m.Queue()
    api['graph'] = facebook.GraphAPI(access_token=api['token'], version='2.5')
    pool = Pool(processes=20)
    api['queue'].put([{
        'id': api['rootId'],
        'type': 'posts'
    }])
    f = open('data.txt', 'w')

    while(True):
        fbDicts = api['queue'].get()
        workload = [(fbDict, api) for fbDict in fbDicts]
        results = pool.starmap(fbProcess, workload)
        for result in results:
            for r in result[0]:
                day = int(r / (3600 * 24))
                seconds = (r % (3600 * 24))
                f.write('{} {} {}\n'.format(day, seconds, result[1]))
                f.flush()
