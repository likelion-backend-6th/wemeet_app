# meet_app

### 작업 방법

    git checkout <본인 개인 branch>
    git merge dev

- `본인 branch` 에 작업을 한 후 dev로 merge 한다. 그리고 dev branch 에서 잘 작동할 경우에만 main으로 merge & request를 날린다.

### 개발 환경
    
| 환경 | 방법   | 
| :---:   | :---: | 
| Local | DB: sqlite3를 이용  |
| Staging | terraform (backend, DB 서버 생성)   |
| Production | K8S 사용   | 

- Local

    기본적인 app 기능 구현 확인 후 push

- Staging

    Prod 환경으로 넘어가기 전 테스트 (Kakao map 관련된 테스트도 진행)

    - 서버로 접속: <terrraform Backend 주소>

- Prodcution

    Helm Chart 구성 후 ArgoCD 에 깃 레포 연결. 

    Prometheus를 이용해 정보를 수집한 후 Grafana 대쉬보드에서 모니터링





