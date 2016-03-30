# project/models.py


import datetime

from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, confirmed,
                 admin=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)

class Submission(db.Model):

    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    data_set = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=True)

    def __init__(self, code, data_set, user):
        self.code = code
        self.user = user
        self.data_set = data_set
        self.time = datetime.datetime.now()

    def submission_time(self):
        return self.time

    def get_user(self):
        return self.user

    def __repr__(self):
        return self.code

class Cat(db.Model):
    __tablename__ = 'cats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, default='Snowball')
    weight = db.Column(db.SmallInteger, nullable=True)

    def __init__(self, name, email):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return '<Cat %r>' % self.name


class Assert(db.Model):

    __tablename__ = "asserts"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    data_set = db.Column(db.Integer, nullable=False)
    hint = db.Column(db.String, nullable=True)

    def __init__(self, code, data_set, hint):

        self.code = code
        self.data_set = data_set
        self.hint = hint

    def get_code(self):
        return self.code

    def get_hint(self):
        return self.hint

    def __repr__(self):
        return self.code
