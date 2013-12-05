#!/usr/bin/env python
"""
Import spreadsheet into the db

Usage:
  import.py [-h] FILE

Arguments:
  FILE        Spreadsheet of meetup data

Options:
  -h --help   Show this screen.


"""
from __future__ import print_function
import sqlite3
import codecs
from docopt import docopt



def import_data(fn):
    """populate database table."""
    db = sqlite3.connect('rsvp.db')
    sql = "insert into rsvp (user_id, meetup_handle, name, rsvp, thumb) values(?, ?, ?, ?, ?)"
    with codecs.open(fn, mode='r', encoding="UTF-8") as f:
        f.next() # skip the header line
        for line in f:
            args = line.strip().split(',')
            args = map(unicode.strip, args)
            args.insert(1, args[1])
            db.cursor().execute(sql, args)
    db.commit()

if __name__ == '__main__':
    args = docopt(__doc__, version="spreadsheet.py 0.1")
    import_data(args['FILE'])    
