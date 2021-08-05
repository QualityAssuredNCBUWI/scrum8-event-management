import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory, abort, jsonify, g, make_response
# from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import datetime
from app.models import *
from app.forms import *
from app.jwt import *


###
# Routing for your application.
###

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
@requires_auth
def getAllEvent():
    if request.method == 'GET':
        event = db.session.query(Event).all()
        print(event)
        result = []
        if len(event) != 0:
            for e in event:
                id = e.id
                title = e.title
                description = e.description
                start_date = e.start_date
                end_date = e.end_date
                venue = e.venue
                website_url = e.website_url
                status = e.status
                image = e.image
                uid = e.uid
                cresult = {'id': id, "description": description, "title": title, "start_date": start_date, "end_date": end_date, "venue": venue, "website_url": website_url, "status": status, "image": image, "uid": uid}
                result.append(cresult)
            return jsonify({'result': result}), 200
        elif len(event) == 0: 
            return jsonify({"result": event}), 404

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


@app.route('/api/events/<id>', methods = ['GET'])
# @requires_auth
def getevent(id):
    event = Event.query.filter_by(id = id).all()  # .all() is used on the BaseQuery to return an array for the results, allowing us to evaluate if we got no reult

    if len(event) !=0:
        for e in event:
            eid = e.id
            description = e.description
            start_date = e.start_date
            end_date = e.end_date
            title = e.title
            venue = e.venue
            website_url = e.website_url
            status = e.status
            image = e.image
            uid = e.uid

        return jsonify({'id': eid, "description": description, "start_date": start_date, "end_date": end_date, "title": title, "venue": venue, "website_url": website_url, "status": status, "image": image, "uid": uid}), 200
    elif len(event) == 0: 
        return jsonify({"result": event}), 404
    # else:
    #     return jsonify({'result': "Access token is missing or invalid"}), 401
