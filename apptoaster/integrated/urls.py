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

    # 템플릿 페이지
    path('template', views.webTemplate, name='webTemplate'),

    # 내부 테스트 페이지
    path('test', views.webTest, name='webTest'),

    ##################################################
    # 앱 토스터 API
    ##################################################
    # 수신인 관리(GET/PATCH)
    path('api/target/key/<str:key>', views.apiTarget, name='apiTarget'),
    # 수신인 확인(GET)
    # request https://apptoaster.co.kr/api/target/key/{key}?deviceType={gcm/apns}&token={token}
    # response
    # 1. 사용자가 등록되지 않았을 경우 사용자 테이블 생성 후
    # status: new
    # target: {
    #     id, token, toasterId, deviceType, isPushAllow, pushAllowDatetime, isAdAllow, adAllowDatetime, lastActivateDate
    # }
    # 2. 사용자가 등록되어있을 경우
    # status: exist
    # target: {
    #     id, token, toasterId, deviceType, isPushAllow, pushAllowDatetime, isAdAllow, adAllowDatetime, lastActivateDate
    # }
    # 3. 키 정보가 없을 경우
    # status: denied
    # target: null
    #
    # 수신인 업데이트(PATCH)
    # request https://apptoaster.co.kr/api/target/key/{key}?id={id}&isPush={isPush}&isAd={isAd}
    # response
    # target: {
    #    id, token, toasterId, deviceType, isPushAllow, pushAllowDatetime, isAdAllow, adAllowDatetime, lastActivateDate
    # }
    
    # 내부 테스트 API
    path('api/test', views.apiTest, name='apiTest'),

    ##################################################
    # PUSH
    ##################################################
    # PUSH 스케줄 추가(POST)
    path('api/toast_push/key/<str:key>', views.apiToastPush, name='apiToastPush'),
    # request https://apptoaster.co.kr/api/toast_push/key/{key}
    # data : alias, title, message, repeat, date, time, ad, to?
    # response toast_push_success.html/toast_push_fail.html

    # PUSH 수정(POST)
    path('api/update_push/key/<str:key>', views.apiUpdatePush, name='apiUpdatePush'),
    # request https://apptoaster.co.kr/api/toast_push/key/{key}
    # data : id?, alias, title, message, repeat, date, time, ad, to?
    # response isSucceed

    # PUSH 스케줄 확인/삭제(GET/DELETE)
    path('api/push/key/<str:key>', views.apiPush, name='apiPush'),
    # PUSH 스케줄 확인(GET)
    # request https://apptoaster.co.kr/api/push/key/{key}
    # response isSucceed, pushList
    # PUSH 스케줄 삭제(DELETE)
    # request https://apptoaster.co.kr/api/push/key/{key}?id={id}&alias={alias}
    # response isSucceed

    # PUSH 기록 확인(GET)
    path('api/toasted_push/key/<str:key>', views.apiPushToasted, name='apiPushToasted')
    # request https://apptoaster.co.kr/api/toasted_push/key/{key}?page={page}
    # response page, pushList
]