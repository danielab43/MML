import sqlalchemy
import json
from app import app, db
from .models import Song, Artist, User
from .forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
import logging
import time

@app.route('/', methods=['GET'])
def homepage():
    page = request.args.get('page', 1, type=int)
    per_page = 16
    songs = Song.query.order_by(Song.Title).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('home.html', Title="Home", songs=songs, title_order='asc', genre_order='asc',
                           year_order='asc', upvotes_order='asc',
                           downvotes_order='asc')


@app.route('/profile/<username>', methods=['GET'])
@login_required
def user(username):
    page = request.args.get('page', 1, type=int)
    per_page = 10

    user = db.first_or_404(sqlalchemy.select(User).where(User.username == username))

    liked_song_ids = [song.SongID for song in user.likedsongs]

    # Filter liked songs and create a custom pagination
    liked_songs = Song.query.filter(Song.SongID.in_(liked_song_ids)).order_by(Song.Title)
    paginated_songs = liked_songs.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('profile.html', Title="Profile", user=user,
                           songs=paginated_songs, page=page)

@app.route('/order/<criteria>', methods=['GET', 'POST'])
def order(criteria):
    title_order = request.args.get('order_title', 'asc')
    genre_order = request.args.get('order_genre', 'asc')
    year_order = request.args.get('order_year', 'asc')
    upvotes_order = request.args.get('order_upvotes', 'asc')
    downvotes_order = request.args.get('order_downvotes', 'asc')

    page = request.args.get('page', 1, type=int)
    per_page = 16

    if criteria == 'Title':
        current_order = title_order
    elif criteria == 'Genre':
        current_order = genre_order
    elif criteria == 'Year':
        current_order = year_order
    elif criteria == 'Upvotes':
        current_order = upvotes_order
    elif criteria == 'Downvotes':
        current_order = downvotes_order
    else:
        current_order = 'no_order'

    if current_order == 'asc':
        songs = Song.query.order_by(getattr(Song, criteria)).paginate(page=page, per_page=per_page, error_out=False)
        next_order = 'desc'
    elif current_order =='desc':
        songs = Song.query.order_by(getattr(Song, criteria).desc()).paginate(page=page, per_page=per_page, error_out=False)
        next_order = 'no_order'
    else:
        songs = Song.query.paginate(page=page, per_page=per_page, error_out=False)
        next_order = 'asc'

    if criteria == 'Title':
        title_order = next_order
    elif criteria == 'Genre':
        genre_order = next_order
    elif criteria == 'Year':
        year_order = next_order
    elif criteria == 'Upvotes':
        upvotes_order = next_order
    elif criteria == 'Downvotes':
        downvotes_order = next_order

    return render_template('home.html', Title="Home", songs=songs,
                           current_order=current_order, next_order=next_order,
                           title_order=title_order, genre_order=genre_order,
                           year_order=year_order, upvotes_order=upvotes_order,
                           downvotes_order=downvotes_order)

@app.route('/recommend')
@login_required
def recomend():
    print("yay")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Stops already logged-in user reaching login in page
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    # When the user attempts to log in
    if form.validate_on_submit():
        # Finds a user object in db if one exists with provided username
        user = db.session.scalar(
            sqlalchemy.select(User).where(User.username == form.username.data))
        # Checks if a user object is found and if provided password is matching
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            app.logger.info('[%s] %s failed to log in',
                            time.asctime(time.localtime()), form.username.data)
            return redirect('/login')
        # Logs the user in setting the current_user to that user for future pages
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', Title="Log In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already signed in stops them reaching sign up page
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    # checks if form has had a valid submit
    if form.validate_on_submit():
        # Creates a new user based on form data
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        # Adds new user to database
        db.session.add(user)
        db.session.commit()
        # Redirects user to log into their account
        flash('Successfully Signed up')
        return redirect('/login')
    return render_template('register.html', Title="Sign Up", form=form)

@app.route('/vote', methods=['POST'])
@login_required
def vote():
    data = json.loads(request.data)
    song_id = int(data.get('song_id'))
    song = Song.query.get(song_id)

    # Increment the correct vote
    if data.get('vote_type') == "up":
        if song in current_user.likedsongs:
            current_user.likedsongs.remove(song)
            song.Upvotes -= 1
        else:
            current_user.likedsongs.append(song)
            song.Upvotes += 1
    else:
        if song in current_user.dislikedsongs:
            current_user.dislikedsongs.remove(song)
            song.Downvotes -= 1
        else:
            current_user.dislikedsongs.append(song)
            song.Downvotes += 1

    # Save the updated vote count in the DB
    db.session.commit()
    # Tell the JS .ajax() call that the data was processed OK
    return json.dumps({'status': 'OK', 'upvotes': song.Upvotes, 'downvotes': song.Downvotes})
