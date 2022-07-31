from rest_framework.response import Response

from mailings.models import Mailing, Message
from mailings.serializers import MailingStatsSerializer


def get_total_stats():
    total_sent_messages = Message.objects.filter(is_sent=True).count()
    total_unsent_messages = Message.objects.filter(is_sent=False).count()

    mailings = Mailing.objects.prefetch_related('messages')
    mailing_stats = serialize_mailings_stats(mailings)

    return Response({
        'total_sent_messages': total_sent_messages,
        'total_unsent_messages': total_unsent_messages,
        'mailing_stats': mailing_stats,
    })


def serialize_mailings_stats(mailings):
    for mailing in mailings:
        mailing_stats = MailingStatsSerializer(mailing)
        yield mailing_stats.data
