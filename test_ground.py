from app import app
from app import db
from app.models import *
from app.data_adder import *


if __name__ == '__main__':
    # addUser(email="test2@test.com")
    # addEvent(uid=3)
    # addGroup(4, "another group")
    addAffiliate(4, 3)
    pass