from celery import shared_task

from .utils import transfer_model


@shared_task
def transfer_model_backend(*args):
    transfer_model(*args)
