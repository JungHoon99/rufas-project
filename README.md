# RUFAS

## 프로젝트 설명
쇼핑몰 웹사이트에서 간단한 코드 적용을 통해서 웹 사용자들의 사이트 이용 로그를 수집하여 이용형태를 확인 할 수 있는 프로그램

----

## Django 사용 방법

1. ### 사용 라이브러리 리스트
        Django==3.2.5
        elasticsearch==8.8.2
        PyMySQL==1.0.2

1. ### 서버 실행
    1. `web_site` 폴더 접근
    1. `python manage.py runserver` 실행


---
### 현재 프로젝트 파일 구조
```
RUFAS-PROJECT
│  .gitignore
│  README.md
│  
├─docker-elk
│  │  docker-compose.yml
│  │  LICENSE
│  │  README.md
│  │
│  ├─elasticsearch
│  │  │  Dockerfile
│  │  │
│  │  └─config
│  │          elasticsearch.yml
│  │
│  ├─extensions
│  │  │  README.md
│  │  │
│  │  ├─curator
│  │  │  │  curator-compose.yml
│  │  │  │  Dockerfile
│  │  │  │  README.md
│  │  │  │
│  │  │  └─config
│  │  │          curator.yml
│  │  │          delete_log_files_curator.yml
│  │  │
│  │  ├─enterprise-search
│  │  │  │  Dockerfile
│  │  │  │  enterprise-search-compose.yml
│  │  │  │  README.md
│  │  │  │
│  │  │  └─config
│  │  │          enterprise-search.yml
│  │  │
│  │  ├─filebeat
│  │  │  │  Dockerfile
│  │  │  │  filebeat-compose.yml
│  │  │  │  README.md
│  │  │  │
│  │  │  └─config
│  │  │          filebeat.yml
│  │  │
│  │  ├─fleet
│  │  │      agent-apmserver-compose.yml
│  │  │      Dockerfile
│  │  │      fleet-compose.yml
│  │  │      README.md
│  │  │
│  │  ├─heartbeat
│  │  │  │  Dockerfile
│  │  │  │  heartbeat-compose.yml
│  │  │  │  README.md
│  │  │  │
│  │  │  └─config
│  │  │          heartbeat.yml
│  │  │
│  │  ├─logspout
│  │  │      build.sh
│  │  │      Dockerfile
│  │  │      logspout-compose.yml
│  │  │      modules.go
│  │  │      README.md
│  │  │
│  │  └─metricbeat
│  │      │  Dockerfile
│  │      │  metricbeat-compose.yml
│  │      │  README.md
│  │      │
│  │      └─config
│  │              metricbeat.yml
│  │
│  ├─kibana
│  │  │  Dockerfile
│  │  │
│  │  └─config
│  │          kibana.yml
│  │
│  ├─logstash
│  │  │  Dockerfile
│  │  │
│  │  ├─config
│  │  │      logstash.yml
│  │  │
│  │  └─pipeline
│  │          logstash.conf
│  │
│  └─setup
│      │  Dockerfile
│      │  entrypoint.sh
│      │  lib.sh
│      │
│      └─roles
│              filebeat_writer.json
│              heartbeat_writer.json
│              logstash_writer.json
│              metricbeat_writer.json
│
├─docker-kafka
│      docker-compose.yml
│
└─web_site
    │  db.sqlite3
    │  env_setting.py
    │  manage.py
    │
    ├─rufas
    │  │  admin.py
    │  │  apps.py
    │  │  models.py
    │  │  tests.py
    │  │  views.py
    │  │  __init__.py
    │  │
    │  └─migrations
    │          __init__.py
    │
    ├─templates
    │      main-login.html
    │
    └─web_site
        │  asgi.py
        │  settings.py
        │  urls.py
        │  wsgi.py
        │  __init__.py
        │
        └─__pycache__
                settings.cpython-39.pyc
                urls.cpython-39.pyc
                wsgi.cpython-39.pyc
                __init__.cpython-39.pyc
```