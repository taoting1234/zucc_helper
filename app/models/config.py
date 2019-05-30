from sqlalchemy import Column, String

from app.models.base import Base, db


class Config(Base):
    __tablename__ = 'config'

    key = Column(String(100), primary_key=True)
    value = Column(String(10000), nullable=False)


def get_value(key):
    r = Config.query.get(key)
    if r:
        return r.value
    return None


def set_value(key, value):
    config = Config.query.get(key)
    if not config:
        with db.auto_commit():
            config = Config()
            config.key = key
            config.value = value
            db.session.add(config)

    else:
        with db.auto_commit():
            config.value = value
