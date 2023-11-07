from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

#Removing validators allows user to signup
#Error recieved: TypeError: Form.validate() got an unexpected keyword argument 'extra_validators' on useradd  11/4
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

#In progress 11/4
class EditUserForm(FlaskForm):
    """Form for editing a user."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    image_url = StringField('Image URL')
    header_image_url = StringField('Header Image URL')
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[DataRequired()])

#attempt to get over: TypeError: Form.validate() got an unexpected keyword argument 'extra_validators' on useradd
#def validate_on_submit(self, extra_validators=None):
#        """Call :meth:`validate` only if the form is submitted.
#        This is a shortcut for ``form.is_submitted() and form.validate()``.Open an interactive python shell in this frame
#        """
#        return self.is_submitted() and self.validate(extra_validators=extra_validators)
#
#
#def validate(self, extra_validators=None):
#    initial_validation = super(UserAddForm, self).validate(extra_validators)