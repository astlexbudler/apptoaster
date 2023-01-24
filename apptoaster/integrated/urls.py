from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    ##################################################
    # 웹 페이지 경로
    ##################################################
    # 메인 페이지
    path('', views.webIndex, name='webIndex'),

    # 이용약관
    path('push/policy', views.webPushPolicy, name='webPushPolicy'),

    # 발송 관리 페이지
    path('push/toasting', views.webPushToasting, name='webPushToasting'),

    # 발송 기록 페이지
    path('push/toasted', views.webPushToasted, name='webPushToasted'),

    # 내부 테스트 페이지
    path('test_console/', views.webTestConsole, name='webTestConsole'),

    ##################################################
    # 앱 토스터 API
    ##################################################
    # 수신인 관리(PUT/GET/PATCH)
    path('api/target/key/<str:key>', views.apiTarget, name='apiTarget'),

    # 로그인
    path('api/login/key/<str:key>', views.apiLogin, name='apiLogin'),

    # 로그아웃
    path('api/logout', views.apiLogout, name='apiLogout'),

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
    path('api/push/toasted/key/<str:key>', views.apiPushToasted, name='apiPushToasted'),

    ##################################################
    # CIA(ChurchInApp) API
    ##################################################
    # 수신인 관리(PUT/GET/PATCH/DELETE)
    path('cia/target/key/<str:key>', views.ciaTarget, name='ciaTarget'),

    # PUSH 스케줄 추가(POST)
    path('cia/toast_push/key/<str:key>', views.ciaToastPush, name='ciaToastPush'),

    # PUSH 수정(POST)
    path('cia/update_push/key/<str:key>', views.ciaUpdatePush, name='ciaUpdatePush'),

    # PUSH 스케줄 확인/삭제(GET/DELETE)
    path('cia/push/key/<str:key>', views.ciaPush, name='ciaPush'),

    # PUSH 기록 확인(GET)
    path('cia/push/toasted/key/<str:key>', views.ciaPushToasted, name='ciaPushToasted'),
]