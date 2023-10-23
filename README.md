# WeMeet App

### 작업 방법
    
    git checkout <본인 개인 branch>
    git merge develop

- `본인 branch` 에 작업을 한 후 develop로 merge 한다. 그리고 develop branch 에서 잘 작동할 경우에만 main으로 merge & request를 날린다.

### 개발 환경 설졍

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


### 주요 설치 패키지


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
|          **Pillow**               |  10.0.0  |




