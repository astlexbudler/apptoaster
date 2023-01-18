from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    ##################################################
    # Web
    ##################################################
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),

    ##################################################
    # 앱 토스터 API
    ##################################################
    path('apptoaster/set_user/', views.apptoasterSetUser, name='apptoasterSetUser'),
    path('apptoaster/get_user/', views.apptoasterGetUser, name='apptoasterGetUser'),
    path('apptoaster/delete_user/', views.apptoasterDeleteUser, name='apptoasterDeleteUser'),
    path('apptoaster/send_notification_to_user/', views.apptoasterSendNotificationToUser, name='apptoasterSendNotificationToUser'),
    path('apptoaster/send_notification_to_all/', views.apptoasterSendNotificationToAll, name='apptoasterSendNotificationToAll'),

    ##################################################
    # 카카오 PUSH API(TEST)
    ##################################################
    path('kakao_register_push_token/', views.kakaoRegisterPushToken, name="kakaoRegisterPushToken"),
    path('kakao_get_push_token/', views.kakaoGetPushToken, name="kakaoGetPushToken"),
    path('kakao_delete_push_token/', views.kakaoDeletePushToken, name="kakaoDeletePushToken"),
    path('kakao_send_push_notification/', views.kakaoSendPushNotification, name="kakaoSendPushNotification"),
]