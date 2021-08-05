from app.data_adder import *

# populate the database with fake data

addUser(
    first_name="John",
    last_name="paul",
    password="password",
    email="johnpaul@duroad.com",
)

addUser(
    first_name="Mary",
    last_name="Jane",
    password="password",
    email="maryjane@duroad.com",
)

addUser(
    first_name="bob",
    last_name="builder",
    password="password",
    email="bobbuilder@duroad.com",
)

addUser(
    first_name="Susan",
    last_name="smith",
    password="password",
    email="susansmith@duroad.com",
)

addUser(
    first_name="Greg",
    last_name="Miller",
    password="password",
    email="gregmiller@duroad.com",
)

addGroup(1, "Party Club")
addGroup(2, "Sport CLub")

addAffiliate(2, 1)
addAffiliate(3, 1)
addAffiliate(4, 1)
addAffiliate(1, 2)
addAffiliate(4, 2)
addAffiliate(5, 2)

addEvent(
    title="Movie and chill",
    description="enjoy a night chilling with friends",
    venue="sandwich theatre",
    uid=2,
    group_id=1
)

addEvent(
    title="Praise adn worship",
    description="Sing praises onto god sing praises ",
    venue="Party Concert",
    uid=1,
    group_id=1
)

addEvent(
    title="Dinner night",
    description="Eat until you drop",
    venue="Just food restaurant",
    uid=2,
    group_id=2
)

addEvent(
    title="Girls night out",
    description="The girls shall have fun",
    venue="All throughout the town",
    uid=4,
)