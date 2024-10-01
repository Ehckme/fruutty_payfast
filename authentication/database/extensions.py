from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from flask import session

"""--------     create OTP code to use for confirming the user
    by importing and using the random module    ------------------
"""
import random
def random_otp():
    otp = ''.join([str(random.randint(0000, 9999)) for i in range(1)])
    return otp

OTP = random_otp()

# create an inheritance class from DeclarativeBase
class Base(DeclarativeBase):
    pass

# instantiate database from sqlalchemy Base
db = SQLAlchemy(model_class=Base)






