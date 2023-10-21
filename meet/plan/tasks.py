from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Group


@shared_task
def send_reminder_email(plan_id):
    groups = Group.objects.filter(plan__id=plan_id)

    for group in groups:
        local_time = group.plan.time.astimezone(timezone.get_default_timezone())
        formatted_time = local_time.strftime("%H:%M")
        date = group.plan.time.strftime("%m월 %d일")
        users = [group.user.username for group in groups]
        formatted_users = ", ".join(users)

        subject = f"{group.plan.title} 모임 알림"
        if group.plan.owner != group.user:
            message_html_template = (
                f"<h1>안녕하세요 {group.user}님!</h1>"
                "<br>"
                f"<p>{group.plan.title} 모임 알림 입니다.</p>"
                "<br>"
                f"{date} <strong>{formatted_time}</strong> 까지 모임에 참석해주시기 바랍니다.</p>"
                f"<p>장소는 <strong>{group.plan.address}</strong> 입니다.</p>"
                "<br>"
                f"참여자는 <strong>{formatted_users}</strong> 님이 참여합니다."
                "<br>"
                f"이 메일은 {group.plan.owner} 님이 직접 발송하였습니다."
                "<br>"
                "<br>"
                f'<a href="https://map.kakao.com/link/map/약속장소,{group.plan.latitude},{group.plan.longitude}">장소 확인하기</a>'
            )
            send_mail(
                subject,  # 이메일의 제목
                "",  # 이메일의 본문
                settings.EMAIL_HOST_USER,
                [group.user.email],
                fail_silently=False,
                html_message=message_html_template,
            )


@shared_task
def send_reminder_email_auto(plan_id):  # auto
    tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
    groups = Group.objects.filter(plan__time__date=tomorrow, plan__id=plan_id)
    users = [group.user.username for group in groups]
    formatted_users = ", ".join(users)

    for group in groups:
        local_time = group.plan.time.astimezone(timezone.get_default_timezone())
        formatted_time = local_time.strftime("%H:%M")

        subject = f"{group.plan.title} 모임 알림"
        message_html_template = (
            f"<h1>안녕하세요 {group.user}님!</h1>"
            "<br>"
            f"<p>{group.plan.title} 모임 알림 입니다.</p>"
            "<br>"
            f"내일까지 <strong>{formatted_time}</strong>까지 모임에 참석해주시기 바랍니다.</p>"
            f"<p>장소는 <strong>{group.plan.address}</strong> 입니다.</p>"
            "<br>"
            f"참여자는 <strong>{formatted_users}</strong> 입니다."
            "<br>"
            f"이 메세지는 미팅 하루 전 자동 발송되었습니다."
            "<br>"
            "<br>"
            f'<a href="https://map.kakao.com/link/map/약속장소,{group.plan.latitude},{group.plan.longitude}">장소 확인하기</a>'
        )
        send_mail(
            subject,  # 이메일의 제목
            "",  # 이메일의 본문
            settings.EMAIL_HOST_USER,
            [group.user.email],
            fail_silently=False,
            html_message=message_html_template,
        )
