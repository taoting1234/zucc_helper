from flask import request

from app.libs.redprint import Redprint
from app.libs.weixin import Weixin
from app.libs.xmlparser import XmlParser
from app.models.message import message_log
from app.models.user import get_user_by_openid
from tasks import (task_get_examination_room, task_get_grade,
                   task_get_makeup_examination_room)

api = Redprint('weixin')


@api.route('', methods=['GET', 'POST'])
def weixin_api():
    if request.method == 'GET':  # 微信开放平台校验
        if Weixin.check_signature(request.args):
            return request.args['echostr']
        return 'auth failed'
    if request.method == 'POST':  # 用户消息
        rcv_dict = XmlParser.loads(request.get_data())['xml']
        user = get_user_by_openid(rcv_dict['FromUserName'])
        if rcv_dict.get('MsgType') == 'text':
            Weixin.create_typing(rcv_dict['FromUserName'])
            message_log(rcv_dict['FromUserName'], rcv_dict['ToUserName'], rcv_dict['Content'], rcv_dict['MsgId'])
            msg = rcv_dict['Content']
            if '成绩' in msg:
                task_get_grade.delay(user.id)
        if rcv_dict.get('MsgType') == 'event':
            if rcv_dict.get('Event') == 'CLICK':
                Weixin.create_typing(rcv_dict['FromUserName'])
                if rcv_dict.get('EventKey') == 'grade':
                    task_get_grade.delay(user.id)
                if rcv_dict.get('EventKey') == 'examination_room':
                    task_get_examination_room.delay(user.id)
                if rcv_dict.get('EventKey') == 'makeup_examination_room':
                    task_get_makeup_examination_room.delay(user.id)

        return 'success'
