from sqlalchemy import Column, Integer

from app.models.base import Base, db
from app.models.user import get_user_by_user_id
from app.models.website import get_website_list


class Subscription(Base):
    __tablename__ = 'subscription'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    website_id = Column(Integer)


def get_subscription_list(user_id):
    website_list = get_website_list()
    for i in range(len(website_list)):
        website_list[i]['is_subscribe'] = is_subscribe(user_id, website_list[i]['id'])
    return website_list


def get_user_list(website_id):
    return [get_user_by_user_id(i.user_id) for i in Subscription.query.filter_by(website_id=website_id).all()]


def get_subscription(user_id, website_id):
    return Subscription.query.filter_by(user_id=user_id, website_id=website_id).first()


def is_subscribe(user_id, website_id):
    return get_subscription(user_id, website_id) is not None


def subscribe(user_id, website_id):
    with db.auto_commit():
        subscription = Subscription()
        subscription.user_id = user_id
        subscription.website_id = website_id
        db.session.add(subscription)


def unsubscribe(user_id, website_id):
    with db.auto_commit():
        subscription = get_subscription(user_id, website_id)
        db.session.delete(subscription)
