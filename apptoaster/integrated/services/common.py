import datetime
import time
import random
import math

import logging
logger = logging.getLogger('appToaster')

'''
common.py
데이터베이스 관련 기능을 관리하는 서비스입니다.
'''

##################################################
# 타임스탬프 생성(1970년부터 timedelta)
##################################################
def getTimestamp():
    return str(int(time.time()*1000))



##################################################
# 아이디 생성(오늘 날짜)
##################################################
def getId():
    # 예 - 20231231235517000000
    str = datetime.datetime.now().strftime("%m%d%H%M%S%f") + '000000'
    return  str[0:20]



##################################################
# 랜덤 문자열 생성
##################################################
def getRandomString(length):
    str = ""
    pool = "123456789qwertyupasdfghkzxcvbnmQWERTYUPASDFGHJKLZXCVBNM"

    for i in range(length):
        str += random.choice(pool)

    return str



##################################################
# 랜덤 숫자 생성
##################################################
def getRandomNumber(length):
    str = ""
    pool = "123456789"

    for i in range(length):
        str += random.choice(pool)

    return str



##################################################
# datetime 을 문자열로
##################################################
def datetimeToString(datetime):
    try: 
        return datetime.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""



##################################################
# date 을 문자열로
##################################################
def dateToString(date):
    try: 
        return date.strftime("%Y-%m-%d")
    except:
        return ""



##################################################
# time 을 문자열로
##################################################
def timeToString(date):
    try: 
        return date.strftime("%H:%M:%S")
    except:
        return ""

##################################################
# time 을 delta로
##################################################
def timeToDelta(time):
    try: 
        hour = time.hour
        minute = time.minute
        second = time.second
        
        return datetime.timedelta(hours=hour, minutes=minute, seconds=second)
    except:
        return ""



##################################################
# 문자열을 datetime 으로
##################################################
def stringToDatetime(string):
    if string != '':
        return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
    else:
        return datetime.datetime.now()



##################################################
# 문자열을 date 으로
##################################################
def stringToDate(string):
    if string != '':
        return datetime.datetime.strptime(string, "%Y-%m-%d")
    else:
        return datetime.date.today()



##################################################
# 문자열을 time 으로
##################################################
def stringToTime(string):
    try:
        if string != '':
            return datetime.datetime.strptime(string, "%H:%M:%S")
        else:
            return datetime.datetime.now().time()
    except:
        return datetime.datetime.now().time()



##################################################
# 두 시간 사이 차
##################################################
def subtractDatetime(datetime1, datetime2):
    if datetime1 == "":
        datetime1 = datetime.datetime.now()

    if datetime2 == "":
        datetime2 = datetime.datetime.now()

    datetime1 = datetime.datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S")
    datetime2 = datetime.datetime.strptime(datetime2, "%Y-%m-%d %H:%M:%S")

    residual_seconds = 0
    delta = datetime1 - datetime2

    try:
        delta_microseconds = delta.microseconds
        sec_microseconds = delta_microseconds / 1000000
        residual_seconds += sec_microseconds
    except:
        pass
    try:
        delta_milliseconds = delta.milliseconds
        sec_milliseconds = delta_milliseconds / 1000
        residual_seconds += sec_milliseconds
    except:
        pass
    try:
        delta_seconds = delta.seconds
        sec_seconds = delta_seconds
        residual_seconds += sec_seconds
    except:
        pass
    try:
        delta_minute = delta.minute
        sec_minute = delta_minute * 60
        residual_seconds += sec_minute
    except:
        pass
    try:
        delta_hours = delta.hours
        sec_hours = delta_hours * 3600
        residual_seconds += sec_minute
    except:
        pass
    try:
        delta_days = delta.days
        sec_days = delta_days * 86400
        residual_seconds += sec_days
    except:
        pass
    try:
        delta_weeks = delta.weeks
        sec_weeks = delta_weeks * 604800
        residual_seconds += sec_weeks
    except:
        pass
    residual_seconds = math.trunc(residual_seconds)
    
    return int(residual_seconds)
