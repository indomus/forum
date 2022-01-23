#!/usr/local/bin/python3
import sys
import json
import asyncio
import time
import requests
import yaml

filename = '/config/packages/skyq_mediaplayer.yaml'
name = 'Sky'
host = '192.168.1.15'
country = 'ITA'

async def buildChannelList():

    sources = {}

    url = 'http://{0}:9006/as/services'.format(host)
    r = requests.get(url, headers={'content-type': 'application/json'})
    array = r.json()
    for channel in array['services']:
       chName = channel['t'].replace(" ", "") + "_"+channel['c']
       chNumber = ",".join([channel['c'][i:i+1] for i in range(0, len(channel['c']), 1)])
       sources[chName] = chNumber

    entity = {'media_player':[
                {'platform': 'skyq',
                 'name': name,
                 'host': host,
                 'live_tv': False,
                 'country': country,
                 'sources': sources
                }
             ]}

    with open(filename, 'w') as f:
        data = yaml.dump(entity, f, sort_keys=False)

async def main():
    asyncio.ensure_future(buildChannelList())

# Main body
if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = time.time()
    #print(f'Time: {end-start:.2f} sec')
