# meet_app

### 작업 방법

    git checkout <본인 개인 branch>
    git merge dev

- `본인 branch` 에 작업을 한 후 dev로 merge 한다. 그리고 dev branch 에서 잘 작동할 경우에만 main으로 merge & request를 날린다.

### docker

    # 컨테이너 실행
    docker-compose up --build -d
    # 그리고 http://localhost:8888로 접속

- docker 명령어

        # superuser 생성
        docker-compose exec web python manage.py createsuperuser 
        
        # 현재 실행되고 있는 컨테이너를 보여줌
        docker-compose ps 
    
        # 컨테이너 종료
        docker-compose down
