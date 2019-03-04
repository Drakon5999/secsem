# -*- coding: utf-8 -*-

import random

from sqlalchemy import text

from flask import render_template, url_for, request, abort, redirect, flash, session, g
from flask_session import Session

from landing import app
from landing import DATABASE

from html import escape
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("index.html", user=session.get('user'))


@app.route('/users')
def users():
    users_active = query_db('SELECT * FROM users where status = 1')
    return render_template('table.html', users=users_active)


@app.route('/by-login', methods=['GET', 'POST'])
def get_user_login():
    login = request.form.get('login')

    if login is not None:
        user_query = query_db("SELECT * FROM users where login = ?", (login, ))

        if len(user_query) != 0:
            return render_template('about.html', user=user_query[0])

        return render_template('search.html', wrong_login=escape(login), user=session.get('user'))

    return render_template('search.html', user=session.get('user'))


@app.route('/by-id', methods=['GET', 'POST'])
def get_user_id():
    id = request.form.get('id')
    print(id)
    if id is not None:
        user_query = query_db("SELECT * FROM users where id = ?", (id, ))

        if len(user_query) != 0:
            return render_template('about.html', user=user_query[0])

        return render_template('search.html', wrong_id=escape(id), user=session.get('user'))

    return render_template('search.html', user=session.get('user'))


@app.route('/search')
def get_user():
    return render_template("search.html", user=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/profile', code=302)

    if 'login' in request.form:
        user_query = query_db("SELECT * FROM users where login = ?",
                                       [request.form['login']])
        if len(user_query) != 0:
            user = user_query[0]
            passwords = query_db("SELECT * FROM p4$5w0rds where id = ? and password = ?",
                                         [user['id'], request.form['password']])
            if len(passwords) != 0:
                session['logged_in'] = True
                session['user'] = user
                return redirect('/profile', code=302)
        return render_template('login.html', wrong=True, last_login_value=escape(request.form['login']), user=session.get('user'))
    else:
        return render_template('login.html', user=session.get('user'))


def luhn_algorithm(digits):
    result = 0

    if len(digits) < 12:
        return False

    for i in range(len(digits)):
        card_num = int(digits[i])
        if card_num is None:
            return False
        if (len(digits) - i) % 2 == 0:
            card_num *= 2

            if card_num > 9:
                card_num -= 9

        result += card_num

    return result % 10 == 0


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
        return redirect('/login', code=302)
    is_admin = session['user']['login'] == 'admin'
    if 'card_number' in request.form and 'money_amount' in request.form:
        new_amount = int(request.form['money_amount'])
        new_card = ''.join(request.form['card_number'].split())
        if new_amount is not None and new_amount >= 0 and luhn_algorithm(new_card):
            query_db("UPDATE users SET money_amount = ?, card_number=? where login = ?",
                              (new_amount, new_card, session['user']['login']))
            get_db().commit()
            user = query_db("SELECT * FROM users where login = ?",
                              (session['user']['login'], ))[0]
            session['user'] = user
            return render_template('profile.html', user=session['user'], is_admin=is_admin, success_card=True)
        else:
            return render_template('profile.html', user=session['user'], is_admin=is_admin, fail_card=True)

    if 'change_password_login' in request.form and 'change_password_password' in request.form and is_admin:
        new_login = request.form['change_password_login']
        new_password = request.form['change_password_password']
        users = query_db("SELECT * FROM users where login = ?", (new_login, ))
        if len(users) == 0:
            return render_template('profile.html', user=session['user'], is_admin=is_admin, wrong_login_password=True)
        user = users[0]
        user_id = user["id"]
        query_db("UPDATE p4$5w0rds SET password = ? where id = ?", (new_password, user_id))
        get_db().commit()
        return render_template('profile.html', user=session['user'], is_admin=is_admin, success_password=True)

    return render_template('profile.html', user=session['user'], is_admin=is_admin)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login', code=302)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
