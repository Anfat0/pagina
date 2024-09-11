from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from logging import DEBUG
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = b'\x8bN7m\xc4\xd0A\xdc'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.logger.setLevel(DEBUG)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

Subcribe = []

def store_subcribe(url):
    Subcribe.append(dict(
        url=url,
        user='Henrry',
        date= datetime.now()
    ))

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/service.html')
def service():
    return render_template('service.html')

@app.route('/team.html', methods=['GET', 'POST'])
def team():
    if request.method=="POST":
        url=request.form['url']
        store_subcribe(url)
        app.logger.debug('stored subcribe: ' + url)
        flash("Your Feedback: " + url)
        return redirect(url_for('home'))
    return render_template('team.html')

@app.route('/why.html')
def why():
    return render_template('why.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created !')
        return redirect(url_for('home'))
    
    if form.errors:
        flash('Validation Errors: ' + str(form.errors))
        app.logger.error('ValidationError:\n' + str(form.errors))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)