import functools
from .db import get_db
from markupsafe import escape
from werkzeug.security import check_password_hash
from flask import Blueprint, g, redirect, render_template, request, session, url_for

bp = Blueprint('auth', __name__, url_prefix='/login')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db = get_db()
        db.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        g.user = db.fetchone()

@bp.route('/', methods=('GET', 'POST'))
def login():
    context = {}
    context["error"] = None
    if request.method == "POST":
        # Process form data here
        username = escape(request.form["username"])
        password = escape(request.form["password"])
        try:
            # look up info from db
            db = g.db
            if db is None:
                print("Database cursor is None")
                context["error"] = "Could not connect to the database. Please try again."
                return render_template("login.html", context=context)
                
            db.execute('SELECT * FROM users WHERE username = %s', (username,))
            g.user = db.fetchone()

            if g.user is None:
                context["error"] = "Incorrect username. Please try again."
            elif not check_password_hash(g.user['password'], password):
                context["error"] = 'Incorrect password. Please try again'
            else:
                session.clear()
                session['user_id'] = g.user['id']
                return redirect("/db-tables/" + str(g.user['id']))
        except Exception as e:
            print('LOGIN ERROR:',e)
            context["error"] = "Login Error."+e
    return render_template("login.html", context=context)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g is not None:
            if getattr(g, 'user', None) is None:
                return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
