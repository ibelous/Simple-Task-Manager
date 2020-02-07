import datetime

from celery.schedules import crontab
from celery.utils.log import get_task_logger
from celery.task import periodic_task

from django.core.mail import send_mass_mail

from projects.models import Task
from src import settings

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/1440')),
    name="task_send_email",
    ignore_result=True
)
def task_send_email():
    """
    Sends email notifications about tasks deadlines every day
    """
    messages_list = []
    for task in Task.objects.all():
        if task.developer and task.status != 'Done' :
            messages_list.append(('Task deadline is coming!',
                                  '{} days left until {} deadline!'
                                  .format(task.due_date-datetime.datetime.today(), Task.title),
                                  settings.EMAIL_HOST_USER,
                                  Task.developer.email))
    send_mass_mail(tuple(messages_list))
    logger.info("Sent email to ")
