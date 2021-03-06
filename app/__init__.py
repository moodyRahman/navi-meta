from flask import *
from os import urandom
from .utils import usrctl, forms, dbctl
from functools import wraps

app = Flask(__name__)
debug = True
app.secret_key = urandom(32) if not debug else 'not a secret key'


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
        # print(session)
        if session['user']['accounttype'] == 'admin':
            return route(*args, **kwargs)
        else:
            flash(f'Administrative privileges required to view \"{url_for(route.__name__)}\"', 'danger')
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
    flash('admin mode', 'info')
    return render_template('home.html')

@app.route("/admindash", methods=["POST", "GET"])
@admin_required
def admindash():
    if request.method == "POST":
        # print(request.form)
        # print(request.form.to_dict(flat=False))
        form = request.form.to_dict(flat=False)
        print(form)
        dictsout={}
        for n, x in enumerate(form["suppq[]"]):
            dictsout[x] = form["wc[]"][n]
        dbctl.AllCollege(name=form["collegename"][0], questions=dictsout).save()
        return "x"
    if request.method == "GET":
        return render_template("admindash.html")
        


# @app.route("")

@app.route('/login', methods=['GET', 'POST'])
@force_logout
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = usrctl.login(request.form['name'], request.form['password'])
        if user: # login() returns user dict
            session['user'] = { # store vital user info
                'name': user['name'], 
                'accounttype': user['accounttype']
            }
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password', 'danger')
    
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
            print('SYSTEM: Created user ' + request.form['name']) # log user creation
            flash('Account created', 'success')
            return redirect(url_for('login'))
        except ValueError as ex:
            flash(ex, 'danger')
        
    return render_template('register.html', form=form)

@app.route("/myessay")
def getessays():
    # dbctl.User.objects(name=session["user"])
    return render_template("myessay.html")

@app.route("/mycolleges")
def mycolleges():

    return render_template("mycolleges.html")

application = app
if __name__ == '__main__':
    app.run(debug=debug)
