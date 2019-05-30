from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from app import login_manager
from app.libs.error_code import AuthFailed
from app.models.base import Base, db


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(100), unique=True)


def create_user(openid):
    with db.auto_commit():
        user = User()
        user.openid = openid
        db.session.add(user)
    return user


def get_user_by_openid(openid):
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        user = create_user(openid)
    return user


@login_manager.user_loader
def get_user_by_user_id(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthFailed()
