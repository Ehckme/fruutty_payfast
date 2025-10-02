
"""------------ import modules for sqlalchemy and flask-sqlaclhemy  ------------"""
import datetime
# from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import String, Integer, CHAR, Column, ForeignKey
from sqlalchemy import Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Table
from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from .extensions import db
from .extensions import Base


""" --------------  Create a User Model, which is a table for Users with flask-sqlalchemy   ----------- 
"""

# 1
class Fruutty_token(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    token_id: Mapped[str] = mapped_column(String(30))
    initial_base_token: Mapped[str] = mapped_column(String(1000))
    available_tokens: Mapped[float] = mapped_column(String(1000), nullable=True, server_default='0.0')
    sold_tokens: Mapped[float] = mapped_column(String(30), nullable=True, server_default='0.0')
    opening_trade: Mapped[float] = mapped_column(String(30), nullable=True, server_default='0.0')
    closing_trade: Mapped[float] = mapped_column(String(30), nullable=True, server_default='0.0')
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Fruutty_token(id={self.id!r}, token_id={self.token_id!r}, ' \
               f'initial_base_token={self.initial_base_token}, available_tokens={self.available_tokens}, ' \
               f'sold_tokens={self.sold_tokens!r}, opening_trade={self.opening_trade!r}, ' \
               f'closing_trade={self.closing_trade!r}, date={self.date!r},'
    def __repr__(self) -> str:
        return f'Fruutty_token(id={self.id!r}, token_id={self.token_id!r}, ' \
               f'initial_base_token={self.initial_base_token}, available_tokens={self.available_tokens}, ' \
               f'sold_tokens={self.sold_tokens!r}, opening_trade={self.opening_trade!r}, ' \
               f'closing_trade={self.closing_trade!r}, date={self.date!r},'


# 2
# Create User a Table class
class Users(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30), nullable=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(CHAR(200))

    confirmed: Mapped[bool] = mapped_column(nullable=False, default=False)
    otp: Mapped[int] = mapped_column(nullable=True)
    confirmed_at: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, )
    signup_at: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())
    lastLogin_at: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, )
    lastLout_at: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, )
    fruutty_token: Mapped[float] = mapped_column(nullable=True, default=0)
    country: Mapped[str] = mapped_column(String(30), nullable=True)
    role: Mapped[str] = mapped_column(String(30), nullable=True, server_default='user')

    def __repr__(self) -> str:
        return f'Users(id={self.id!r}, user_id={self.user_id!r}, username={self.username!r}, ' \
               f'email={self.email!r}, password={self.password!r}, ' \
               f'confirmed={self.confirmed!r}, otp={self.otp!r}, confirmed_at={self.confirmed_at!r},' \
               f'signup_at={self.signup_at!r}, lastlogin_at={self.lastLogin_at!r},' \
               f'lastLogout_at={self.lastLout_at!r}, fruutty_token={self.fruutty_token!r},' \
               f'country={self.country!r}, role={self.role})'


# 3
class Fruutty_card_purchases(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30))
    purchase_id: Mapped[str] = mapped_column(String(30))

    card_number: Mapped[str] = mapped_column(String(100))
    card_type: Mapped[str] = mapped_column(String(30))
    card_holder_name: Mapped[str] = mapped_column(String(30))

    bank_name: Mapped[str] = mapped_column(String(30))
    branch_code: Mapped[str] = mapped_column(String(30))

    exp_month: Mapped[str] = mapped_column(String(30))
    exp_year: Mapped[str] = mapped_column(String(30))
    cvv: Mapped[str] = mapped_column(String(30))

    tokens: Mapped[str] = mapped_column(String(30))
    purchase_amount: Mapped[str] = mapped_column(String(30))


    country : Mapped[str] = mapped_column(String(30))
    city : Mapped[str] = mapped_column(String(30))
    currency: Mapped[str] = mapped_column(String(30))

    date : Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())
    processor : Mapped[str] = mapped_column(String(60))


    def __repr__(self) -> str:
        return f'Fruutty_card_purchases(id={self.id!r}, user_id={self.user_id!r}' \
               f'purchase_id={self.purchase_id!r}, card_number={self.card_number!r},' \
               f'card_type={self.card_type!r}, card_holder_name={self.card_holder_name!r} ' \
               f'bank_name={self.bank_name!r}, branch_code ={self.branch_code!r}),' \
               f'exp_month={self.exp_month!r}, exp_year={self.exp_year!r}, ' \
               f'cvv={self.cvv!r}, tokens={self.tokens!r}, purchase_amount={self.purchase_amount!r},' \
               f'country={self.country!r}, city={self.city!r}, currency={self.currency!r},' \
               f'date={self.date!r}, processor={self.processor!r},'

# 4
class User_tokens(db.Model, UserMixin):


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    user_id: Mapped[str] = mapped_column(String(30))
    token_id: Mapped[str] = mapped_column(String(30))
    availble_tokens: Mapped[str] = mapped_column(String(1000))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'User_tokens(id={self.id!r}, user_id={self.user_id!r}, ' \
               f'token_id={self.token_id!r}, availble_tokens={self.availble_tokens!r}, ' \
               f'date={self.date!r},'

# 7
class Fruutty_transactions(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30))
    token_id: Mapped[str] = mapped_column(String(30))
    token_type: Mapped[str] = mapped_column((String(1000)))
    product_name: Mapped[str] = mapped_column(String(30), nullable=True, default='N/A')
    store_name: Mapped[str] = mapped_column(String(30), nullable=True, default='N/A')
    token_amount: Mapped[str] = mapped_column((String(1000)))
    from_owner : Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Fruutty_transactions(id={self.id!r}, user_id={self.user_id!r}, ' \
               f'token_id={self.token_id!r}, token_type={self.token_type!r}, ' \
               f'product_name={self.product_name!r}, store_name={self.store_name!r}, ' \
               f'token_amount={self.token_amount!r}, from_owner={self.from_owner!r} ' \
               f'location={self.location!r}, date={self.date!r},'


# 8
class Ftvs(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    south_african_rand: Mapped[str] = mapped_column(String(30))
    united_states_dollar: Mapped[str] = mapped_column(String(30))
    british_pound: Mapped[str] = mapped_column((String(30)))
    kuwaiti_dinar: Mapped[str] = mapped_column(String(30))
    chinese_yuan: Mapped[str] = mapped_column(String(30))
    average: Mapped[str] = mapped_column((String(30)))
    total: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Ftvs(id={self.id!r}, south_african_rand={self.south_african_rand!r}, ' \
               f'united_states_dollar={self.united_states_dollar!r}, british_pound={self.british_pound!r}, ' \
               f'kuwaiti_dinar={self.kuwaiti_dinar!r}, chinese_yuan={self.chinese_yuan!r}, ' \
               f'average={self.average!r}, total={self.total!r}, ' \
               f'date={self.date!r},'

# 9
class Currencies(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country: Mapped[str] = mapped_column(String(30))
    symbol: Mapped[str] = mapped_column(String(30))
    value: Mapped[float] = mapped_column()
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Currencies(id={self.id!r}, country={self.country!r}, ' \
               f'symbol={self.symbol!r}, value={self.value!r}, ' \
               f'date={self.date!r},'


# 10
class Notifications(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30))
    notification_id: Mapped[str] = mapped_column(String(30))
    notification_type: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())


    def __repr__(self) -> str:
        return f'Notifications=(id={self.id!r}, user_id={self.user_id!r} ,' \
               f'notification_id={self.notification_id!r}, notification_type={self.notification_type!r},' \
               f'date={self.date!r} )'


# 11
class Received_tokens(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30))
    token_reference: Mapped[str] = mapped_column(String(30))
    token_amount: Mapped[str] = mapped_column(String(30))
    token_value: Mapped[str] = mapped_column(String(30))
    sender: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Received_tokens=(id={self.id!r}, user_id={self.user_id!r}, ' \
               f'token_reference={self.token_reference!r} ,' \
               f'token_amount={self.token_amount!r}, ' \
               f'token_value={self.token_value!r}, sender={self.sender!r},' \
               f'date={self.date!r} )'


# 12
class Sent_tokens(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30))
    token_reference: Mapped[str] = mapped_column(String(30))
    token_amount: Mapped[str] = mapped_column(String(30))
    token_value: Mapped[str] = mapped_column(String(30))
    receiver: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Sent_tokens=(id={self.id!r}, user_id={self.user_id!r}, ' \
               f'token_reference={self.token_reference!r} ,' \
               f'token_amount={self.token_amount!r}, ' \
               f'token_value={self.token_value!r}, receiver={self.receiver!r},' \
               f'date={self.date!r} )'


class Food(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    image_name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(60))
    link: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Food=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r} ,' \
               f'image_name={self.image_name!r},' \
               f'company_name={self.company_name}, link={self.link!r},' \
               f'date={self.date!r} )'


# 14
class Drive(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    image_name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(60))
    link: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Drive=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r} ,' \
               f'image_name={self.image_name!r}', \
               f'company_name={self.company_name}, link={self.link!r},' \
               f'date={self.date!r} )'


# 15
class Fashion(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    image_name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(60))
    link: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Fashion=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r},' \
               f'image_name={self.image_name!r},' \
               f'company_name={self.company_name}, link={self.link!r}, ' \
               f'date={self.date!r})'


# 16
class Tech(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    image_name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(60))
    link: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Tech=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r},' \
               f'image_name={self.image_name!r},' \
               f'company_name={self.company_name}, link={self.link!r},' \
               f'date={self.date!r} )'


# 17
class Music(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    audio_file_name: Mapped[str] = mapped_column(String(200))
    song_name: Mapped[str] = mapped_column(String(200))
    artist_name: Mapped[str] = mapped_column(String(60))
    artist_bio: Mapped[str] = mapped_column(String(250))
    record_company: Mapped[str] = mapped_column(String(100), nullable=True)
    image_link: Mapped[str] = mapped_column(String(500))
    song_link: Mapped[str] = mapped_column(String(500), server_default=None)
    lyrics: Mapped[str] = mapped_column(String(5000), server_default=None)
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Music=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r}, audio_file_name={self.audio_file_name!r},' \
               f'song_name={self.song_name!r},' \
               f'artist_name={self.artist_name!r}, artist_bio={self.artist_bio!r},' \
               f'record_company={self.record_company!r}, image_link={self.image_link!r}, ' \
               f'song_link={self.song_link!r}, lyrics={self.lyrics!r}, ' \
               f'date={self.date!r})'


class Applications(db.Model, UserMixin):
    __bind_key__ = "auth_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    """ Contact Email & mobile cell number """
    email: Mapped[str] = mapped_column(String(30))
    cell: Mapped[str] = mapped_column(String(30))
    """ Home Address """
    street_name: Mapped[str] = mapped_column(String(30))
    house_number: Mapped[str] = mapped_column(String(30))
    area_name: Mapped[str] = mapped_column(String(60))
    postal_code: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(60))
    province: Mapped[str] = mapped_column(String(60))
    country: Mapped[str] = mapped_column(String(60))
    """ Approve """
    approoved: Mapped[bool] = mapped_column(nullable=True, default=False)
    application_date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())
    approved_date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True,)

    def __repr__(self) -> str:
        return f'Applications(id={self.id!r}, name={self.name!r},' \
               f'surname={self.surname!r}, email={self.email!r}, ' \
               f'cell_no={self.cell!r}, street_name={self.street_name!r}' \
               f'house_number={self.house_number!r}, area_name={self.area_name!r},' \
               f'postal_code={self.postal_code!r}, city={self.city!r},' \
               f'province={self.province!r}, country={self.country!r},' \
               f'approoved={self.approoved!r}, application_date={self.application_date!r}' \
               f' approved_date={self.approved_date!r} )'

class Employees(db.Model, UserMixin):

    __bind_key__ = "auth_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    """ Contact Email & mobile cell number """
    email: Mapped[str] = mapped_column(String(30))
    cell: Mapped[str] = mapped_column(String(30))
    """ Employee Department & role """
    department: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f'Employees(id={self.id!r}, employee_id={self.employee_id!r},' \
               f'name={self.name!r}, surname={self.surname!r},' \
               f'email={self.email!r}, cell={self.cell!r},' \
               f'Department={self.department!r}, role={self.role!r}  )'



class Employee_address(db.Model, UserMixin):
    __bind_key__ = "auth_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    """ Home Address """
    street_name: Mapped[str] = mapped_column(String(30))
    house_number: Mapped[str] = mapped_column(String(30))
    area_name: Mapped[str] = mapped_column(String(60))
    postal_code: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(60))
    province: Mapped[str] = mapped_column(String(60))
    country: Mapped[str] = mapped_column(String(60))

    def __repr__(self) -> str:
        return f'Employee_address(id={self.id!r},' \
               f'employee_id={self.employee_id!r}, name={self.name!r},' \
               f'street_name={self.street_name!r}' \
               f'house_number={self.house_number!r}, area_name={self.area_name!r},' \
               f'postal_code={self.postal_code!r}, city={self.city!r},' \
               f'province={self.province!r}, country={self.country!r},'

"""
Create connection Tables for binds
"""


# Create User a Table class
class Employee_login(db.Model, UserMixin):
    __bind_key__ = "auth_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30), nullable=True)
    employee_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(CHAR(200))
    role: Mapped[str] = mapped_column(String(30), nullable=True)
    lastLogin_at: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, )
    lastLogout_at: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, )


    def __repr__(self) -> str:
        return f'Employee_login(id={self.id!r}, employee_id={self.employee_id!r}, ' \
               f'employee_name={self.employee_name!r}, ' \
               f'email={self.email!r}, password={self.password!r}, ' \
               f'role={self.role!r},' \
               f'lastlogin_at={self.lastLogin_at!r},' \
               f'lastLogout_at={self.lastLogout_at!r},)'
#19

class Admin_token_request(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30), nullable=True)
    employee_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30), nullable=True)
    token_request: Mapped[str] = mapped_column(String(30))
    token_amount: Mapped[str] = mapped_column(String(30))
    reference: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, server_default=func.now() )

    def __repr__(self) -> str:
        return f'Admin_token_request=(id={self.id!r}, employee_id={self.employee_id!r},' \
               f'employee_name={self.ememployee_name!r}, email={self.email!r},' \
               f'role={self.role!r}, token_request={self.token_request!r},' \
               f'token_amoun={self.token_amount!r}, reference={self.reference!r},' \
               f'date={self.date!r} )'

class Sales(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(40), nullable=True)
    upload_section: Mapped[str] = mapped_column(String(30))
    company: Mapped[str] = mapped_column(String(30))
    amount: Mapped[str] = mapped_column(String(30))
    discount: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, server_default=func.now())
    def __repr__(self) -> str:
        return f'Sales=(id={self.id!r}, employee_id={self.employee_id!r},' \
               f'upload_section={self.upload_section!r}, company={self.company!r}' \
               f'amount={self.amount!r}, date={self.date!r}),'


# PayFast section

class PayFastUsers(db.Model, UserMixin):
    __tablename__ = "payfast_users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    # add other fields if needed


class TokenPurchase(db.Model, UserMixin):
    __tablename__ = "token_purchases"
    id = Column(Integer, primary_key=True)
    user_email = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("payfast_users.id"), nullable=True)
    bundle_id = Column(Integer, nullable=True)  # optional
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(30), default="pending")
    payfast_ref = Column(String(255), nullable=True)
    m_payment_id = Column(String(128), nullable=True, unique=True)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        default=datetime.datetime.utcnow
    )

    user = relationship("PayFastUsers")


class QRToken(db.Model, UserMixin):
    __tablename__ = "qr_tokens"
    id = Column(Integer, primary_key=True)
    purchase_id = Column(Integer, ForeignKey("token_purchases.id"), nullable=False)
    token_code = Column(String(128), unique=True, nullable=False)
    token_value = Column(Numeric(12, 2), nullable=False)
    qr_path = Column(String(255), nullable=True)
    used = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), 
        nullable=False, 
        default=datetime.datetime.utcnow
    )

    purchase = relationship("TokenPurchase")

