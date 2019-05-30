# ZUCC小助手

本程序分为2大部分，一部分是用flask写的web后端，另一部分是celery写的异步任务和定时任务

# flask启动方式
```bash
# 一般启动（仅用于测试环境）
python app.py
```

# celery
```bash
# 启动celery
celery -A tasks worker
# 启动定时器（发送定时任务）
celery -A tasks beat
# 删除所有任务
celery -A tasks purge
```