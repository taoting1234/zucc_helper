from flask import jsonify

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.subscription import (get_subscription_list, subscribe,
                                     unsubscribe)
from app.models.user_log import user_log
from app.validators.forms import SubscriptionForm
from flask_login import current_user, login_required

api = Redprint('subscription')


@api.route("/get_subscription_list", methods=['POST'])
@login_required
def get_subscription_list_api():
    return jsonify({
        'code': 0,
        'data': get_subscription_list(current_user.id)
    })


@api.route("/modify_subscription", methods=['POST'])
@login_required
def modify_subscription_api():
    form = SubscriptionForm().validate_for_api()
    if form.is_subscribe.data:
        user_log(current_user.id, 'subscription %s' % form.website_id.data)
        subscribe(current_user.id, form.website_id.data)
    else:
        user_log(current_user.id, 'unsubscription %s' % form.website_id.data)
        unsubscribe(current_user.id, form.website_id.data)
    return Success()
