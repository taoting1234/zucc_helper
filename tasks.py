import os
import platform

import requests
from celery import Celery

from app import create_app
from app.libs.logger import logger
from app.libs.service import (get_examination_room, get_grade,
                              get_makeup_examination_room, push_all_title)

if platform.system() == 'Windows':
    # 解决windows运行worker错误

    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

celery = Celery('tasks')
celery.config_from_object('app.config.setting')
celery.config_from_object('app.config.secure')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, heartbeat, name='heartbeat')
    sender.add_periodic_task(600, task_push_all_title, name='task_push_all_title')


@celery.task
def heartbeat():
    try:
        requests.get('http://xk.zucc.edu.cn')
        logger.debug('heartbeat success')
    except Exception as e:
        logger.debug('heartbeat failed %s', e)


@celery.task
def task_get_grade(user_id):
    app = create_app()
    with app.app_context():
        get_grade(user_id)


@celery.task
def task_get_examination_room(user_id):
    app = create_app()
    with app.app_context():
        get_examination_room(user_id)


@celery.task
def task_get_makeup_examination_room(user_id):
    app = create_app()
    with app.app_context():
        get_makeup_examination_room(user_id)


@celery.task
def task_push_all_title():
    app = create_app()
    with app.app_context():
        push_all_title()


if __name__ == '__main__':
    task_push_all_title()
