from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base, db


class Title(Base):
    __tablename__ = 'title'

    id = Column(Integer, primary_key=True, autoincrement=True)
    website_id = Column(Integer)
    title = Column(String)
    publish_time = Column(DateTime)


def is_exist_title(website_id, title):
    return Title.query.filter_by(website_id=website_id, title=title).first() is not None


def create_title(website_id, title, publish_time):
    with db.auto_commit():
        t = Title()
        t.website_id = website_id
        t.title = title
        t.publish_time = publish_time
        db.session.add(t)
