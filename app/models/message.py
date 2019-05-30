from sqlalchemy import BigInteger, Column, Integer, String

from app.models.base import Base, db


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_user_name = Column(String(100), nullable=False)
    to_user_name = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    msgid = Column(BigInteger, unique=True)


def message_log(from_user_name, to_user_name, content, msgid=None):
    with db.auto_commit():
        message = Message()
        message.from_user_name = from_user_name
        message.to_user_name = to_user_name
        message.content = content
        message.msgid = msgid
        db.session.add(message)
