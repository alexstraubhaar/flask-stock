from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from stck.models import User, Artist, Album

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

class ArtistForm(FlaskForm):
    name = StringField("Artist's name", validators=[DataRequired()])
    submit = SubmitField('Create')

class AlbumForm(FlaskForm):
    title = StringField("Album's title", validators=[DataRequired()])

    # Selectfield with avalaible artists' names
    artist_name = SelectField(u'Artist', coerce=int, validators=[DataRequired()], choices=[(artist.id, artist.name) for artist in Artist.query.order_by('name')])

    submit = SubmitField('Create')


class SearchForm(FlaskForm):
    search = StringField('search', [DataRequired()])
    submit = SubmitField('Search')
    
