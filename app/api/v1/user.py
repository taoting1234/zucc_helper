from flask import jsonify

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.service import bind_user, unbind_user
from app.libs.weixin import Weixin
from app.models.user import (get_user_by_openid, get_user_by_user_id,
                             modify_user)
from app.models.user_log import user_log
from app.models.zf_user import get_zf_user_by_user_id
from app.validators.forms import BindForm, CodeForm, ModifyUserForm
from flask_login import current_user, login_required, login_user, logout_user

api = Redprint('user')


# 微信登录
@api.route("/weixin_login", methods=['POST'])
def weixin_login_api():
    form = CodeForm().validate_for_api()
    openid = Weixin.get_openid(form.code.data)
    user = get_user_by_openid(openid)
    login_user(user, remember=True)
    return Success()


# 测试登录
@api.route("/test_login", methods=['GET', 'POST'])
def test_login_api():
    user = get_user_by_user_id(1)
    login_user(user)
    return Success()


@api.route("/logout", methods=['POST'])
def logout_api():
    logout_user()
    return Success()


@api.route("/bind_user", methods=['POST'])
@login_required
def bind_user_api():
    form = BindForm().validate_for_api()
    user_log(current_user.id, 'bind_user')
    bind_user(current_user.id, form.username.data, form.password.data)
    return Success()


@api.route("/unbind_user", methods=['POST'])
@login_required
def unbind_user_api():
    unbind_user(current_user.id)
    return Success()


@api.route("/get_auth_status", methods=['POST'])
@login_required
def get_auth_status_api():
    return jsonify({'code': 0 if current_user else -1})


@api.route("/get_user_info", methods=['POST'])
@login_required
def get_user_info_api():
    zf_user = get_zf_user_by_user_id(current_user.id)
    if zf_user:
        zf_username = zf_user.username
    else:
        zf_username = None
    return jsonify({
        'code': 0,
        'username': zf_username,
        'xq': current_user.xq,
        'xn': current_user.xn
    })


@api.route("/modify_user_info", methods=['POST'])
@login_required
def modify_user_info_api():
    form = ModifyUserForm().validate_for_api()
    modify_user(current_user.id, form.xn.data, form.xq.data)
    return Success()
