#!/usr/bin/env python
"""
Using the Meetup API - Dump first name, last name, RSVP status and pic to .csv for importing

Usage:
  spreadsheet.py [-h] --output=foo.csv EVENT_ID

Arguments:
  EVENT_ID     Meetup event id as seen in url of event.

Options:
  -h --help               Show this screen.
  --output <fullnames>    Output filename

"""
from __future__ import print_function
import os
import codecs
import requests
import json
from docopt import docopt


KEY = os.environ["MEETUP_API_KEY"]
HOST = "https://api.meetup.com"

class Rsvp(object):
  def __init__(self, record):
    self.id = record['member']['member_id']
    self.name = record['member']['name']
    self.response = record['response']
    self.pic = record.get("member_photo", {}).get('thumb_link', '')
    self.raw = record

  def csv(self):
    return [str(self.id), self.name, self.response, self.pic]

def rsvps(event_id):
  rsvps_url = "/2/rsvps"
  i = 0
  total_count = 1 # just guess and hope there are records
  next = HOST + rsvps_url
  per_page = 100
  params = {"event_id": event_id, "key": KEY, 'page': per_page, 'offset': 0, 'order': 'event', 'desc': 'false'}
  i = 0
  records = []
  while True:
    r = requests.get(next, params=params)
    data = json.loads(r.text)
    for page_i, record in enumerate(data['results']):
      records.append(record)
    i += page_i + 1
    meta = data['meta']
    offset = i / per_page
    if i < meta['total_count']:
      params['offset'] = offset
    else:
      return records

def main(event_id, fn):
  member_url = "/2/member/%s"
  header = [['member_id', 'handle', 'rsvp', 'pic']]
  responses = {}
  records = rsvps(event_id)
  print("Total number of records: %s" % len(records))
  for record in records:
    r = Rsvp(record)
    responses[r.id] = r # later responses overwrite earlier
  records = header + [obj.csv() for obj in responses.values() if obj.response in ['yes', 'waitlist']]
  with codecs.open(fn, "w", encoding="UTF-8") as fp:
    for rec in records:
      fp.write(", ".join(rec) + "\n")

if __name__ == '__main__':
  args = docopt(__doc__, version="spreadsheet.py 0.1")
  main(args['EVENT_ID'], args['--output'])
