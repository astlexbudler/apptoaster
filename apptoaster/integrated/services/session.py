from . import model

'''
session.py
세션 관련 기능을 관리하는 서비스입니다.
'''

##################################################
# 사용자 IP 확인
##################################################
def getIp(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    except Exception() as e:
        model.createSystemLog(9, 'SYSTEM', 'services.session.getIp IP 확인 실패. ' + e)



##################################################
# Key 정보 저장
##################################################
def setKeySession(request, key):
    try:
        request.session['key'] = key

    except Exception() as e:
        model.createSystemLog(9, 'SYSTEM', 'services.session.setKeySession key 세션 생성 실패. ' + e)



##################################################
# key 정보 확인
##################################################
def getSessionKey(request):
    return request.session.get('key', '')