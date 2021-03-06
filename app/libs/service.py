from urllib.error import HTTPError

from app.config.secure import *
from app.config.setting import *
from app.libs.error_code import APIException
from app.libs.weixin import Weixin
from app.models.config import get_value
from app.models.subscription import get_user_list
from app.models.title import create_title, is_exist_title
from app.models.user import get_user_by_user_id
from app.models.website import get_website, get_website_list
from app.models.zf_user import (bind_zf_user, delete_zf_user,
                                get_zf_user_by_user_id)
from spider.apps.zf.zf_spider import ZfSpider
from spider.apps.zucc_jsxy.zucc_jsxy_constant import ZuccJsxyConstant
from spider.apps.zucc_jsxy.zucc_jsxy_spider import ZuccJsxySpider
from spider.apps.zucc_jwb.zucc_jwb_constant import ZuccJwbConstant
from spider.apps.zucc_jwb.zucc_jwb_spider import ZuccJwbSpider


def bind_user(user_id, username, password):
    zf = ZfSpider(username, password)
    try:
        zf.login()
    except HTTPError as e:
        raise APIException('连接教务系统失败：' + str(e), 200, -1)
    except Exception as e:
        raise APIException('绑定用户失败：' + str(e), 200, -1)
    unbind_user_id = delete_zf_user(username)
    if unbind_user_id:
        data = {
            "username": {
                "value": username,
                "color": "#FF0000"
            }
        }
        url = "http://wx-web.newitd.com/auth.html?module=bind_user"
        Weixin.send_template_text(get_user_by_user_id(unbind_user_id).openid, PASSIVE_UNBIND_TEMPLATE_ID, data, url)

    bind_zf_user(user_id, username, password)


def unbind_user(user_id):
    zf_user = get_zf_user_by_user_id(user_id)
    if not zf_user:
        raise APIException('用户未绑定', 200, -1)
    data = {
        "username": {
            "value": zf_user.username,
            "color": "#FF0000"
        }
    }
    url = "http://wx-web.newitd.com/auth.html?module=bind_user"
    Weixin.send_template_text(get_user_by_user_id(user_id).openid, INITIATIVE_UNBIND_TEMPLATE_ID, data, url)

    delete_zf_user(zf_user.username)


def get_grade(user_id):
    user = get_user_by_user_id(user_id)
    zf_user = get_zf_user_by_user_id(user_id)
    if zf_user is None:
        Weixin.send_text(user.openid, '你还没有绑定账号，请先绑定账号')
        return
    xn = user.xn if user.xn else get_value('default_xn')
    xq = user.xq if user.xq else get_value('default_xq')
    zf = ZfSpider(zf_user.username, zf_user.password, xn, xq)
    try:
        zf.login()
        r = zf.get_grade()
    except HTTPError as e:
        Weixin.send_text(user.openid, '连接教务系统失败' + str(e))
        return
    except AssertionError:
        Weixin.send_text(user.openid, '切换学年学期失败，可能该学期不存在或者没有该学期信息')
        return
    except Exception as e:
        Weixin.send_text(user.openid, '获取信息失败：' + str(e))
        return

    s = GRADE_TEXT_TITLE.format(**{
        'id': zf.id,
        'xn': zf.xn,
        'xq': zf.xq
    })
    for i in r:
        s += GRADE_TEXT_ITEM.format(**{
            'class_name': i['课程名称'],
            'credit': i['学分'],
            'grade_point': i['绩点'],
            'grade': i['成绩']
        })
    Weixin.send_text(user.openid, s)


def get_examination_room(user_id):
    user = get_user_by_user_id(user_id)
    zf_user = get_zf_user_by_user_id(user_id)
    if zf_user is None:
        Weixin.send_text(user.openid, '你还没有绑定账号，请先绑定账号')
        return
    xn = user.xn if user.xn else get_value('default_xn')
    xq = user.xq if user.xq else get_value('default_xq')
    zf = ZfSpider(zf_user.username, zf_user.password, xn, xq)
    try:
        zf.login()
        r = zf.get_examination_room()
    except HTTPError as e:
        Weixin.send_text(user.openid, '连接教务系统失败' + str(e))
        return
    except AssertionError:
        Weixin.send_text(user.openid, '切换学年学期失败，可能该学期不存在或者没有该学期信息')
        return
    except Exception as e:
        Weixin.send_text(user.openid, '获取信息失败：' + str(e))
        return

    s = EXAMINATION_ROOM_TEXT_TITLE.format(**{
        'id': zf.id,
        'xn': zf.xn,
        'xq': zf.xq
    })
    for i in r:
        s += EXAMINATION_ROOM_TEXT_ITEM.format(**{
            'class_name': i['课程名称'],
            'time': i['时间'],
            'classroom': i['教室'],
            'number': i['座位号']
        })
    Weixin.send_text(user.openid, s)


def get_makeup_examination_room(user_id):
    user = get_user_by_user_id(user_id)
    zf_user = get_zf_user_by_user_id(user_id)
    if zf_user is None:
        Weixin.send_text(user.openid, '你还没有绑定账号，请先绑定账号')
        return
    xn = user.xn if user.xn else get_value('default_xn')
    xq = user.xq if user.xq else get_value('default_xq')
    zf = ZfSpider(zf_user.username, zf_user.password, xn, xq)
    try:
        zf.login()
        r = zf.get_makeup_examination_room()
    except HTTPError as e:
        Weixin.send_text(user.openid, '连接教务系统失败' + str(e))
        return
    except AssertionError:
        Weixin.send_text(user.openid, '切换学年学期失败，可能该学期不存在或者没有该学期信息')
        return
    except Exception as e:
        Weixin.send_text(user.openid, '获取信息失败：' + str(e))
        return

    s = MAKEUP_EXAMINATION_ROOM_TEXT_TITLE.format(**{
        'id': zf.id,
        'xn': zf.xn,
        'xq': zf.xq
    })
    for i in r:
        s += MAKEUP_EXAMINATION_ROOM_TEXT_ITEM.format(**{
            'class_name': i['课程名称'],
            'time': i['时间'],
            'classroom': i['教室'],
            'number': i['座位号']
        })
    Weixin.send_text(user.openid, s)


def get_title_list(website_id):
    if website_id == 1:
        return ZuccJwbSpider().get_article_list(ZuccJwbConstant.RCTZ)
    elif website_id == 2:
        return ZuccJwbSpider().get_article_list(ZuccJwbConstant.JXDT)
    elif website_id == 3:
        return ZuccJsxySpider().get_article_list(ZuccJsxyConstant.XSGZ_RCTZ)
    elif website_id == 4:
        return ZuccJsxySpider().get_article_list(ZuccJsxyConstant.XSGZ_XWDT)
    elif website_id == 5:
        return ZuccJsxySpider().get_article_list(ZuccJsxyConstant.XSGZ_PJPY)
    elif website_id == 6:
        return ZuccJsxySpider().get_article_list(ZuccJsxyConstant.XSGZ_DEKT)
    elif website_id == 7:
        return ZuccJsxySpider().get_article_list(ZuccJsxyConstant.JXJW_JXTZ)


def push_all_title():
    website_list = get_website_list()
    for i in website_list:
        push_title(i['id'])


def push_title(website_id):
    title_list = get_title_list(website_id)
    push_list = []
    for i in title_list:
        if not is_exist_title(website_id, i['title']):
            push_list.append(i)
            create_title(website_id, i['title'], i['time'])

    user_list = get_user_list(website_id)

    if push_list:
        data = {
            "item": {
                "value": get_website(website_id).name,
                "color": "#FF0000"
            },
            "title": {
                "value": push_list[0]['title'],
                "color": "#FF0000"
            },
            "time": {
                "value": push_list[0]['time'],
                "color": "#FF0000"
            }
        }
        url = push_list[0]['url']
        for i in user_list:
            Weixin.send_template_text(i.openid, PUSH_TEMPLATE_ID, data, url)
