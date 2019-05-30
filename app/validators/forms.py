from flask_login import current_user
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.models.subscription import is_subscribe
from app.models.website import get_website
from app.validators.base import BaseForm as Form


class BindForm(Form):
    username = StringField(validators=[DataRequired(message='用户名不能为空')])
    password = StringField(validators=[DataRequired(message='密码不能为空')])


class CodeForm(Form):
    code = StringField(validators=[DataRequired(message='code不能为空')])


class SubscriptionForm(Form):
    website_id = IntegerField(validators=[DataRequired(message='网站id不能为空')])
    is_subscribe = BooleanField()

    def validate_website_id(self, value):
        if not get_website(value.data):
            raise ValidationError('网站id不存在')

    def validate_is_subscribe(self, value):
        if value.data:
            if is_subscribe(current_user.id, self.website_id.data):
                raise ValidationError('该网站已订阅')
        else:
            if not is_subscribe(current_user.id, self.website_id.data):
                raise ValidationError('该网站未订阅')


class ModifyUserForm(Form):
    xn = StringField(validators=[DataRequired(message='学年不能为空')])
    xq = StringField(validators=[DataRequired(message='学期不能为空')])
