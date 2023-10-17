from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Group


@shared_task
def send_reminder_email(plan_id):
    tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
    groups = Group.objects.filter(plan__time__date=tomorrow, plan__id=plan_id)

    for group in groups:
        local_time = group.plan.time.astimezone(timezone.get_default_timezone())
        formatted_time = local_time.strftime("%H:%M")

        subject = f"{group.plan.title} 모임 알림"
        message_html_template = (
            f"<h1>안녕하세요 {group.user}님!</h1>"
            "<br>"
            f"<p>{group.plan.title} 모임 알림 입니다.</p>"
            "<br>"
            f"내일 <strong>{formatted_time}</strong>까지 모임에 참석해주시기 바랍니다.</p>"
            f"<p>장소는 <strong>{group.plan.address}</strong> 입니다.</p>"
            "<br>"
            f'<a href="https://www.google.com/maps/search/?api=1&query={group.plan.latitude},{group.plan.longitude}" target="_blank">장소 확인하기</a>'
        )
        send_mail(
            subject,  # 이메일의 제목
            "",  # 이메일의 본문
            settings.EMAIL_HOST_USER,
            [group.user.email],
            fail_silently=False,
            html_message=message_html_template,
        )
