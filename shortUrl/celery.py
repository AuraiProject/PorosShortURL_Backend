import os
from datetime import datetime

from celery import Celery
from celery.schedules import crontab
from django.db.models import Q

from main.utils import transfer_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortUrl.settings')

app = Celery('shortUrl')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    设置 celery 周期任务
    """
    sender.add_periodic_task(
        crontab(minute=0, hour=0),
        clear_expired_link.s()
    )


@app.task
def clear_expired_link():
    """
    迁移过期 url 到另一个模型
    """
    from main.models import Url, ExpiredUrl

    expireds = Url._base_manager.filter(Q(
        expired_timestamp__lt=datetime.timestamp(datetime.now())
    )).all()
    for obj in expireds:
        transfer_model(obj, ExpiredUrl)
