# -*- coding:utf-8 -*-
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.config.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('auth/login.html')
    
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    
    if login_name is None or len(login_name) < 1:
        msg = '请输入用户名'
        return render_template('auth/login.html', msg=msg)
    
    if login_pwd is None or len(login_pwd) < 1:
        msg = '请输入密码'
        return render_template('auth/login.html', msg=msg)
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE username = ?',(login_name,)).fetchone()

    if user is None:
        msg = '用户名与密码错误！'
    elif not check_password_hash(user['password'],login_pwd):
        msg = '用户名与密码错误！'
        return render_template('auth/login.html', msg=msg)

    return redirect(url_for('center.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['login_name']
        password = request.form['login_pwd']
        db = get_db()
        error = None

        if not username:
            msg = 'Username is required.'
        elif not password:
            msg = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            msg = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return render_template('auth/register.html',msg=msg)

        msg = '注册成功'
        flash(error)

    return render_template('auth/register.html',msg=msg)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
