import os, re
from app import app, db
from flask import request,url_for, send_from_directory, abort, jsonify, g, make_response
# from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone
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
        rawPhoto = request.files['profile_photo']
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
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                password = request.form['password'],
                email = request.form['email'],
                profile_photo = filename,
                created_at =  datetime.now(timezone.utc)
            )

            #add user to db
            db.session.add(user)
            db.session.commit()

            #build api response with user data
            userResult = {
                'message':"User created successfully",
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
                'iat': datetime.now(timezone.utc), #current time -- generate timestamp
                'exp': datetime.now(timezone.utc) + timedelta(minutes=60) #token expires in 10 mins -- generate timestamp
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
@requires_auth
def getUser(user_id):
    try:
        if (not isinstance(user_id, int) and not user_id.isnumeric()): 
            return jsonify({"message":"Invalid user ID"}),406

        user = User.query.get(user_id)
        if(user is None): 
            return jsonify({"message":"user is unavailable"}),404
        
        user_response = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "profile_photo": user.profile_photo,
            "created_at": user.created_at
        }

        return jsonify({
            "status": "user found",
            "user": user_response
        }), 200
    except:
        pass
    return jsonify({"message":"An error occured"}),400


@app.route('/api/users/current', methods = ['GET'])
@requires_auth
def getCurrentUser():
    try:
        user_id = g.current_user['sub']
        if (not isinstance(user_id, int) and not user_id.isnumeric()): 
            return jsonify({"message":"Invalid user ID"}),406

        user = User.query.get(user_id)
        if(user is None): 
            return jsonify({"message":"user is unavailable"}),404
        
        user_response = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "profile_photo": user.profile_photo,
            "created_at": user.created_at
        }

        return jsonify({
            "status": "user found",
            "user": user_response
        }), 200
    except:
        pass
    return jsonify({"message":"An error occured"}),400


@app.route('/api/users/current', methods = ['PUT'])
@requires_auth
def updateCurrentUser():
    try:
        if request.form or request.files:
            error_found = False
            errors = []

            user_id = g.current_user['sub']
            if (not isinstance(user_id, int) and not user_id.isnumeric()): 
                return jsonify({"message":"Invalid user ID"}),406

            user = User.query.get(user_id)
            if(user is None):
                return jsonify({"message":"user is unavailable"}),404
            
            # update each user field if its available
            if('photo' in request.files):
                rawPhoto = request.files['photo']
                filename = secure_filename(rawPhoto.filename)
                rawPhoto.save(os.path.join(
                    app.config['PROFILE_UPLOAD_FOLDER'], filename
                ))
                user.profile_photo = filename
            
            # update firstname
            if('firstname' in request.form):
                user.first_name = request.form['firstname']
            
            # update lastname
            if('lastname' in request.form):
                user.last_name = request.form['lastname']
            
            # update email
            if('email' in request.form):
                if('confirm_email' in request.form):
                    if(request.form['email'] == request.form['confirm_email']):
                        user.email = request.form['email']
                    else:
                        error_found = True
                        errors.append("The emails are different")
                else:
                    error_found = True
                    errors.append("The ( confirm_email ) field is required")
            
            # update password
            if('password' in request.form):
                if('confirm_password' in request.form):
                    if(request.form['password'] == request.form['confirm_password']):
                        user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256') 
                    else:
                        error_found = True
                        errors.append("The passwords are different")
                else:
                    error_found = True
                    errors.append("The ( confirm_password ) field is required")
            
            if(error_found):
                return jsonify({
                    "message": "Incorrect or missing fields",
                    "errors": errors
                }), 406

            db.session.commit()

            user_response = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "profile_photo": user.profile_photo,
                "created_at": user.created_at
            }

            return jsonify({
                "message": "user updated",
                "user": user_response
            }), 200
    except:
        pass
    return jsonify({"status":"An error occured"}),400


@app.route('/api/users/<user_id>', methods = ['PUT']) #update user endpoint
@requires_auth #ensure the user is logged in
def updateUser(user_id):
    try:
        if request.form:
            error_found = False
            errors = []

            if (not isinstance(user_id, int) and not user_id.isnumeric()): 
                return jsonify({"message":"Invalid user ID"}),406

            user = User.query.get(user_id)
            if(user is None): 
                return jsonify({"message":"user is unavailable"}),404
            
            # update each user field if its available
            if('photo' in request.files):
                rawPhoto = request.files['photo']
                filename = secure_filename(rawPhoto.filename)
                rawPhoto.save(os.path.join(
                    app.config['PROFILE_UPLOAD_FOLDER'], filename
                ))
                user.profile_photo = filename
            
            # update firstname
            if('firstname' in request.form):
                user.first_name = request.form['firstname']
            
            # update lastname
            if('lastname' in request.form):
                user.last_name = request.form['lastname']
            
            # update email
            if('email' in request.form):
                if('confirm_email' in request.form):
                    if(request.form['email'] == request.form['confirm_email']):
                        user.email = request.form['email']
                    else:
                        error_found = True
                        errors.append("The emails are different")
                else:
                    error_found = True
                    errors.append("The ( confirm_email ) field is required")
            
            # update password
            if 'password' in request.form and 'old_password' in request.form:
                if check_password_hash(user.password, request.form['old_password']):
                    if 'confirm_password' in request.form:
                        if(request.form['password'] == request.form['confirm_password']):
                            user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256') 
                        else:
                            error_found = True
                            errors.append("The passwords are different")
                    else:
                        error_found = True
                        errors.append("The ( confirm_password ) field is required")
                else:
                    error_found = True
                    errors.append("Incorrect old password")
            
            if(error_found):
                return jsonify({
                    "message": "Incorrect or missing fields",
                    "errors": errors
                }), 406

            db.session.commit()

            user_response = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "profile_photo": user.profile_photo,
                "created_at": user.created_at
            }

            return jsonify({
                "message": "user updated",
                "user": user_response
            }), 200
    except:
        pass
    return jsonify({"message":"An error occured"}),400


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
@requires_auth
def addEvents():
    if request.form:
        # check if the group exist 
        if( Group.query.get(request.form["group_id"]) is None): 
            return jsonify({"message":"group not found"}), 404
        
        #check if the user is in group
        if(Affiliate.query.filter_by(userId=g.current_user['sub'], groupId=request.form["group_id"]).first() is None):
            return jsonify({"message": "User is not in group"}), 403 
        
        # get photo filename
        rawEventPhoto = request.files['images']
        eventFilename = secure_filename(rawEventPhoto.filename)
        rawEventPhoto.save(os.path.join(
            app.config['EVENT_UPLOAD_FOLDER'], eventFilename
        ))
        # check if event already exists in database 
        # for a user to add a event, it must have at least one attribute that differs from all other events
        event = None
    
        if Event.query.filter_by(description = request.form['description']).first() \
            and Event.query.filter_by(start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")).first() \
            and Event.query.filter_by(end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d")).first() \
            and Event.query.filter_by(title = request.form['title']).first() \
            and Event.query.filter_by(venue = request.form['venue']).first() \
            and Event.query.filter_by(website_url = request.form['websiteurl']).first() \
            and Event.query.filter_by(uid = g.current_user['sub']).first() \
            and Event.query.filter_by(image = eventFilename).first():
                return jsonify({'message': 'Event already exists.'}), 409
        else:
            event = Event(
                title = request.form['title'],
                description = request.form['description'],
                start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d"),
                end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d"),
                venue = request.form['venue'],
                website_url = request.form['websiteurl'],
                status = "pending",
                image = eventFilename,
                uid = g.current_user['sub'],
                created_at= datetime.now(timezone.utc)
            )
            print("here")

            #add event to db
            db.session.add(event)
            db.session.commit()

            schedule = Schedule(event.id, request.form["group_id"])
            db.session.add(schedule)
            db.session.commit()

            submit = Submit(event.id, g.current_user['sub'])
            db.session.add(submit)
            db.session.commit()

            event_response = {
                'id': event.id, 
                'description': event.description,  'start_date': event.start_date,   
                'end_date': event.end_date, 
                'title': event.title,
                'venue': event.venue,  
                'website_url': event.website_url,
                'status': event.status, 
                'image': event.image,  
                'user_id': event.uid
            }

            #send api response
            # return jsonify({'event': eventResult}), 201
            return jsonify({
                "message":"event added",
                "group_id": request.form["group_id"],
                "event": event_response
                }), 201
    return jsonify({"message":"An error occured", 'event': []}), 400


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


@app.route('/api/events/<event_id>', methods = ['PUT']) #update user endpoint
@requires_auth #ensure the user is logged in
def updateEvent(event_id):
    # event= Event.query.filter_by(id=event_id).first()
    schedule = Schedule.query.filter_by(eventId=event_id).first()
    group = Group.query.filter_by(id=schedule.groupId).first()
    # check if the current user it the admin for the group responsible for the event
    if g.current_user['sub'] == group.admin:
        # {title, start_date, end_date, description, venue, websiteurl, status}= request.form
        data = request.form
        event = Event.query.filter_by(id=event_id).first()
        # event.start_date = data.start_date
        # event.end_date = data.end_date
        # event.description = data.description
        # event.venue = data.venue
        # event.websiteurl = data.websiteurl
        event.status = data['status']
        db.session.commit()
        # event.status = 'Published'
        return jsonify({'id': event.id, 'status': event.status})
    else:
        return jsonify({'message': 'Not allowed'}), 400

@app.route('/api/events/<event_id>', methods = ['DELETE']) 
@requires_auth
def removeEvent(event_id):
    schedule = Schedule.query.filter_by(eventId=event_id).first()
    if schedule is not None:
        group = Group.query.filter_by(id=schedule.groupId).first()
        if group is not None:
            if g.current_user['sub'] == group.admin:
                event = Event.query.filter_by(id=event_id).first()
                schedule = Schedule.query.filter_by(eventId=event_id).first()
                submit = Submit.query.filter_by(eventId=event_id).first()

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

                db.session.delete(schedule)
                db.session.delete(submit)
                db.session.delete(event)
            
                db.session.commit()
                if( Event.query.filter_by(id=event_id).first() is not None or Schedule.query.filter_by(eventId=event_id).first() is not None or Submit.query.filter_by(eventId=event_id).first() is not None):
                    return ({'result': 'Unable to delete event'}), 400  
                else:
                    return jsonify({'message': 'Event deleted.', 'result':{'id': eid, "description": description, "start_date": start_date, "end_date": end_date, "title": title, "venue": venue, "website_url": website_url, "status": status, "image": image, "uid": uid}}), 200
            else:
                return jsonify({'result': 'You are not the admin for this group.'}), 401
            return jsonify({"message": 'Event not found'}), 404  
    else:
        return jsonify({"message": 'Event not found'}), 404   

@app.route('/api/events/groups/<group_id>/pending', methods = ['GET']) #update user endpoint
@requires_auth #ensure the user is logged in
def getPending(group_id):
    try:
        user_id = g.current_user['sub']
        if (not isinstance(user_id, int) and not user_id.isnumeric()): 
            return jsonify({"message":"Invalid user ID"}),406

        if (not isinstance(group_id, int) and not group_id.isnumeric()): 
            return jsonify({"message":"Invalid group ID"}),406 
        
        group = Group.query.get(group_id)
        if ( group == None): 
            return jsonify({"message":"Group unavailable"}),404

        # check if the user is the group admin
        if(group.admin != user_id):
            return jsonify({"message":"User is not the group admin"}),401

        # get the events if the group exist
        schedules = Schedule.query.filter_by(groupId = group_id).all()

        events = []

        for schedule in schedules:
            event = Event.query.get(schedule.eventId)
            if(event.status == "pending"):
                events.append({
                    'id': event.id,
                    'title': event.title,
                    'start_date': event.start_date,
                    'end_date': event.end_date,
                    'description': event.description,
                    'venue': event.venue,
                    'image': event.image,
                    'website_url': event.website_url,
                    'status': event.status,
                    'user_id': event.uid,
                    'created_date': event.created_at
                })

        return jsonify({"message": "events", "group": group_id, "events":events})
    except:
        pass

    return jsonify({"message":"an error occured"})
            

@app.route('/api/events/groups/<group_id>', methods= ['GET'])
def getEventsInGroup(group_id): 
    try:
        if (not isinstance(group_id, int) and not group_id.isnumeric()): abort(400)

        if ( Group.query.get(group_id) == None): 
            return jsonify({"message":"Group unavailable"}),404
        
        # get the evnts if the group exist
        schedules = Schedule.query.filter_by(groupId = group_id).all()

        events = []

        for schedule in schedules:
            event = Event.query.get(schedule.eventId)
            if(event.status == "active"):
                events.append({
                    'id': event.id,
                    'title': event.title,
                    'start_date': event.start_date,
                    'end_date': event.end_date,
                    'description': event.description,
                    'venue': event.venue,
                    'image': event.image,
                    'website_url': event.website_url,
                    'status': event.status,
                    'user_id': event.uid,
                    'created_date': event.created_at
                })

        return jsonify({"message": "events", "group": group_id, "events":events})
    except:
        pass

    return jsonify({"message":"an error occured"})
    

"""              API: Group              """
@app.route('/api/groups/addMember', methods = ['POST'])
@requires_auth
def addMember():
    # ! should i get the email from a for field or should it just be passed in?
    # Check if the logged in user is the admin of the group they want to add the user to 
    # get admin of group thru id
    email = request.form['email']
    groupid = request.form['group']

    group = db.session.query(Group).filter_by(id=groupid).first()
    admin = group.admin

    
    # Check if the member exists    
    # memberExists = db.session.query(db.exists().where(User.email==email)).scalar()
    member = db.session.query(User).filter_by(email=email).first()

    if admin == g.current_user['sub']: 
        if member is not None:
            # Check if the member already exist in the affiliate table
            if Affiliate.query.filter_by(userId=member.id, groupId=group.id).first():
                return jsonify({'message': 'User already a member'}), 409
            else:
                # Update the affiliation table with the new member 
                affiliate=  Affiliate(
                    userId= member.id,
                    groupId=group.id
                )

                # Add member to Affiliation in db
                db.session.add(affiliate)
                db.session.commit()

                # get the new member just added
                newMember = Affiliate.query.filter_by(userId=member.id, groupId=group.id).first()

                # build jsonify response
                return jsonify({'userId': newMember.userId, 'groupId': newMember.groupId}), 201
        else:
            return jsonify({'message': 'Member with email address ' + email + ' does not exist'}), 400
    else:
        return jsonify({'message': 'Must be logged into an active session and be admin of group'}), 400


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

           # Check if the member already exist in the affiliate table
            if Affiliate.query.filter_by(userId=g.current_user['sub'], groupId=newgroup.id).first():
                return jsonify({'message': 'User already a member'}), 409
            else:
                # Update the affiliation table with the new member 
                affiliate=  Affiliate(
                    userId= g.current_user['sub'],
                    groupId=newgroup.id
                )

                # Add member to Affiliation in db
                db.session.add(affiliate)
                db.session.commit()
            # build jsonify response
            return jsonify({'id': newgroup.id, 'name': newgroup.name, 'admin': newgroup.admin}), 201

    else:
            return jsonify({'Group': []}), 400
