import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from uhcarmel.db import get_db, User

bp = Blueprint('auth', __name__, url_prefix='/uhcarmel/auth')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        mirs = request.form['mirs']
        password = request.form['password']
        
        
        db = get_db()
        error = None
        user = db.query(User).filter_by(mirs = mirs).one();
        if user is None:
            error = 'Incorrect username.'
        elif not user.verify_password(password):
            error = 'Incorrect password.'
        elif not user.is_admin:
            print user.is_admin
            error = "Unauthorized User"

        if error is None:
            session.clear()
            session['mirs'] = user.mirs
            return redirect(url_for('locations.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        mirs = request.form['mirs']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['lastname_name']
        is_admin = request.form['is_admin']
        db = get_db()
        error = None

        if not mirs:
            error = 'mirs is required.'
        elif not password:
            error = 'Password is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Password is required.'
        elif db.query(User).filter_by(mirs = mirs).one() is not None:
            error = 'User {} is already registered.'.format(mirs)

        if error is None:
            new_user = User(mirs=mirs,first_name=first_name,last_name=last_name,is_admin=is_admin)
            new_user.hash_password(password)
            db.add()
            db.commit()
            return redirect(url_for('auth.register'))
        
        flash(error)

    return render_template('auth/register.html')

@bp.before_app_request
def load_logged_in_user():
    mirs = session.get('mirs')

    if mirs is None:
        g.user = None
    else:
        g.user = get_db().query(User).filter_by(mirs = mirs).one()

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