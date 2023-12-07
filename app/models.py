from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


linking = db.Table('linking',
                   db.Model.metadata,
                   db.Column('SongID', db.Integer, db.ForeignKey('song.SongID'), primary_key=True),
                   db.Column('ArtistID', db.Integer, db.ForeignKey('artist.ArtistID'), primary_key=True)
                   )

usersongs = db.Table('usersongs',
                     db.Model.metadata,
                     db.Column('SongID', db.Integer, db.ForeignKey('song.SongID'), primary_key=True),
                     db.Column('userid', db.Integer, db.ForeignKey('user.userid'), primary_key=True)
                     )

userdissongs = db.Table('userdissongs',
                        db.Model.metadata,
                        db.Column('SongID', db.Integer, db.ForeignKey('song.SongID'), primary_key=True),
                        db.Column('userid', db.Integer, db.ForeignKey('user.userid'), primary_key=True)
                        )


class Song(db.Model):
    __tablename__ = 'song'
    SongID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(250), index=True)
    Genre = db.Column(db.String(250), index=True)
    Year = db.Column(db.Integer, index=True)
    Upvotes = db.Column(db.Integer, default=0)
    Downvotes = db.Column(db.Integer, default=0)
    Artists = db.relationship('Artist', secondary=linking, back_populates="Songs")

    def __repr__(self):
        return self.Title


class Artist(db.Model):
    __tablename__ = 'artist'
    ArtistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(250), index=True)
    Songs = db.relationship('Song', secondary=linking, back_populates="Artists")

    def __repr__(self):
        return self.Name


class User(UserMixin, db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), index=True, unique=True)
    password_hash = db.Column(db.String(256), nullable=True)
    likedsongs = db.relationship('Song', secondary=usersongs)
    dislikedsongs = db.relationship('Song', secondary=userdissongs)

    def get_id(self):
        return self.userid

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def like_song(self, song):
        if song not in self.likedsongs:
            self.likedsongs.append(song)
            song.Upvotes += 1
            db.session.commit()

    def unlike_song(self, song):
        if song in self.likedsongs:
            self.likedsongs.remove(song)
            song.Upvotes -= 1
            db.session.commit()

    def avatar(self, size):
        return f'https://www.gravatar.com/avatar/{self.userid}?d=identicon&s={size}'

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
