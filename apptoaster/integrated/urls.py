from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    ##################################################
    # 웹 페이지 경로
    ##################################################
    # 메인 페이지
    path('', views.webIndex, name='webIndex'),

    # 계정 관리 페이지
    path('toaster', views.webToaster, name='webToaster'),

    # PUSH 발송 관리 페이지
    path('push_toasting', views.webPushToasting, name='webPushToasting'),

    # PUSH 발송 기록 페이지
    path('push_toasted', views.webPushToasted, name='webPushToasted'),

    # 관리자 페이지
    path('overseer', views.webOverseer, name='webOverseer'),

    # 이용약관
    path('policy', views.webPolicy, name='webPolicy'),

    # 개인정보 처리 방침
    path('privacy', views.webPrivacy, name='webPrivacy'),

    # 내부 테스트 페이지
    path('test', views.webTest, name='webTest'),

    ##################################################
    # 앱 토스터 API
    ##################################################
    # 수신인 관리(PUT/GET/PATCH)
    path('api/target/key/<str:key>', views.apiTarget, name='apiTarget'),

    # 내부 테스트 API
    path('api/test', views.apiTest, name='apiTest'),

    ##################################################
    # PUSH API
    ##################################################
    # PUSH 스케줄 추가(POST)
    path('api/toast_push/key/<str:key>', views.apiToastPush, name='apiToastPush'),

    # PUSH 수정(POST)
    path('api/update_push/key/<str:key>', views.apiUpdatePush, name='apiUpdatePush'),

    # PUSH 스케줄 확인/삭제(GET/DELETE)
    path('api/push/key/<str:key>', views.apiPush, name='apiPush'),

    # PUSH 기록 확인(GET)
    path('api/toasted_push/key/<str:key>', views.apiPushToasted, name='apiPushToasted')
]