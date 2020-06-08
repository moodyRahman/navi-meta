from flask import *
from os import urandom
from .utils import usrctl, forms

# from pymongo import ObjectID
app = Flask(__name__)
app.secret_key = urandom(32)
WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False


@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if 'user' in session:
        return redirect('/')
    if form.validate_on_submit():
        user = usrctl.login(request.form['name'], request.form['password'])
        if user:
            session['user'] = user['name']
            return redirect('/')
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['user']
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/')
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            usrctl.create(request.form['name'], request.form['password'])
            print('SYSTEM: Created user ' + request.form['name'])
            return redirect('/login')
        except ValueError as ex:
            flash(ex)
    return render_template('register.html', form=form)


application = app
if __name__ == '__main__':
    app.run(debug=True)
