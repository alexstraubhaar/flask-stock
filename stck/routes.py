from flask import render_template, flash, redirect
from stck import app
from stck.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Alex'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login required for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
