#!/usr/bin/env python
"""
Using the Meetup API - Dump first name, last name, RSVP status and pic to html tabular output.

Usage:
  spreadsheet.py [-h] EVENT_ID

Arguments:
  EVENT_ID     Meetup event id as seen in url of event.

Options:
  -h --help                    Show this screen.


"""
from __future__ import print_function
import os
import requests
import json
from docopt import docopt


KEY = os.environ["MEETUP_API_KEY"]
HOST = "https://api.meetup.com"

"""
r.text['meta'] = 
{u'count': 200, u'updated': 1386006108000, u'description': u'Query for Event RSVPs by event',
u'title': u'Meetup RSVPs v2',
u'url': u'https://api.meetup.com/2/rsvps?key=7e522312373d4e442613258306a49&event_id=151525392&order=event&desc=false&format=json&offset=0&page=200&fields=',
u'total_count': 217, u'lon': u'',
u'next': u'https://api.meetup.com/2/rsvps?key=7e522312373d4e442613258306a49&event_id=151525392&order=event&desc=false&format=json&offset=1&page=200&fields=',
u'method': u'RSVPs v2', u'link': u'https://api.meetup.com/2/rsvps',
u'lat': u'', u'id': u''}

and r.text['results']

{u'group': {u'urlname': u'sfpython', u'group_lon': -122.44000244140625, u'id': 1187265, u'group_lat': 37.77000045776367, u'join_mode': u'open'},
u'created': 1385449521000,
u'rsvp_id': 1057896362,
u'venue': {u'city': u'San Francisco', u'name': u'Yelp', u'zip': u'94105', u'repinned': False, u'lon': -122.399773, u'state': u'CA', u'address_1': u'140 New Montgomery', u'country': u'us', u'lat': 37.786663, u'id': 15022762},
u'response': u'yes',
u'member': {u'name': u'user 104429', u'member_id': 104429}, u'guests': 0, u'mtime': 1385449521000,
u'event': {u'event_url': u'http://www.meetup.com/sfpython/events/151525392/', u'id': u'151525392', u'name': u'December Presentation Night with Glyph', u'time': 1386209700000}}
"""

def rsvps(event_id):
    rsvps_url = "/2/rsvps"
    i = 0
    total_count = 1 # just guess and hope there are records
    next = HOST + rsvps_url
    params = {"event_id": event_id, "key": KEY}
    while i < total_count:
        r = requests.get(next, params=params)
        #decode json and get meta and results
        data = json.loads(r.text)
        total_count = data['meta']['total_count'] # real total, could be zero
        for record in data['results']:
            i += 1
            if record['response'] == 'yes':
                yield record
        next = data['meta'].get('next')
        if next:
            params = {} # already in the url

def main(event_id):
    member_url = "/2/member/%s"
    records = [['member_id', 'handle', 'rsvp', 'pic']]
    for record in rsvps(event_id):
        m = record['member']
        r = requests.get(HOST + member_url % (m['member_id']), params={"key": KEY})
        try:
            data = json.loads(r.text)
            pic = data['photo']['thumb_link']
        except KeyError:
            pic = ""
        records.append([str(m['member_id']), m['name'], record['response'], pic])
        
    print("\n".join([", ".join(rec) for rec in records]).encode("UTF-8"))

if __name__ == '__main__':
    args = docopt(__doc__, version="spreadsheet.py 0.1")
    main(args['EVENT_ID'])
    

