from app import db
from app.models import *
from datetime import date, time, timedelta

"""
USER
"""

def addUser(first_name = "fname" , last_name ="lname", password="testpassword", email="test@test.com", profile_photo="testprofile.png", created_at = date.today()):
    try:
        user = User(
            first_name, 
            last_name, 
            password, 
            email, 
            profile_photo, 
            created_at)
        db.session.add(user)
        db.session.commit()
    except:
        pass

"""
EVENT
"""

def addEvent(title ="Test Event", start_date = date.today(), end_date = date.today() + timedelta(days=7), description = "Just a test event", venue ="Test Venue", image = "testevent.jpg", website_url="testurl.com", status="pending", uid=None, created_at = date.today(), user_email = None, group_id = None):
    try:
        if(uid != None or user_email != None):
            # only add event if user id is present or email

            user  = None
            if(uid != None):
                # get the user object if id is present
                user = User.query.get(uid)
            else:
                # get the user usign the email
                user = User.query.filter_by(email=user_email).first()

            if(user == None): #exit if the user cannot be found
                print("-->user does not exist")
                return 0

            event = Event(
                title, 
                start_date, 
                end_date, 
                description, 
                venue, 
                image, 
                website_url, 
                status, 
                uid, 
                created_at)
            
            db.session.add(event)
            db.session.commit()

            group = None
            if( group_id == None):
                #add user to a new group
                group = Group(user.first_name+" new group", user.id)
                db.session.add(group)
                db.session.commit()

                # add user affiliation to group
                affiliate = Affiliate(user.id, group.id)
                db.session.add(affiliate)
                db.session.commit()


            else:
                # add the user to the group added. 
                # first check if the user is affiliated to a group 
                group = Group.query.get(group_id)
                affiliate = Affiliate.query.filter_by(userId = user.id, groupId = group.id).first()
                if( affiliate ==  None):
                    affiliate = Affiliate(user.id, group.id)
                    db.session.add(affiliate)
                    db.session.commit()
                    print(affiliate)
                

            
            schedule = Schedule(event.id, group.id)
            db.session.add(schedule)
            db.session.commit()

            submit = Submit(event.id, user.id)
            db.session.add(submit)
            db.session.commit()
        else:
            print("--> please submit a user ID")
    except:
        pass

"""
GROUP
"""

def addGroup(user_id, groupname):
    try:
        group = Group(groupname, user_id)
        db.session.add(group)
        db.session.commit()

        # add affiliates
        affil = Affiliate(user_id, group.id)
        db.session.add(affil)
        db.session.commit()
    except:
        pass

def addAffiliate(user_id, group_id):
    try:
        affil = Affiliate(user_id, group_id)
        db.session.add(affil)
        db.session.commit()
    except:
        pass