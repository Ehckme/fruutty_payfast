"""
The following below code is for connecting  to an existing
database and creating new table using SQLAlchemy 2.22 version
It inherits from sqlalchemy.orm DeclarativeBase

Please check for latest version updates and update when necessary!

"""

# import SQLAlchemy
from __future__ import annotations
import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from typing import List
from sqlalchemy import ForeignKey, String, Integer, CHAR, Boolean, Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy import Table, create_engine
from sqlalchemy.orm import Session


from uconra.register import Register, random_chars
import sys
sys.path
print(sys.path)

sys.path.insert(0,'/home/ehckme/Desktop/fruutty/')
"""
import config
Config = config.Config
"""

from config import Config



# create an inheritance class from declarativeBase
class Base(DeclarativeBase):
    pass


# Create an association tabele for both tables to merge
# note for a Core table, we use the sqlalchemy.column construct
# not sqlalchemy.orm.mapped_column


# 1
class Fruutty_token(Base):
    __tablename__ = 'fruutty_token'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    token_id: Mapped[str] = mapped_column(String(30))
    initial_base_token: Mapped[str] = mapped_column(String(1000))
    available_tokens: Mapped[float] = mapped_column(String(1000), nullable=True, server_default='0.0')
    sold_tokens: Mapped[float] = mapped_column(String(30), nullable=True, server_default='0.0')
    opening_trade: Mapped[float] = mapped_column(String(30), nullable=True, server_default='0.0')
    closing_trade: Mapped[float] = mapped_column(String(30), nullable=True, server_default='0.0')
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Fruutty_token(id={self.id!r}, token_id={self.token_id!r}, ' \
               f'initial_base_token={self.initial_base_token}, available_tokens={self.available_tokens}, ' \
               f'sold_tokens={self.sold_tokens!r}, opening_trade={self.opening_trade!r}, ' \
               f'closing_trade={self.closing_trade!r}, date={self.date!r},'





# 2
# Create User a Table class
class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(30), nullable=True)
    username: Mapped[str] = mapped_column(String(30))
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
               f'country={self.country!r}, role={self.role} '



# 3
class Fruutty_card_purchases(Base):
    __tablename__ = 'fruutty_card_purchases'
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
class User_tokens(Base):
    __tablename__ = 'user_tokens'

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





# 5
class Fruutty_transactions(Base):
    __tablename__ = 'fruutty_transactions'

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
               f'token_amount={self.token_amount!r}, from_owner={self.from_owner!r}, ' \
               f'location={self.location!r}, date={self.date!r},'


# 6
class Ftvs(Base):
    __tablename__ = 'ftvs'

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

# 7
class Currencies(Base):
    __tablename__ = 'currencies'

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

# 8
class Notifications(Base):
    __tablename__ = 'notifications'

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

# 9
class Received_tokens(Base):
    __tablename__ = 'received_tokens'

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

# 10
class Sent_tokens(Base):
    __tablename__ = 'sent_tokens'

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
# 11

class Food(Base):
    __tablename__ = 'food'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    image_name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(60))
    link: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Food=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r},' \
               f'image_name={self.image_name!r},' \
               f'company_name={self.company_name}, link={self.link!r}, ' \
               f'date={self.date!r})'


# 12
class Drive(Base):
    __tablename__ = 'drive'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30))
    image_name: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[str] = mapped_column(String(60))
    link: Mapped[str] = mapped_column(String(500))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f'Drive=(id={self.id!r}, ' \
               f'employee_id={self.employee_id!r},' \
               f'image_name={self.image_name!r},' \
               f'company_name={self.company_name}, link={self.link!r}, ' \
               f'date={self.date!r})'



# 13
class Fashion(Base):
    __tablename__ = 'fashion'

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


# 14
class Tech(Base):
    __tablename__ = 'tech'

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
               f'company_name={self.company_name}, link={self.link!r}, ' \
               f'date={self.date!r})'


# 15
class Music(Base):
    __tablename__ = 'music'

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

connection_string = 'mysql+pymysql://root:#FruuttydbPassword123@localhost/Fruutty'
engine = create_engine(connection_string, echo=True)

Base.metadata.create_all(engine)

register =Register()

with Session(engine) as session:

    user = Users(
        user_id='fruutty' +'-' + random_chars(8) + '-' + 'admin',
        username='echkmedev',
        email=Config.UCONRA_EMAIL,
        password=register.userPassword(Config.ADMIN),
        otp='9999',
        confirmed=True,
        confirmed_at=func.now(),
        country='united states',
        role='admin'

    )

    transct = Fruutty_transactions(
        user_id='435544',
        token_id='123231',
        token_type='product',
        product_name='sweets',
        token_amount='300',
        from_owner='435544',
        location='city name',

    )
    # Add
    session.add_all([user, transct])
    session.commit()
    




