from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, views

from craft import celery_app
from mailings import serializers
from mailings.models import Customer, Mailing
from mailings.services import get_total_stats


class CustomerCreateView(generics.CreateAPIView):
    """
    Create a customer instance.
    `timezone` field accepts string value of timezone like 'Europe/Moscow'
    """
    serializer_class = serializers.CustomerSerializer
    queryset = Customer.objects.all()


class CustomerUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    put:
        Update a customer instance.
        `timezone` field accepts string value of timezone like 'Europe/Moscow'
    delete:
        Delete customer instance.
    """
    serializer_class = serializers.CustomerSerializer
    queryset = Customer.objects.all()
    http_method_names = ['delete', 'put']


class MailingCreateView(generics.CreateAPIView):
    """
    Create a mailing instance. Celery task is assigned to send messages to all
    customers, whos tags and operator_code are the same as this mailing instance.
    `end_time` should be later than `start_time`.
    """
    serializer_class = serializers.MailingSerializer
    queryset = Mailing.objects.all()


class MailingUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    put:
        Update a mailing instance. Celery task is reassigned to send messages to all
        customers, whos tags and operator_code are the same as this mailing instance.
        `end_time` should be later than `start_time`
    delete:
        Delete a mailing instance. Also revokes corresponding celery task.
    """
    serializer_class = serializers.MailingSerializer
    queryset = Mailing.objects.all()
    http_method_names = ['delete', 'put']

    def perform_destroy(self, mailing):
        celery_app.control.revoke(mailing.task_id)
        super().perform_destroy(mailing)


class MailingStatsView(generics.RetrieveAPIView):
    """
    Returns simple statistics for chosen mailing.
    """
    serializer_class = serializers.MailingStatsSerializer
    queryset = Mailing.objects.prefetch_related('messages')


class TotalStatsView(views.APIView):
    """
    Returns total statistics for all mailings.
    """
    serializer_class = serializers.TotalStatsSerializer

    @swagger_auto_schema(responses={200: serializers.TotalStatsSerializer()})
    def get(self, request):
        return get_total_stats()
