from flask import *
from os import urandom
from utils import usrctl, forms

app = Flask(__name__)
app.secret_key = urandom(32)
WTF_CSRF_ENABLED = False
WTF_CSRF_CHECK_DEFAULT = False


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = usrctl.login(request.form['name'], request.form['password'])
        if user:
            flash('User mode: ' + user['mode'])
            return redirect('/')
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=forms.LoginForm())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                usrctl.create(request.form['name'], request.form['password'])
                print('SYSTEM: Created user ' + request.form['name'])
                return redirect('/login', form=forms.LoginForm())
            except ValueError as ex:
                flash(ex)
    return render_template('register.html', form=form)



application = app
if __name__ == '__main__':
    app.run(debug=True)
