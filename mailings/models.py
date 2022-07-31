from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField


class Mailing(models.Model):
    start_time = models.DateTimeField(
        'время запуска рассылки',
    )
    end_time = models.DateTimeField(
        'время окончания рассылки',
    )
    message_text = models.TextField(
        'текст сообщения',
    )
    tag = models.CharField(
        'тэг',
        max_length=20,
    )
    operator_code = models.IntegerField(
        'код оператора',
        validators=[
            MinValueValidator(900),
            MaxValueValidator(999),
        ],
    )
    task_id = models.CharField(
        'id задачи celery',
        max_length=36,
        blank=True,
    )

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return f'Рассылка {self.id}'


class Customer(models.Model):
    phone = PhoneNumberField(
        'телефонный номер',
        unique=True,
    )
    tag = models.CharField(
        'тэг',
        max_length=20,
    )
    timezone = TimeZoneField(
        'часовой пояс',
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return str(self.phone)


class Message(models.Model):
    sending_time = models.DateTimeField(
        'время отправки',
        null=True,
    )
    is_sent = models.BooleanField(
        'отправлено',
        default=False,
    )
    mailing = models.ForeignKey(
        'Mailing',
        verbose_name='рассылка',
        related_name='messages',
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        'Customer',
        verbose_name='клиент',
        related_name='messages',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return f'Сообщение {self.id}'
