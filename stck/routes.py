from flask import render_template, flash, redirect, request, url_for
from stck import app, db
from stck.forms import LoginForm, RegistrationForm, ArtistForm, AlbumForm
from flask_login import current_user, login_user, logout_user, login_required
from stck.models import User, Artist, Album
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/artist/<name>')
@login_required
def artist(name):
    artist = Artist.query.filter_by(name=name).first_or_404()
    albums = Album.query.filter_by(artist_id=artist.id).all()
    return render_template('artist.html', artist=artist, albums=albums)

@app.route('/artist/create', methods=['GET', 'POST'])
@login_required
def new_artist():
    form = ArtistForm()
    if form.validate_on_submit():
        artist = Artist(name=form.name.data)
        db.session.add(artist)
        db.session.commit()
        flash('Artist created')
    return render_template('new_artist.html', form=form)

@app.route('/album/<title>')
@login_required
def album(title):
    album = Album.query.filter_by(title=title).first_or_404()
    return render_template('album.html', album=album)

@app.route('/album/create', methods=['GET', 'POST'])
@login_required
def new_album():
    form = AlbumForm()
    if form.validate_on_submit():
        title = form.title.data
        artist_id = form.artist_name.data
        lps = form.lps.data
        cds = form.cds.data
        tapes = form.tapes.data
        album = Album(title=title, artist_id=artist_id, lps=lps, cds=cds, tapes=tapes)
        db.session.add(album)
        db.session.commit()
        flash('Album created')
    return render_template('new_album.html', form=form)

@app.route('/stock')
@login_required
def stock():
    albums = Album.query.all()
    return render_template('stock.html', albums=albums)
