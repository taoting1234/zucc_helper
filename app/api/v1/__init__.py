from flask import Blueprint

from app.api.v1 import subscription, system, user, weixin


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    weixin.api.register(bp_v1)
    system.api.register(bp_v1)
    subscription.api.register(bp_v1)
    return bp_v1
