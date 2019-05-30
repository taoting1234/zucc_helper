import hashlib
import json
import time

import requests

from app.config.secure import *
from app.libs.error_code import AuthFailed
from app.libs.logger import logger
from app.models.config import get_value, set_value
from app.models.message import message_log


class Weixin:
    @staticmethod
    def check_signature(data):
        try:
            params = [data['nonce'], data['timestamp'], token]
            params.sort()
            tmp = params[0] + params[1] + params[2]
            tmp = hashlib.sha1(tmp.encode()).hexdigest()
            if tmp == data['signature']:
                return True
            return False
        except:
            return False

    @classmethod
    def get_token(cls):
        token_ = get_value('token')
        try:
            token_ = json.loads(token_)
        except:
            token_ = None

        if token_ is None or time.time() - token_['time'] > 0.9 * token_['expires_in']:
            token_ = cls.__get_token()
        return token_['access_token']

    @classmethod
    def __get_token(cls):
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': AppID,
            'secret': AppSecret
        }
        res = requests.get(url=url, params=params)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            logger.debug(('get token failed:', res_json.get('errmsg')))
            time.sleep(1)
            return cls.__get_token()
        token_dict = {
            'access_token': res_json['access_token'],
            'expires_in': res_json['expires_in'],
            'time': time.time()
        }
        token_json = json.dumps(token_dict)
        set_value('token', token_json)
        logger.debug(('get token success:', token_dict))
        return token_dict

    @classmethod
    def init_menu(cls):
        cls.delete_menu()
        cls.create_menu()

    @staticmethod
    def create_menu():
        with open('menu.json', 'r', encoding='utf8') as f:
            r = json.load(f)
        rr = json.dumps(r, ensure_ascii=False).encode('utf-8')
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}".format(Weixin.get_token())
        res = requests.post(url=url, data=rr)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            raise Exception('create menu failed:', res_json.get('errcode'), res_json.get('errmsg'))
        logger.debug(('create menu success:', res_json))

    @staticmethod
    def delete_menu():
        url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={}".format(Weixin.get_token())
        res = requests.get(url=url)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            raise Exception('delete menu failed:', res_json.get('errcode'), res_json.get('errmsg'))
        logger.debug(('delete menu success:', res_json))

    @staticmethod
    def send_text(openid, text, self_openid='localhost'):
        message_log(self_openid, openid, text)
        r = {
            "touser": openid,
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        rr = json.dumps(r, ensure_ascii=False).encode('utf-8')
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(Weixin.get_token())
        res = requests.post(url=url, data=rr)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            logger.debug(('send text message failed:', res_json.get('errcode'), res_json.get('errmsg')))
        logger.debug(('send text message success:', res_json))

    @staticmethod
    def send_template_text(openid, template_id, data, jump_url):
        r = {
            "touser": openid,
            "template_id": template_id,
            "url": jump_url,
            "data": data
        }
        rr = json.dumps(r, ensure_ascii=False).encode('utf-8')
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(Weixin.get_token())
        res = requests.post(url=url, data=rr)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            logger.debug('send template text message failed: %s %s', res_json.get('errcode'), res_json.get('errmsg'))
        logger.debug('send template text message success: %s', res_json)

    @staticmethod
    def create_typing(openid):
        r = {
            "touser": openid,
            "command": "Typing"
        }
        rr = json.dumps(r, ensure_ascii=False).encode('utf-8')
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/typing?access_token={}".format(Weixin.get_token())
        res = requests.post(url=url, data=rr)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            logger.debug(('create typing failed:', res_json.get('errcode'), res_json.get('errmsg')))
        logger.debug(('create typing success:', res_json))

    @staticmethod
    def get_openid(code):
        url = "https://api.weixin.qq.com/sns/oauth2/access_token" \
              "?appid={}&secret={}&code={}&grant_type=authorization_code".format(AppID, AppSecret, code)
        res = requests.get(url=url)
        res_json = json.loads(res.text)
        if res_json.get('errcode', 0) != 0:
            logger.debug(('get openid failed:', res_json.get('errcode'), res_json.get('errmsg')))
            raise AuthFailed()
        logger.debug(('get openid success:', res_json))
        return res_json.get('openid')
