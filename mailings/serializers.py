from datetime import datetime

import pytz
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from craft.celery import celery_app
from mailings.models import Customer, Mailing
from mailings.tasks import send_mailing


class CustomerSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'tags': {'required': False},
        }


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        exclude = ['task_id']
        extra_kwargs = {
            'tags': {'required': False},
        }

    def validate(self, attrs):
        if attrs['start_time'] > attrs['end_time']:
            error = {
                'start_time': 'start_time should be sooner than end_time',
                'end_time': 'start_time should be sooner than end_time',
            }
            raise serializers.ValidationError(error)
        return attrs

    def create(self, validated_data):
        mailing = super().create(validated_data)
        self._send_task_in_queue(mailing)
        return mailing

    def update(self, instance, validated_data):
        mailing = super().update(instance, validated_data)
        celery_app.control.revoke(mailing.task_id)
        self._send_task_in_queue(mailing)
        return mailing

    def _send_task_in_queue(self, mailing):
        now = datetime.now(tz=pytz.UTC)
        start_time = mailing.start_time
        end_time = mailing.end_time

        if start_time <= now <= end_time:
            mailing.task_id = send_mailing.apply_async(
                (mailing.id,),
                expires=end_time,
            )
            mailing.save()
        if start_time >= now and end_time >= now:
            mailing.task_id = send_mailing.apply_async(
                (mailing.id,),
                eta=start_time,
                expires=end_time,
            )
            mailing.save()


class MailingStatsSerializer(serializers.ModelSerializer):
    sent_messages_count = serializers.SerializerMethodField()
    unsent_messages_count = serializers.SerializerMethodField()

    def get_sent_messages_count(self, mailing):
        return mailing.messages.filter(is_sent=True).count()

    def get_unsent_messages_count(self, mailing):
        return mailing.messages.filter(is_sent=False).count()

    class Meta:
        model = Mailing
        fields = [
            'tag',
            'operator_code',
            'sent_messages_count',
            'unsent_messages_count',
        ]


class TotalStatsSerializer(serializers.Serializer):
    sent_messages_count = serializers.IntegerField()
    unsent_messages_count = serializers.IntegerField()

    mailings = MailingStatsSerializer(many=True)
