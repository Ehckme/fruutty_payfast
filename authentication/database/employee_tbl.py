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

sys.path.insert(0,'/home/ehckme/Desktop/fruutty/')

from config import Config

# create an inheritance class from declarativeBase
class Base(DeclarativeBase):
    pass


# Create an association tabele for both tables to merge
# note for a Core table, we use the sqlalchemy.column construct
# not sqlalchemy.orm.mapped_column


# 1
class Applications(Base):
    __tablename__ = 'applications'

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

class Employees(Base):

    __tablename__ = 'employees'

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



class Employee_address(Base):

    __tablename__ = 'employee_address'

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
class Employee_login(Base):
    __tablename__ = 'employee_login'

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
               f'lastLogout_at={self.lastLout_at!r},)'


class Admin_token_request(Base):
    __tablename__ = 'admin_token_request'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[str] = mapped_column(String(30), nullable=True)
    employee_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30), nullable=True)
    token_request: Mapped[str] = mapped_column(String(30))
    token_amount: Mapped[str] = mapped_column(String(30))
    reference: Mapped[str] = mapped_column(String(500))
    to: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.datetime] = mapped_column(DateTime(
        timezone=True), nullable=True, server_default=func.now() )
    def __repr__(self) -> str:
        return f'Admin_token_request=(id={self.id!r}, employee_id={self.employee_id!r},' \
               f'employee_name={self.ememployee_name!r}, email={self.email!r},' \
               f'role={self.role!r}, token_request={self.token_request!r},' \
               f'token_amoun={self.token_amount!r}, reference={self.reference!r},' \
               f'to={self.to!r}, date={self.date!r} )'


class Sales(Base):
    __tablename__ = 'Sales'
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


binds_string = 'mysql+pymysql://root:#FruuttydbPassword123@localhost/Fruutty_employees'
engine = create_engine(binds_string, echo=True)

Base.metadata.create_all(engine)

register = Register()
# password = regisster.userPassword(Config.ADMIN)
"""
with Session(engine) as session:

    employee_login = Employee_login(
        employee_id='fruutty' + '-' + random_chars(8) + '-' + 'employee',
        employee_name='Ehckmedev',
        role='admin',
        email=f'{Config.UCONRA_EMAIL}',
        password=register.userPassword(Config.ADMIN)

    )
    session.add_all([employee_login])
    session.commit()
"""



