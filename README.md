# WeMeet App

## 작업 방법
    
    git checkout <본인 개인 branch>
    git merge develop

- `본인 branch` 에 작업을 한 후 develop로 merge 한다. 그리고 develop branch 에서 잘 작동할 경우에만 main으로 merge & request를 날린다.

## 개발 환경 설졍

- Local

    ```
    python manage.py runserver localhost:8000
    ```
    에서 기능을 구현 및 테스트 진행

- Staging

    Prod 환경으로 넘어가기 전 테스트를 진행
    
    버전과 관련된 오류 체크 및 파일 경로 체크

- Prodcution

    ```
    http://default-stag-wemeet-fc448-19977705-a3810fad5f77.kr.lb.naverncp.com
    ```

    
- Monitoring

    Prometheus 

    Grafana

<br>

## 주요 설치 패키지


|                이름                 |    버전    |
|:---------------------------------:|:--------:|
|            **python**             |  3.9.13  |
|            **Django**             |  4.2.5   |
|          **PostgreSQL**           | 13-alpine|
|           **gunicorn**            |  21.2.0  |
|        **psycopg2-binary**        |  2.9.7   |
|      **djangorestframework**      |  3.14.0  |
| **djangorestframework-simplejwt** |  5.3.0   |
|      **drf-nested-routers**       |  0.93.4  |
|          **drf-yasg**             |  0.26.4  |
|      **django-bootstrap4**        |   23.2   |
|    **social-auth-app-django**     |   5.3.0  |
|       **django-allauthr**         |   23.2   |
|      **django-prometheus**        |  2.3.1   |
|          **celery**               |  5.3.4   |
|     **django-celery-results**     |  2.5.1   |
|       **django-celery-beat**      |  2.5.0   |
|         **django-redis**          |  5.4.0   |
|          **redis**                |  4.6.0   |
|          **Pillow**               |  10.1.0  |

<br>

## 주요 URL

### About User

|     기능     |          요청            |     URL     |
|-------------|--------------------------|-------------|
| **로그인**              |       POST         | /account/login |
| **로그아웃**            |       POST         | /account/logged_out   |
| **회원가입**            |       POST         | /account/register    |
| **현재 위치 업데이트**   |      POST          | /account/update_location    |
| **마이페이지**          |       GET          | /account/my_page    |
| **내 활동 요약**        |       GET          | /account/dashboard    |
| **계정 정보 수정**      |       POST         | /account/edit/user    |
| **프로필 수정**         |       POST         | /account/edit/profile    |


### About Plan

|     기능     |          요청            |     URL     |
|-------------|--------------------------|-------------|
| **약속 리스트**           |       GET         | /plan/ |
| **약속 생성**             |  POST     | /plan/create   |
| **약속 조회**             |  GET      | /plan/<pk>/    |
| **약속 수정**             |  POST     | /plan/<pk>/edit  |
| **약속 삭제**             |   POST    | /plan/<pk>/delete |
| **참여자 위치보기**        |   GET     | /plan/<pk>/map  |
| **참여자에게 메일발송**     |  POST    | /plan/<pk>/mail   |
| **약속 참여(그룹 생성)**    |  POST    | /plan/<pk>/group  |
| **약속 나가기(그룹 삭제)**  |  POST    | /plan/<pk>/group/delete  |
| **댓글 생성**              |  POST    | /plan/<pk>/comment/create  |
| **비밀방 비밀번호 체크**    |  POST    | /plan/check_password/    |

<br>

## ERD

![ERD](https://github.com/Ex-ez/Django_development/assets/68387118/3bb946b9-9b75-40f6-99e8-80c8433190cc)
