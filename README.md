# 💻WeMeet App
약속 참여자들의 위치현황을 파악해서 성공적인 만남을 도와주는 프로젝트

## ✨배포주소
http://default-app-wemeet-d8af9-20143429-9c5e3fc9d15b.kr.lb.naverncp.com/plan

<br>

## 🎲프로젝트 소개(수정필요)
- 프로젝트명: Wemeet
  
- 개발 기간: 2023.09.25 ~ 2023.10.24
  
- 팀원: 최하나, 안주현, 강영구, 조성열
  
- 기능: 회원가입 후 약속방을 생성하면 유저를 초대할 수 있는 초대코드를 초대하고싶은 유저에게 전할하면 약속방 참여와 함께 참여자들의 위치와 도착지점과의 거리도 알 수 있습니다. 알 수 있습니다. 약속 하루전 알람 이메일발송이 자동으로 보내집니다. 


<br>

## 🔍기술스택

### ✔️Frond-end
<img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black"><img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"><img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"><img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"><img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">


### ✔️Back-end
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"><img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white"><img src="https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=Celery&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white">


### ✔️Infra 
<img src="https://img.shields.io/badge/Naver Cloud Platform-03C75A?style=for-the-badge&logo=Naver Cloud Platform&logoColor=white"><img src="https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=Terraform&logoColor=white"><img src="https://img.shields.io/badge/Kubernetes-EF7B4D?style=for-the-badge&logo=Kubernetes&logoColor=white"><img src="https://img.shields.io/badge/ArgoCD-326CE5?style=for-the-badge&logo=Argo&logoColor=white"><img src="https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=Helm&logoColor=white">

### ✔️Monitoring
<img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=Grafana&logoColor=white"><img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white">

### ✔️management
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"><img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"><img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white">

##⚙

<br>

## 🛠주요 설치 패키지


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

## 작업 방법
    
    git checkout <본인 개인 branch>
    git merge develop

- `본인 branch` 에 작업을 한 후 develop로 merge 한다. 그리고 develop branch 에서 잘 작동할 경우에만 main으로 merge & request를 날린다.

## ⚙개발 환경 설정

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
    http://default-app-wemeet-d8af9-20143429-9c5e3fc9d15b.kr.lb.naverncp.com/plan
    ```

    
- Monitoring

    Prometheus 

    Grafana
