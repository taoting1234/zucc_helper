from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base, db


class UserLog(Base):
    __tablename__ = 'user-log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    log = Column(String(1000), nullable=False)


def user_log(user_id, log):
    with db.auto_commit():
        userlog = UserLog()
        userlog.user_id = user_id
        userlog.log = log
        db.session.add(userlog)
