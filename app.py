import csv

from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

# from forms import LoginForm, RegisterForm, ContactForm, ResetForm, FeedBackForm

# basic setup
app = Flask(__name__,template_folder='templates')
Bootstrap(app)
app.secret_key = "key"

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
# app.config['USE_SESSION_FOR_NEXT'] = True

@app.route('/')
def index():
    return render_template('unprotected/unprotectedHome.html')

if __name__ == '__main__':
    app.run(debug=True)