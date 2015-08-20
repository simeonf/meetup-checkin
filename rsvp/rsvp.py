# all the imports
import sqlite3
from os.path import dirname, abspath
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration
DATABASE = abspath(dirname(__file__)) + '/rsvp.db'
DEBUG = True
SECRET_KEY = 'Hmm. Should autogen this, right?'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db
    
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
@app.route('/')
def index():
    rsvps = query_db("SELECT * from rsvp where rsvp=? or rsvp=? order by name ", ('yes', 'waitlist'))
    present = query_db("SELECT count(*) as num from rsvp where present=?", (1,), True)['num']
    absent = query_db("SELECT count(*) as num from rsvp where present<>?", (1,), True)['num']
    total = present + absent
    return render_template('index.html', **locals())

@app.route('/ajax', methods=['POST'])
def ajax():
    db = get_db()
    id, present = request.form['id'], request.form['present']
    db.cursor().execute("UPDATE rsvp set present=? where id=?", (present, id))
    db.commit()
    return "OK"

@app.route('/ajax/stats')
def stats():
    present = query_db("SELECT count(*) as num from rsvp where present=?", (1,), True)['num']
    absent = query_db("SELECT count(*) as num from rsvp where present<>?", (1,), True)['num']
    total = present + absent
    return "%s / %s" % (present, total)

    
if __name__ == '__main__':
    app.run()

