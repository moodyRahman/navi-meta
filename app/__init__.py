from flask import *
from os import urandom
from .utils import usrctl, forms, mongodoc
from functools import wraps
# from pymongo import ObjectID
app = Flask(__name__)
app.secret_key = urandom(32)

# Decorators

def force_logout(route):
    '''Removes `\'user\'` from session cookie'''
    @wraps(route)
    def wrapper(*args, **kwargs):
        session.pop('user', None)
        return route(*args, **kwargs)

    return wrapper

def login_required(route):
    '''Checks for presence of `\'user\'` in session cookie. If nonexistant, redirects to login page'''
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return route(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper

def admin_required(route):
    '''Checks user mode. If not admin, returns home'''
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session['user']['mode'] == 'admin':
            return route(*args, **kwargs)
        else:
            flash('Administrative privileges required')
            return redirect(url_for('index'))

    return wrapper
        
# Routes

@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('home.html')

@app.route('/admin', methods=['GET'])
@admin_required
@login_required
def admin():
    flash('admin mode')
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
@force_logout
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = usrctl.login(request.form['name'], request.form['password'])
        if user:
            session['user'] = {'name': user['name'], 'mode':user['mode']}
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@force_logout
def logout():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@force_logout
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            usrctl.create(request.form['name'], request.form['password'])
            print('SYSTEM: Created user ' + request.form['name'])
            return redirect(url_for('login'))
        except ValueError as ex:
            flash(ex)
    return render_template('register.html', form=form)


application = app
if __name__ == '__main__':
    app.run(debug=True)
