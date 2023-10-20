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


### 버전


| 버전 | | 
| :---:   | :--- | 
| PostgreSQL | 13-alpine  |
| Django | 4.2.5 |
| Celery | 5.3.4 | 
| Redis | 7.2.1 | 
| Kubernetes | 1.25.8 | 




