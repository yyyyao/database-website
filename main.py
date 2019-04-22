import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3 as sql
import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"
Bootstrap(app)
DATABASEURI = "postgresql://yw3225:dbdb@34.73.21.127/proj1part2"
engine = create_engine(DATABASEURI)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except Exception as e:
        print ("Problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    username=form.username.data
    email=form.email.data
    password=form.password.data

    if form.validate_on_submit():
        cursor = g.conn.execute(
            '''SELECT id, username FROM usernba WHERE username = '{}';'''.format(username)
                ).fetchone()
        if cursor is not None:
            print(cursor)
            return render_template('signup.html',
                                   error=True, form = form)

        if  g.conn.execute(
            '''SELECT id FROM usernba WHERE username = '{}';'''.format(username)
                ).fetchone() is not None:
            return render_template('signup.html',
                                   error=True, form = form)

        if  g.conn.execute(
            '''SELECT id FROM usernba WHERE email = '{}';'''.format(email)
                ).fetchone() is not None:
            return render_template('signup.html',
                                   error=True, form = form)

        cursor = g.conn.execute("SELECT max(id) FROM usernba")
        new_id = cursor.fetchone()[0] + 1
        g.conn.execute(
        '''INSERT INTO usernba (id, username, email, password) VALUES ({0}, '{1}', '{2}', '{3}')'''.format(new_id, username, email, password)
            )

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password'].strip()
        # print (password)
        user = g.conn.execute(
            '''SELECT * FROM usernba WHERE username = '{}';'''.format(username)
        )
        if user:
            for u in user:
                u = str(u.password).strip()
                print("------user------password------{}".format(u))
                # print(str(password))
                # if check_password_hash(u[3], form.password.data):

                if u == password:
                    print ("---------success--------")
                    session['logged_in'] = True
                    #session['user_id'] = user[0]
                    #login_user(user, remember=form.remember.data)
                    return redirect(url_for('index'))
        return render_template('login.html', error=True, form = form)
            #'<body>Invalid username or password, please return to the previous page and try agian.</body>'
    return render_template('login.html', error = False, form=form)

@app.route('/logout')
def logout():
    session['user_id'] = None
    session['logged_in'] = False
    return redirect(url_for('base'))

@app.route('/index')
def index():
    return render_template('index.html')

######################################################################################################################
######################################################################################################################
######################################################################################################################

@app.route('/result',methods = ['POST'])
def search_player():
    if request.method == 'POST':
        pname = request.form['pname']
        tname = request.form['tname']
        print('pname', pname, 'tname', tname)

        # con = sql.connect("database.db")
        # con.row_factory = sql.Row
        # cur = con.cursor()

        # conn.execute("CREATE VIEW viewplayer AS SELECT pid,players.team,players.ssn,birthday,height_in,weight_lb,position,salary2018_2019,pointspergame FROM players inner join employees on players.ssn = employees.ssn")

        engine = create_engine(DATABASEURI, convert_unicode=True)
        conn = engine.connect()

        if pname != '*':
          cursor_player = conn.execute('''SELECT * FROM viewplayer WHERE pid = '{}';'''.format(pname))
          rows_player = cursor_player.fetchall()
          print(rows_player)
        # cursor_team = conn.execute('''SELECT * FROM teams WHERE name = '{}';'''.format(tname))
        # rows_team = cursor_team.fetchall()

        # players = Table('viewplayer', metadata, autoload=True)
        # rows_player = players.select(players.c.pid == pname).execute()

        # metadata = MetaData(bind=engine)
        # players = Table('players', metadata, autoload=True)
        # rows = players.select(players.c.pid == pname).execute()

        # cur.execute("SELECT * from players")
          if rows_player != []:
            print ("Select Player successfully")
            return render_template("psqlsearch_player.html",rows_player=rows_player)
          else:
            return render_template("error.html", pvalue=pname, tvalue=tname)
        elif tname != '*':
          cursor_team = conn.execute('''SELECT * FROM teams WHERE name = '{}';'''.format(tname))
          rows_team = cursor_team.fetchall()
          if rows_team != []:
            print ("Select Team successfully")

            cursor_game = conn.execute('''SELECT DISTINCT games.gid, games.date, games.time, host, scoreh, visitor, scorev from teams inner join games on name = games.host OR name = games.visitor WHERE name = '{}';'''.format(tname))
            rows_game = cursor_game.fetchall()
            print ("Select Game successfully")

            cursor_manager = conn.execute('''SELECT mname, ssn, college, since FROM teams inner join
                                    (SELECT mname, managers.ssn, college, tid, since FROM managers inner join manage 
                                    ON managers.ssn = manage.ssn) new
                                    ON teams.tid = new.tid
                                    WHERE name = '{}';'''.format(tname))
            rows_manager = cursor_manager.fetchall()

            print ("Select manager successfully")

            cursor_boss = conn.execute('''SELECT new.name, ssn, since FROM teams inner join
                                            (SELECT boss.name, boss.ssn, own_by.tid, own_by.since FROM boss inner join own_by
                                            ON boss.ssn = own_by.ssn) new
                                            ON teams.tid = new.tid
                                            WHERE teams.name = '{}';'''.format(tname))
            rows_boss = cursor_boss.fetchall()

            print ("Select manager successfully")
            return render_template("psqlsearch_team.html",rows_team=rows_team,rows_game = rows_game,rows_manager=rows_manager, rows_boss=rows_boss)
          else:
            return render_template("error.html", pvalue=pname, tvalue=tname)
        else:
          return render_template("error.html", pvalue=pname, tvalue=tname)


@app.route('/search_team/<tname>')
def search_team(tname):
    print(tname)

    engine = create_engine(DATABASEURI, convert_unicode=True)
    conn = engine.connect()

    cursor_team = conn.execute('''SELECT * FROM teams WHERE name = '{}';'''.format(tname))
    rows_team = cursor_team.fetchall()

    print ("Select Team successfully")

    cursor_game = conn.execute('''SELECT DISTINCT games.gid, games.date, games.time, host, scoreh, visitor, scorev from teams inner join games on name = games.host OR name = games.visitor WHERE name = '{}';'''.format(tname))
    rows_game = cursor_game.fetchall()

    print ("Select Game successfully")

    cursor_manager = conn.execute('''SELECT mname, ssn, college, since FROM teams inner join
                                    (SELECT mname, managers.ssn, college, tid, since FROM managers inner join manage 
                                    ON managers.ssn = manage.ssn) new
                                    ON teams.tid = new.tid
                                    WHERE name = '{}';'''.format(tname))
    rows_manager = cursor_manager.fetchall()

    print ("Select manager successfully")

    cursor_boss = conn.execute('''SELECT new.name, ssn, since FROM teams inner join
                                    (SELECT boss.name, boss.ssn, own_by.tid, own_by.since FROM boss inner join own_by
                                    ON boss.ssn = own_by.ssn) new
                                    ON teams.tid = new.tid
                                    WHERE teams.name = '{}';'''.format(tname))
    rows_boss = cursor_boss.fetchall()

    print ("Select manager successfully")

    return render_template("psqlsearch_team.html",rows_team = rows_team, rows_game = rows_game, rows_manager=rows_manager, rows_boss=rows_boss)

# @app.route('/result',methods = ['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         result = request.form
#         return render_template("search.html",result = result)
@app.route('/enterplayer')
def new_player():
    return render_template('newplayer.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    # msg = ''
    if request.method == 'POST':

        nm = request.form['addname']
        tm = request.form['addteam']

        if not nm:
            error = 'player name is required.'
        elif not tm:
            error = 'team name is required.'
        try:
            engine = create_engine(DATABASEURI)
            # with sql.connect("database.db") as con:
            with engine.connect() as con:
            # cur = con.cursor()
            # cur.execute("INSERT INTO players (name, team) VALUES (?,?)",(nm,tm) )
                con.execute('''INSERT INTO myinsert (name, team) VALUES ('{0}', '{1}')'''.format(nm,tm))
                # con.commit()
                msg = "Request successfully added, waiting for administrator to approve."
                print(msg)
                return render_template("result.html", msg = msg)
                con.close()
        # except:
        #   con.rollback()
        #   msg = "error in insert operation"
        #   print(msg)
        # finally:
        except Exception as e:
            error = e
    return render_template("result.html", msg = error)
          


@app.route('/profile')
def profile():
    # con = sql.connect("database.db")
    # con.row_factory = sql.Row
    # cur = con.cursor()
    # cur.execute("select * from players")
    # rows = cur.fetchall()
    # cur_user = con.cursor()
    # cur_user.execute("select * from user")
    # user = cur_user.fetchall()

    engine = create_engine(DATABASEURI)
    con = engine.connect()
    cusor_insert = con.execute("select * from myinsert")
    rows_insert = cusor_insert.fetchall()

    cusor_user = con.execute("select * from usernba")
    rows_user = cusor_user.fetchall()

    return render_template("profile.html",rows_user = rows_user, rows_insert = rows_insert)


@app.route('/listplayer')
def listplayer():
    # con = sql.connect("database.db")
    # con.row_factory = sql.Row
    # cur = con.cursor()
    # cur.execute("select * from players")
    # rows = cur.fetchall()

    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    cursor_player = conn.execute("select * from players inner join employees on players.ssn = employees.ssn")
    rows_player = cursor_player.fetchall()
    return render_template("listplayer.html",rows = rows_player)

@app.route('/listteam')
def listteam():
    engine = create_engine(DATABASEURI)
    conn = engine.connect()
    cursor_team = conn.execute("select * from teams")
    rows_team = cursor_team.fetchall()

    return render_template("listteam.html",rows = rows_team)

@app.route('/listgame')
def listgame():
    engine = create_engine(DATABASEURI)
    conn = engine.connect()
    cursor_game = conn.execute("select * from games")
    rows_game = cursor_game.fetchall()
    return render_template("listgame.html",rows = rows_game)


@app.route('/init')
def init():
    # conn = sqlite3.connect('database.db')
    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    print ("Opened database successfully")

    conn.execute('CREATE TABLE myinsert (name TEXT, team TEXT)')
    print ("Insert Player Table created successfully")

    # conn.execute('CREATE TABLE user (id INT, username CHAR(15), email CHAR(50), password CHAR(80), PRIMARY KEY (id))')
    # print ("User Table created successfully")

    conn.close()
    return 'OK'


@app.route('/initpsql')
def initpsql():
    engine = create_engine(DATABASEURI)
    conn = engine.connect()

    cursor_player = conn.execute("select * from players inner join employees on players.ssn = employees.ssn")
    rows_player = cursor_player.fetchall()

    cursor_coach = conn.execute("select * from coaches inner join employees on coaches.ssn = employees.ssn")
    rows_coach = cursor_coach.fetchall()

    cursor_manager = conn.execute("select * from managers inner join employees on managers.ssn = employees.ssn")
    rows_manager = cursor_manager.fetchall()

    cursor_team = conn.execute("select * from teams")
    rows_team = cursor_team.fetchall()

    cursor_boss = conn.execute("select * from boss")
    rows_boss = cursor_boss.fetchall()

    cursor_game = conn.execute("select * from games")
    rows_game = cursor_game.fetchall()

    return render_template("list.html",
      rows_player=rows_player,
      rows_coach=rows_coach,
      rows_manager=rows_manager,
      rows_team=rows_team,
      rows_boss=rows_boss,
      rows_game=rows_game)



if __name__ == '__main__':
    import click
    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print ("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=True, threaded=threaded)
    run()
    # app.run(debug = True)
