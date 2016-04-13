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
        return '<email {}>'.format(self.email)

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

    def __init__(self, name):
        self.name = name
        # self.weight = weight

    def __repr__(self):
        return '<Cat %r>' % self.name

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    challenges = db.relationship('Challenge', backref='course', lazy='dynamic')
    #students ::: add this later after you get the basics working.

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Course Name: %r>' % self.name

class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text, nullable=True)
    dueDate = db.Column(db.DateTime, nullable=True)
    codeText = db.Column(db.Text, nullable=True)
    testCases = db.Column(db.PickleType)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    # def __init__(self, name, description):
    #     self.name = name
    #     self.description = description
    #     self.testCases = {}

    def addTestCase(self, assertion, hint):

        testCase = {}
        caseNumber = len(self.testCases) + 1

        # populate test case with name, assertion, and hint
        testCase['name'] = 'Test Case %d' % caseNumber
        testCase['assertion'] = assertion
        testCase['hint'] = hint

        # add to ordered test case list
        if len(self.testCases) == 0:
            print "no previous test cases"
            testCases = []

        else:
            print "There were indeed some previus test cases."
            testCases = self.testCases

        testCases.append(testCase)
        self.testCases = testCases


    def addDueDate(self, year, month, day):
        self.dueDate = datetime.date(year, month, day)

    def addCodeText(self, codefile):
        codefile = open(codefile)
        text = codefile.read()
        self.codeText = text

    def __repr__(self):
        return '<Challenge %r>' % self.name


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
