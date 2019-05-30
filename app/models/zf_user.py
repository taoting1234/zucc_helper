from sqlalchemy import Column, ForeignKey, Integer, String

from app import create_app
from app.models.base import Base, db


class ZfUser(Base):
    __tablename__ = 'zf-user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)


def get_zf_user(zf_user_id):
    return ZfUser.query.get(zf_user_id)


def bind_zf_user(user_id, username, password):
    with db.auto_commit():
        zf_user = ZfUser()
        zf_user.username = username
        zf_user.password = password
        zf_user.user_id = user_id
        db.session.add(zf_user)


def get_zf_user_by_user_id(user_id):
    return ZfUser.query.filter_by(user_id=user_id).first()


def delete_zf_user(username):
    zf_user = ZfUser.query.filter_by(username=username).first()
    if zf_user:
        with db.auto_commit():
            db.session.delete(zf_user)
        return zf_user.user_id
