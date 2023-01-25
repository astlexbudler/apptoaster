# apptoaster

1. 무료 요금제
제작 50,000원
푸시 알림 없음(GCM, APNS 없음)
푸시 추가 시 새로 제작해야함.

2. 유료 요금제(월 3,900원 1년 45,000원)
1년 계약 시 제작비 10,000원



todo
1. push 메세지 관리
2. 이메일 연동
3. 아이폰 연동
4. 카카오 비즈 연결
5. 통계 확인 기능 업데이트
6. 이메일 메세지 연결
7. SMS 메세지 연결
8. 카카오 메세지 연결

venv requirements
pip install Django
pip install requests
pip install django-apscheduler

        /*
        앱에서 실행되는 코드
        TARGET
        (PUT) /api/target/key/00000000?deviceType=gcm&token=TEST_TOKEN&isPushAllow=true
        (GET) /api/target/key/00000000?deviceType=gcm&token=TEST_TOKEN
        (PATCH) /api/target/key/00000000?id=20230125051653577140&isPushAllow=true&isAdAllow=true&isNightAllow=false

        PUSH
        (POST) /api/toast_push/key/00000000
        alias = test_push1
        title = push_title
        message = push_message
        date = 2023-01-25
        time = 12:00:00
        repeat = 1
        ad = 1
        (POST) /api/update_push/key/00000000
        id = 20230125060029107002
        alias = updated_alias
        title = updated_title
        message = updated_message
        date = null
        time = 11:00:00
        repeat = 2
        ad = 0
        (GET) /api/push/key/00000000
        (DELETE) /api/push/key/00000000?id=20230125060029107002
        (GET) /api/push/toasted/key/00000000
        */