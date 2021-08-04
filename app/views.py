"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory, abort, jsonify, g, make_response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Event, Affiliate, Schedule, Submit
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
#from datetime import datetime, timezone
import datetime

# Using JWT
import jwt
from flask import _request_ctx_stack
from functools import wraps
import datetime

"""                              JWT                          """
# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      # return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401
      return jsonify({'result': "Access token is missing or invalid"}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      # return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
      return jsonify({'result': "Access token is missing or invalid"}), 401
    elif len(parts) == 1:
      # return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
      return jsonify({'result': "Access token is missing or invalid"}), 401
    elif len(parts) > 2:
      # return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401
      return jsonify({'result': "Access token is missing or invalid"}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        # return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        return jsonify({'result': "Access token is missing or invalid"}), 401
    except jwt.DecodeError:
        # return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401
        return jsonify({'result': "Access token is missing or invalid"}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


###
# Routing for your application.
###
"""              API: AUTHENTICATION & SEARCH              """

# This route doesn't require a JWT
@app.route('/api/register', methods=['POST'])
def register(): 
    # if the request data is not there
    # or any of the username/password/name/email is missing
    # respond with a bad request code and stop registration
    # if not request.json: # or not 'username' in request.json or not 'password' in request.json or not 'name' in request.json or not 'email' in request.json:
    #    abort(400) #bad request http code
    #if not request.form: # or not 'username' in request.form or not 'password' in request.form or not 'name' in request.form or not 'email' in request.form:
     #  abort(400) #bad request http code

    if request.form: #TBD:update to check for essentials
        # get photo filename
        rawPhoto = request.files['photo']
        filename = secure_filename(rawPhoto.filename)
        rawPhoto.save(os.path.join(
            app.config['PROFILE_UPLOAD_FOLDER'], filename
        ))
        
        # check if user already exists in database
        if User.query.filter_by(username = request.form['username']).first() \
            or User.query.filter_by(email = request.form['email']).first():
                 return jsonify({'message': 'Username or email already exists.'}), 409
        else:
            # create user 
            user = User(
                first_name=request.form['firstname'],
                last_name=request.form['lastname'],
                password = request.form['password'], 
                email = request.form['email'],
                profile_photo = "../../../profileUploads/" + filename,
                created_at =  datetime.datetime.now(datetime.timezone.utc)
            )

            #add user to db
            db.session.add(user)
            db.session.commit()

            #get the user from the db
            newUser = User.query.filter_by(username = request.form['username']).first()

            #build api response with user data
            userResult = {
                'id': newUser.id, 
                'username': newUser.username,
                'firstname': newUser.firstname,
                'lastname': newUser.lastname,
                'email': newUser.email,
                'photo': newUser.photo,
                'created_at': newUser.created_at
            }
            
            #send api response
            # return jsonify({'user': userResult}), 201
            return jsonify({'id': newUser.id, \
                            'username': newUser.username,   \
                            'name''username': newUser.username,\
                            'firstname': newUser.firstname, \
                            'lastname': newUser.lastname, \
                            'email': newUser.email, \
                            'photo': newUser.photo,\
                            'created_at': newUser.created_at}), 201
    else:
    #    abort(400) #bad request http code
        return jsonify({'user': []}), 400


@app.route('/api/auth/login', methods=['POST'])
def login(): 
    if not request.json or not 'username' in request.json or not 'password' in request.json:
       abort(400) #bad request http code
    else:
        username = request.json['username']
        password = request.json['password']

        user = User.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            login_user(user)

            #generate JWT token
            payload = {
                'sub': user.id, #technical identifier of the user
                'name': user.name,
                'iat': datetime.datetime.now(datetime.timezone.utc), #current time -- generate timestamp
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10) #token expires in 10 mins -- generate timestamp
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

            # #build api response 
            # result = {
            #     'message': 'Login successful',
            #     'token': token
            # }

            #send api response
            return jsonify({'message': 'Login successful', 'token': token}), 200
        elif user is None or not check_password_hash(user.password, password):
            return jsonify({'message': 'Login unsuccessful'}), 404
        else:
            return jsonify({'message': 'Server may have encountered an error'}), 500
        

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/api/auth/logout', methods=['POST'])
@requires_auth
def logout(): 
    logout_user()
    #build api response 
    # result = {
    #     'message': 'Log out successful'
    # }

    return jsonify({'message': 'Log out successful'}), 200

"""              API: PROFILE MANAGEMENT              """

@app.route('/api/users/<user_id>', methods = ['GET'])
# @requires_auth
def getUser(user_id):
    user = User.query.filter_by(id = user_id).all()
    if len(user) !=0:
        for u in user:
            uid = u.id
            username = u.username
            name = u.name
            email = u.email
            location = u.location
            biography = u.biography
            photo = u.photo
            date_joined = u.date_joined

        # result = {'id': uid, "username": username, "password": password, "name": name, "email": email, "location": location, "biography": biography, "photo": photo, "date_joined": date_joined}
        # return jsonify({'result':result}), 200
        return jsonify({'id': uid, "username": username, "name": name, "email": email, "location": location, "biography": biography, "photo": photo, "date_joined": date_joined}), 200
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
@requires_auth
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
@requires_auth
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
        




# Please create all new routes and view functions above this route.
# This route is now our catch all route for our VueJS single page
# application.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    Because we use HTML5 history mode in vue-router we need to configure our
    web server to redirect all routes to index.html. Hence the additional route
    "/<path:path".
    Also we will render the initial webpage and then let VueJS take control.
    """
    return render_template('index.html')


@app.route('/profileUploads/<filename>')
def get_profile_image(filename):
    return send_from_directory(os.path.join('..', app.config['PROFILE_UPLOAD_FOLDER']), filename)

@app.route('/eventUploads/<filename>')
def get_event_image(filename):
    return send_from_directory(os.path.join('..', app.config['EVENT_UPLOAD_FOLDER']), filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port="8079")
