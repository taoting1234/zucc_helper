from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Website(Base):
    __tablename__ = 'website'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)


def get_website(website_id):
    return Website.query.get(website_id)


def get_website_list():
    website = Website.query.all()
    res = list()
    for i in website:
        res.append({
            'id': i.id,
            'name': i.name
        })
    return res
