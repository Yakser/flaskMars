import sqlalchemy
from data import db_session
from data.jobs import Jobs
from data.users import User

db_name = input()
db_session.global_init(db_name)
db_sess = db_session.create_session()

[print(i) for i in db_sess.query(User).filter(User.address == "module_1",
                                              User.speciality.notlike('%engineer%'),
                                              User.position.notlike('%engineer%')).all()]

# query
# # Created by Sergey Yaksanov at 02.03.2021
# Copyright © 2020 Yakser. All rights reserved.
