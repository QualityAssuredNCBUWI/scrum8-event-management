from . import db
from werkzeug.security import generate_password_hash


affiliation = db.Table('affiliation', 
    db.Column('uid', db.Integer, db.ForignKey('users.id'), primary_key=True),
    db.Column('groupid', db.Integer, db.ForeignKey('groups.id'), primary_key=True )
    )

class Users(db.Model):
    __tablename__ = 'Users'
 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(1024))
    last_name = db.Column(db.String(1024))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    role = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True))
    groups = db.relationship("Groups",  secondary=affiliation)
    

    def __init__(self, first_name, last_name, username, password, email, role, profile_photo, created_at, groups):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.email = email
        self.profile_photo = profile_photo
        self.created_at = created_at
        self.role = role
        self.groups=groups

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r, %r>' % (self.id, self.name) 

class Events(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'Events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1024))
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))
    description = db.Column(db.String(1024))
    venue = db.Column(db.String(255))
    image = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    status = db.Column(db.String(255))
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(timezone=True))



    def __init__(self, title, start_date, end_date, description, venue, image, website_url, status, uid, created_at):
        self.description = description
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.image = image
        self.website_url = website_url
        self.status = status
        self.uid = uid 
        self.created_at = created_at


    def __repr__(self):
        return '<Events %r>' % (self.id)


class Groups(db.Model):
    __tablename__ = 'Groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    admin = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
        

    def __repr__(self):
        return '<Groups %r>' % (self.id)




class Affiliate(db.Model):
    __tablename__ = 'Affiliate'

    userId = db.Column(db.String(1024), foreign_key=True)
    groupId = db.Column(db.String(1024), foreign_key=True)
    
    def __init__(self, userId, groupId):
        self.userId = userId
        self.groupId = groupId
        

    def __repr__(self):
        return '<Affiliate %r>' % (self.id)


class Schedule(db.Model):
    __tablename__ = 'Schedule'

    eventId = db.Column(db.String(1024), foreign_key=True)
    groupId = db.Column(db.String(1024), foreign_key=True)
    
    def __init__(self, eventId, groupId):
        self.eventId = eventId
        self.groupId = groupId
        

    def __repr__(self):
        return '<Schedule %r>' % (self.id)


class Submit(db.Model):
    __tablename__ = 'Submit'

    eventId = db.Column(db.String(1024), foreign_key=True)
    userId = db.Column(db.String(1024), foreign_key=True)
    
    def __init__(self, eventId, userId):
        self.eventId = eventId
        self.userId = userId
        

    def __repr__(self):
        return '<Submit %r>' % (self.id)