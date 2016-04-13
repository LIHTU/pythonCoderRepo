# project/user/forms.py

from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, DateField, FileField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Required, Optional

from project.models import User

class LoginForm(Form):
    email = TextField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class ChangePasswordForm(Form):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

class TestCaseForm(Form):
    assertion = StringField("Enter Assertion Here", validators=[Required()])
    hint = StringField("Enter a hint", validators=[Optional()])

class ChallengeForm(Form):
    name = StringField("Challenge Name", validators=[Optional()])
    description = TextField("Challenge Description", validators=[Optional()])
    dueDate = DateField("Due Date", validators=[Optional()])
    codeText = FileField("Initial Code Text", validators=[Optional()])
    # testCases = (will grab from session.localStorage...maybe)
    # course_id = SelectMultipleField("Choose a Course", validators=[Required()])
    submit = SubmitField("Submit")

    def validate(self):
        return True

