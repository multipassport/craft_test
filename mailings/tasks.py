from datetime import datetime
from time import sleep
from urllib.parse import urljoin

import requests
from celery import shared_task
from django.conf import settings
from requests.adapters import HTTPAdapter, Retry

from mailings.models import Customer, Mailing, Message


@shared_task
def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)

    phonenumber_rule = f'+7{mailing.operator_code}'
    customers = Customer.objects.filter(
        phone__startswith=phonenumber_rule,
        tag=mailing.tag,
    )

    message_text = mailing.message_text

    headers = {'Authorization': settings.MAILING_JWT_TOKEN}

    for customer in customers:
        message, _ = Message.objects.get_or_create(
            mailing=mailing,
            customer=customer,
        )
        cut_number = str(customer.phone).lstrip('+')
        message_params = {
          'id': message.id,
          'phone': cut_number,
          'text': message_text,
        }

        session = requests.Session()
        retries = Retry(total=20, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount(settings.MAILING_URL, HTTPAdapter(max_retries=retries))

        url = urljoin(settings.MAILING_URL, str(message.id))
        response = session.post(url, headers=headers, json=message_params)
        response.raise_for_status()

        message.sending_time = datetime.now()
        message.is_sent = True
        message.save()

        sleep(0.1)
