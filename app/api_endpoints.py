import os, re
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory, abort, jsonify, g, make_response
# from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models import *
# from app.forms import *
from app.jwt import *


# Used to validate dates
r = re.compile('(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[- /.](19|20)\d\d')


"""              API: AUTHENTICATION & SEARCH              """

# This route doesn't require a JWT
@app.route('/api/register', methods=['POST'])
def register(): 
    if request.form : #TBD:update to check for essentials
        # get photo filename
        rawPhoto = request.files['photo']
        filename = secure_filename(rawPhoto.filename)
        rawPhoto.save(os.path.join(
            app.config['PROFILE_UPLOAD_FOLDER'], filename
        ))
        
        # check if user already exists in database
        if User.query.filter_by(email = request.form['email']).first():
                 return jsonify({'message': 'Email already exists.'}), 409
        else:
            # create user 
            user = User(
                first_name=request.form['firstname'],
                last_name=request.form['lastname'],
                password = request.form['password'], 
                email = request.form['email'],
                profile_photo = filename,
                created_at =  datetime.datetime.now(datetime.timezone.utc)
            )

            #add user to db
            db.session.add(user)
            db.session.commit()

            #build api response with user data
            userResult = {
                'status':"User created successfully",
                'id': user.id, 
                'firstname': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'created_at': user.created_at
            }
            
            #send api response
            return jsonify(userResult), 201
    else:
        return jsonify({'user': []}), 400

@app.route('/api/auth/login', methods=['POST'])
def login(): 
    if not request.json or not 'email' in request.json or not 'password' in request.json:
       abort(400) #bad request http code
    else:
        email = request.json['email']
        password = request.json['password']

        user = User.query.filter_by(email=email).first()

        if user is not None and check_password_hash(user.password, password):
            # login_user(user)

            #generate JWT token
            payload = {
                'sub': user.id, #technical identifier of the user
                'email': user.email,
                'iat': datetime.datetime.now(datetime.timezone.utc), #current time -- generate timestamp
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60) #token expires in 10 mins -- generate timestamp
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

            #send api response
            return jsonify({'message': 'Login successful', 'token': token}), 200
        elif user is None or not check_password_hash(user.password, password):
            return jsonify({'message': 'Login unsuccessful'}), 404
        else:
            return jsonify({'message': 'Server may have encountered an error'}), 500
        
@app.route('/api/auth/logout', methods=['POST'])
@requires_auth
def logout(): 
    spoiltoken = JWTBlacklist(g.current_token)
    db.session.add(spoiltoken)
    db.session.commit()
    
    # logout_user()
    return jsonify({'message': 'Log out successful'}), 200


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))



"""              API: PROFILE MANAGEMENT              """

@app.route('/api/users/<user_id>', methods = ['GET'])
# @requires_auth
def getUser(user_id):
    user = User.query.filter_by(id = user_id).all()
    if len(user) !=0:
        for u in user:
            uid = u.id
            first_name = u.first_name
            last_name = u.last_name
            email = u.email
            photo = u.profile_photo
            created_at = u.created_at

        # result = {'id': uid, "username": username, "password": password, "name": name, "email": email, "location": location, "biography": biography, "photo": photo, "date_joined": date_joined}
        # return jsonify({'result':result}), 200
        return jsonify({'id': uid, "first_name": first_name, "last_name": last_name, "email": email, "photo": photo, "created_at": created_at}), 200
    elif len(user) == 0: 
        return jsonify({"result": user}), 404
    # else:
    #     # idealy need to figure out how to check the user is authenticated and token valid for a 401
    #     return jsonify({'result': "Access token is missing or invalid"}), 401



"""              API: Events              """

@app.route('/api/events', methods = ['GET'])
def get_all_events():
    """
        Get all events that match the filters for start and end date and title if they exist.
    """
    if request.method == 'GET':
        start = request.args.get('start_date')
        if start is None:
            start = ''
        end = request.args.get('end_date')
        if end is None:
            end = ''
        title = request.args.get('title')
        if start == '' and end == '' and title is None:
            events = db.session.query(Event).all()
            print(1)
        elif r.match(start) is not None and r.match(end) is not None and title is not None:
            start = datetime.strptime(start, '%d-%m-%Y')
            end = datetime.strptime(end, '%d-%m-%Y')
            events = Event.query.filter(Event.end_date>=end).filter(Event.start_date>=start).filter_by(title=title).all()
            print(2)
        elif r.match(start) is not None and r.match(end) is not None and title is None:
            start = datetime.strptime(start, '%d-%m-%Y')
            end = datetime.strptime(end, '%d-%m-%Y')
            events = Event.query.filter(Event.end_date <= end).filter(Event.start_date >= start).all()
            print(3)
        elif r.match(start) is not None and r.match(end) is None and title is None:
            start = datetime.strptime(start, '%d-%m-%Y')
            events = Event.query.filter(Event.start_date >= start).all()
            print(4)
        elif r.match(start) is None and r.match(end) is not None and title is None:
            end = datetime.strptime(end, '%d-%m-%Y')
            events = Event.query.filter(Event.end_date <= end).all()
            print(5)
        elif r.match(start) is None and r.match(end) is None and title is not None:
            events = Event.query.filter_by(title=title).all()
            print(6)
        elif r.match(start) is None and r.match(end) is None and title is None:
            return jsonify({"message": "Invalid query parameters, Dates should be formatted as dd-mm-yyyy"}), 400
        else:
            return jsonify({"message": "Invalid query parameters, Dates should be formatted as dd-mm-yyyy"}), 400
        result = []
        if len(events) != 0:
            for event in events:
                eid = event.id
                title = event.title
                description = event.description
                start_date = event.start_date
                end_date = event.end_date
                venue = event.venue
                website_url = event.website_url
                status = event.status
                image = event.image
                uid = event.uid
                event = {'id': eid, "description": description, "title": title, "start_date": start_date, "end_date": end_date, "venue": venue, "website_url": website_url, "status": status, "image": image, "uid": uid}
                result.append(event)
            return jsonify({'result': result}), 200
        return jsonify({"message": "No events found."}), 404

@app.route('/api/events', methods = ['POST'])
# @requires_auth
def addEvents():
    if request.form:
        # get photo filename
        rawEventPhoto = request.files['image']
        eventFilename = secure_filename(rawEventPhoto.filename)
        rawEventPhoto.save(os.path.join(
            app.config['EVENT_UPLOAD_FOLDER'], eventFilename
        ))
        
        eventPhotoPath = "../../../eventUploads/" + eventFilename

        # check if event already exists in database 
        # for a user to add a event, it must have at least one attribute that differs from all other events
        if Event.query.filter_by(description = request.form['description']).first() \
            and Event.query.filter_by(start_date = request.form['start_date']).first() \
            and Event.query.filter_by(end_date = request.form['end_date']).first() \
            and Event.query.filter_by(title = request.form['title']).first() \
            and Event.query.filter_by(venue = request.form['venue']).first() \
            and Event.query.filter_by(website_url = request.form['website_url']).first() \
            and Event.query.filter_by(status = request.form['status']).first() \
            and Event.query.filter_by(uid = request.form['uid']).first() \
            and Event.query.filter_by(image = eventPhotoPath).first():
                return jsonify({'message': 'Event already exists.'}), 409
        else:
            event = Event(
                description = request.form['description'],
                start_date = request.form['start_date'],
                end_date = request.form['end_date'],
                title = request.form['title'],
                venue = request.form['venue'],
                website_url = request.form['website_url'],
                status = request.form['status'],
                image = eventPhotoPath,
                uid = request.form['uid']
            )

            #add event to db
            db.session.add(event)
            db.session.commit()

            #get the event from the db (using description, user_id and photo to identify)
            newEvent = Event.query.filter_by(description = request.form['description']) \
                                .filter_by(uid = request.form['uid']) \
                                .filter_by(image = eventPhotoPath) \
                                .first()

            #send api response
            # return jsonify({'event': eventResult}), 201
            return jsonify({'id': newEvent.id, 
                            'description': newEvent.description,  \
                            'start_date': newEvent.start_date,    \
                            'end_date': newEvent.end_date,    \
                            'title': newEvent.title,  \
                            'venue': newEvent.venue,    \
                            'website_url': newEvent.website_url,    \
                            'status': newEvent.status,    \
                            'image': newEvent.image,  \
                            'uid': newEvent.uid}), 201
    else:
    #    abort(400) #bad request http code
        return jsonify({'event': []}), 400


@app.route('/api/events/<event_id>', methods = ['GET'])
@requires_auth
def getevent(event_id):
    event = Event.query.filter_by(id=event_id).first()
     # .all() is used on the BaseQuery to return an array for the results,
     # allowing us to evaluate if we got no reult
    if event is not None:
        eid = event.id
        description = event.description
        start_date = event.start_date
        end_date = event.end_date
        title = event.title
        venue = event.venue
        website_url = event.website_url
        status = event.status
        image = event.image
        uid = event.uid

        return jsonify({'id': eid, "description": description, "start_date": start_date, "end_date": end_date, "title": title, "venue": venue, "website_url": website_url, "status": status, "image": image, "uid": uid}), 200
    elif event is None:
        return jsonify({"message": "No event found."}), 404  



@app.route('/api/events/<event_id>', methods = ['PUT'])
@requires_auth
def updateEvent(event_id):


    # event= Event.query.filter_by(id=event_id).first()
    schedule = Schedule.query.filter_by(eventId=event_id).first()
    group = Group.query.filter_by(id=schedule.groupId)
    if g.current_user['sub'] == group.admin:
        # {title, start_date, end_date, description, venue, websiteurl, status}= request.form
        data = request.form
        event = Event.query.filter_by(id=event_id).first()
        event.start_date = data.start_date
        event.end_date = data.end_date
        event.description = data.description
        event.venue = data.venue
        event.websiteurl = data.websiteurl
        event.status = data.status
        db.session.commit()
        # event.status = 'Published'
        # return jsonify({'id': event.id, 'status': event.status})
    else:
        return jsonify({'result': 'Not allowed'}), 400

        

"""              API: Group              """
@app.route('/api/groups/<groupId>,<email>', methods = ['POST'])
@requires_auth
def addMember(groupId, email):
    # ! should i get the email from a for field or should it just be passed in?
    # Check if the logged in user is the admin of the group they want to add the user to 
    isAdmin = db.session.query(db.exists().where(Group.id == groupId, Group.admin==g.current_user['sub'])).scalar()
    # Check if the member exists    
    memberExists = db.session.query(db.exists().where(User.email==email)).scalar()
    
    if isAdmin == True: 
        if memberExists==True:
            member = User.query.filter_by(email=email).first()
            # Check if the member already exist in the affiliate table
            if Affiliate.query.filter_by(userId=member.id):
                return jsonify({'message': 'User already a member'}), 409
            else:
                # Update the affiliation table with the new member 
                affiliate=  Affiliate(
                    userId= member.id,
                    groupId=groupId
                )

                # Add member to Affiliation in db
                db.session.add(affiliate)
                db.session.commit()

                # get the new member just added
                newMember = Affiliate.query.filter_by(userId=member.id).first()

                # build jsonify response
                return jsonify({'userId': newMember.userId, 'groupId': newMember.groupId}), 201
        else:
            return jsonify({'message': 'Member with email address ' + email + ' does not exist'}), 400
    else:
        return jsonify({'message': 'Must be logged into an active session and be admin of group'}), 400


# @app.route('/api/groups/<groupId>,<eventId>', methods = ['POST'])
# @requires_auth
def attachEventToGroup(groupId, eventId):
    # Check if event, group mapping already exists in the schedule table
    if Schedule.query.filter_by(eventId=eventId, groupId=groupId):
        return jsonify({'message': 'Event already attached to group'}), 409
    else:
        schedule=Schedule(
            eventId=eventId,
            groupId=groupId
        )

        # Add member to Affiliation in db
        db.session.add(schedule)
        db.session.commit()

        # get the new member just added
        neweventgroup = Schedule.query.filter_by(eventId=eventId, groupId=groupId).first()

        # build jsonify response
        return jsonify({'eventId': neweventgroup.eventId, 'groupId': neweventgroup.groupId}), 201

@app.route('/api/groups', methods = ['POST'])
@requires_auth
def createGroup():    
    if request.form:
        groupName= request.form['name']
        # check if the group already exists with that name
        if Group.query.filter_by(name=groupName).first():
            return jsonify({'Error': 'Group already exists with that name'}), 409
        else:
            # create Group
            group = Group(
                name= request.form['name'],
                admin=g.current_user['sub']
            )
            
            # Add member to Affiliation in db
            db.session.add(group)
            db.session.commit()

            # get the new member just added
            newgroup = Group.query.filter_by(name=groupName).first()

            # build jsonify response
            return jsonify({'id': newgroup.id, 'name': newgroup.name, 'admin': newgroup.admin}), 201

    else:
            return jsonify({'Group': []}), 400
