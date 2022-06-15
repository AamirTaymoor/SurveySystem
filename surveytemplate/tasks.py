from celery.decorators import task
from celery.utils.log import get_task_logger
from .models import SurveyTemplates
from django.core.mail import send_mail
import os
from django.conf import settings


from time import sleep
logger = get_task_logger(__name__)


@task(name='EmailTask')
#@shared_task
def EmailTask(final_recipients,template):
    #final_recipients,template = data
    temp = SurveyTemplates.objects.get(template_name = template)
    subject = temp.subject
    body = temp.body
    email_from = settings.EMAIL_HOST_USER

    for key,value in final_recipients.items():
        message = body.replace("{name}",key)
        to = [value]
        d = send_mail(subject,message,email_from, to )
        
    

    return('Junaid')


