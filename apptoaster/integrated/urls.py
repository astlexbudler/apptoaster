from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    ##################################################
    # 웹 페이지 경로
    ##################################################
    ########################################
    # 메인
    ########################################
    path('', views.index, name='index'),

    ########################################
    # 템플릿
    ########################################
    path('template', views.template, name='template'),

    ########################################
    # 이용약관
    ########################################
    path('policy', views.policy, name='policy'),

    ########################################
    # 개인정보 처리방침
    ########################################
    path('privacy', views.privacy, name='privacy'),

    ########################################
    # 광고
    ########################################
    path('ad', views.ad, name='ad'),



    ##################################################
    # 앱 관리
    ##################################################
    ########################################
    # 로그인
    ########################################
    path('login', views.login, name='login'),
    path('api/login', views.apiLogin, name='apiLogin'),
    path('api/logout', views.apiLogout, name='apiLogout'),

    ########################################
    # 대시보드
    ########################################
    path('dash', views.dash, name='dash'),

    ########################################
    # 푸시 관리
    ########################################
    path('push', views.push, name='push'),

    ########################################
    # 일반 설정
    ########################################
    path('general', views.general, name='general'),
    path('general_update', views.generalUpdate, name='generalUpdate'),
    path('api/general_update', views.apiGeneralUpdate, name='apiGeneralUpdate'),

    ########################################
    # 로딩 설정
    ########################################
    path('splash', views.splash, name='splash'),

    ########################################
    # 레이아웃 설정
    ########################################
    path('layout', views.layout, name='layout'),

    ########################################
    # 질문하기
    ########################################
    path('faq', views.faq, name='faq'),
    path('qna', views.qna, name='qna'),
    path('api/qna_create', views.apiQnaCreate, name='apiQnaCreate'),

    ########################################
    # 접속 기록
    ########################################
    path('access_log', views.accessLog, name='accessLog'),

    ########################################
    # 업데이트 기록
    ########################################
    path('update_log', views.updateLog, name='updateLog'),



    ##################################################
    # 앱 토스터 API
    ##################################################
    ########################################
    # 타겟 관리(GET/PATCH)
    ########################################
    path('api/target/id/<str:id>', views.apiTarget, name='apiTarget'),

    ########################################
    # 아이디 생성기
    ########################################
    path('api/id', views.apiId, name='apiId'),

    ########################################
    # 신청
    ########################################
    path('api/contact', views.apiContact, name='apiContact'),
    
    ########################################
    # 테스트
    ########################################
    path('api/test', views.apiTest, name='apiTest'),



    ##################################################
    # 푸시
    ##################################################
    ########################################
    # 푸시 관리(POST/DELETE)
    ########################################
    path('api/push/id/<str:id>', views.apiPush, name='apiPush'),

    ##################################################
    # EVERYPUSH ORIGINAL
    ##################################################
    ########################################
    # 에브리푸시 이용약관 및 개인정보처리방침
    ########################################
    path('terms', views.everypushTerms, name='everypushTerms'),
    ########################################
    # 유저 부가정보(ADDITIONAL USER DATA)
    ########################################
    path('api/get_additional_user_data', views.everypushGetAdditionalData, name='everypushGetAdditionalData'),
    ########################################
    # 결제페이지
    ########################################
    path('payments', views.everypushPayments, name='everypushPayments'),
    ########################################
    # 결제결과페이지(임시)
    ########################################
    path('payments_result', views.everypushPaymentsResult, name='everypushPaymentsResult'),
    ########################################
    # 일반결제 성공
    ########################################
    path('payments_success', views.everypushPaymentsSuccess, name='everypushPaymentsSuccess'),
    ########################################
    # 일반결제 실패
    ########################################
    path('payments_fail', views.everypushPaymentsFail, name='everypusPaymentsFail'),
    ########################################
    # 빌링결제 성공
    ########################################
    path('billing_success', views.everypushBillingSuccess, name='everypushBillingSuccess'),
    ########################################
    # 빌링결제 실패
    ########################################
    path('billing_fail', views.everypushBillingFail, name='everypushBillingFail'),
    ########################################
    # 빌링 연장
    ########################################
    path('renew_billing', views.everypushRenewBilling, name='everypushRenewBilling'),

]