from django.db.models.fields import DateTimeField
from django.shortcuts import render
from rest_framework import serializers, viewsets
from .serializers import LogDataSerializer, LiveDataSerializer
from .models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
import requests
from django.http import HttpResponse, JsonResponse, response
from django.forms.models import model_to_dict
from django.db.models import Avg, Count, Sum, F, DateTimeField
import datetime
from django.utils.dateparse import parse_datetime
from .configData import cupSize, inf, timeCheck
import traceback
import pytz
from datetime import datetime, date , timedelta
import xlrd, xlwt
utc = pytz.UTC

# ResultFileName = "log_data.xls"
# ResultBook = xlwt.Workbook(encoding="utf-8")
# ResultSheet_01_Minute = ResultBook.add_sheet("01")

@api_view(['POST'])
def logsInPeriodAggre(request):
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data) and ('dur_time' in request.data):
            if (request.data['start_time'] and request.data['end_time'] and request.data['dur_time']):
                response = []
                time = parse_datetime(request.data['start_time'])
                time2 = parse_datetime(request.data['end_time'])
                # if(datetime.now(pytz.utc) - time2 <= timedelta(hours=float(23))):
                    # time2= time2.replace(hour=2, minute=30, second=0, microsecond=0)
                    # print(time2)
                mac = request.data['mac_address']
                pin = request.data['pin']
                position = request.data['position']
                type_data_id = request.data['type_data']
                dur_time = request.data['dur_time']
                report_id = request.data['report_id']
                now_set = datetime.now()
                logs_in_period = LogData.objects.values('mac_addr', 'pin', 'sendDataTime').filter(
                    sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                    position=position).filter(type_data=type_data_id).order_by("sendDataTime")

                # try:

                if int(dur_time) == 1 and report_id == str(1):
                    logs_in_period = (
                        OneMinFlow.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'data',
                                                  'sendDataTime')
                        .filter(sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                        )
                    print(logs_in_period)
                    response.append(logs_in_period)
                if int(dur_time) == 5 and report_id == str(1):
                    logs_in_period = (
                        FiveMinFlow.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'data',
                                                   'sendDataTime')
                        .filter(sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                        )
                    response.append(logs_in_period)
                if int(dur_time) == 15 and report_id == str(1):
                    logs_in_period = (
                        FifteenMinFlow.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'data',
                                                      'sendDataTime')
                        .filter(sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                        )
                    response.append(logs_in_period)
                if int(dur_time) == 30 and report_id == str(1):
                    logs_in_period = (
                        ThirtyMinFlow.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'data',
                                                     'sendDataTime')
                        .filter(sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                        )
                    response.append(logs_in_period)
                if int(dur_time) == 60 and report_id == str(1):
                    logs_in_period = (
                        OneHourFlow.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'data',
                                                   'sendDataTime')
                        .filter(sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                        )
                    response.append((logs_in_period))
                if int(dur_time) >= 60 and report_id == str(2):

                    # querynum = Rotation.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on',
                                                       # 'data', 'sendDataTime').filter(
                        # sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                        # position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                    
                    # querynum = Rotation.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on',
                                                       # 'data', 'sendDataTime').filter(
                        # sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                        # position=position).filter(type_data=type_data_id).count()
                    # if querynum :
                    queryset = Rotation.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on',
                                                        'data', 'sendDataTime').filter(
                                        sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                                        position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                    # else :
                        # queryset = Rotation.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on',
                                                            # 'data', 'sendDataTime').filter(mac_addr=mac).filter(pin=pin).filter(
                                        # position=position).filter(type_data=type_data_id).order_by("-sendDataTime")
                        
                        
                    status_before_duration = None
                    while time < time2:
                        if time2 >= datetime.now().replace(tzinfo=utc):
                            time2 = datetime.now().replace(minute=0, second=0, microsecond=0,tzinfo=utc)
                        status_on = None
                        time_set = timedelta(minutes=float(0))
                        result_time_set = timedelta(minutes=float(0))
                        specific_time_null = timedelta(minutes=float(0))
                        temp_time = time + timedelta(minutes=float(request.data['dur_time']))
                        print("debug     ","time: ", time, "time2: ", time2)
                        if temp_time < time2:

                            # print("temp_time",temp_time)
                            logs_in_period_count = (
                                queryset.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on', 'data',
                                                'sendDataTime')
                                .filter(sendDataTime__range=(time, temp_time)).order_by("sendDataTime").count()
                                )
                            if logs_in_period_count :
                                print("debug     ","log in time specified found" )
                                logs_in_period = (
                                    queryset.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on', 'data',
                                                    'sendDataTime')
                                    .filter(sendDataTime__range=(time, temp_time)).order_by("sendDataTime")
                                    )
                            else :
                                
                                print("debug     ","log in time specified not found" )
                                logs_in_period = []
                                logs_in_period_response = Rotation.objects.values('mac_addr', 'pin', 'position',
                                                                                  'type_data_id', 'flag_on',
                                                                                  'data', 'sendDataTime').filter(
                                    mac_addr=mac).filter(pin=pin).filter(
                                    position=position).filter(type_data=type_data_id).filter(sendDataTime__lte=time).order_by("-sendDataTime")[:1]
                                logs_in_period_json = {}
                                for keys in ['mac_addr', 'pin', 'position', 'type_data_id', 'flag_on', 'data', 'sendDataTime']:
                                    if keys == 'sendDataTime':
                                        if logs_in_period_response[0][keys] < time :
                                            logs_in_period_json[keys] = time
                                        else:
                                            logs_in_period_json[keys] = logs_in_period_response[0][keys]
                                    else:
                                        logs_in_period_json[keys] = logs_in_period_response[0][keys]
                                logs_in_period.append(logs_in_period_json)
                                pass
                            
                            for item in logs_in_period:
                                if item['flag_on'] == 'on' and status_before_duration != 'null':
                                    status_before_duration = 'on'
                                    if status_on is None:
                                        status_on = 'on'
                                        time_set = item['sendDataTime']
                                    elif status_on == 'off':
                                        status_on = 'on'
                                        time_set = item['sendDataTime']

                                elif item['flag_on'] == 'off' and status_before_duration != 'null':
                                    status_before_duration = 'off'
                                    if status_on is None:  # virtual on
                                        status_on = 'off'
                                        time_set = item['sendDataTime']
                                        result_time_set = result_time_set + (
                                                    item['sendDataTime'].replace(tzinfo=utc) - time.replace(
                                                tzinfo=utc))
                                    elif status_on == 'on':
                                        status_on = 'off'
                                        result_time_set = result_time_set + (
                                                    item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                                tzinfo=utc))
                                        time_set = item['sendDataTime']
                                elif item['flag_on'] is None and status_before_duration == 'on':
                                    status_before_duration = 'null'
                                    time_set = item['sendDataTime']
                                    status_on = 'null'
                                    result_time_set = result_time_set + (
                                            item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                        tzinfo=utc))
                                elif item['flag_on'] is None and status_before_duration == 'off':
                                    status_before_duration = 'null'
                                    time_set = item['sendDataTime']
                                    status_on = 'null'
                                elif (item['flag_on'] == 'on' or item['flag_on'] == 'off') and status_before_duration == 'null':
                                    status_before_duration = item['flag_on']
                                    time_set = item['sendDataTime']
                                    status_on = item['flag_on']
                                    specific_time_null = specific_time_null + (
                                            item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                        tzinfo=utc))


                            if status_on == 'on':  # virtual off
                                result_time_set = result_time_set + (
                                            temp_time.replace(tzinfo=utc) - time_set.replace(tzinfo=utc))

                            elif status_on is None and status_before_duration == 'on':
                                result_time_set = time2 + timedelta(
                                    minutes=float(request.data['dur_time'])) - temp_time

                            if status_on == 'null':  # virtual off
                                specific_time_null = specific_time_null + (
                                            temp_time.replace(tzinfo=utc) - time_set.replace(tzinfo=utc))

                            elif status_on is None and status_before_duration == 'null':
                                specific_time_null = time2 + timedelta(
                                    minutes=float(request.data['dur_time'])) - temp_time

                            if result_time_set == '0:00:00':
                                time = temp_time
                            else:
                                response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                                  "type_data_id": type_data_id, "sendDataTime": time, "status": "real",
                                                  "data": result_time_set / 60}))
                            if specific_time_null == '0:00:00':
                                time = temp_time
                            else:
                                response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                                  "type_data_id": type_data_id, "sendDataTime": time,
                                                  "status": "fake",
                                                  "data": specific_time_null / 60}))
                                time = temp_time
                        else:
                            # print("temp_time",temp_time)
                            logs_in_period_count = (
                                queryset.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on', 'data',
                                                'sendDataTime')
                                .filter(sendDataTime__range=(time, time2)).order_by("sendDataTime").count()
                                )
                            
                            
                            if logs_in_period_count :
                                logs_in_period = (
                                queryset.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on', 'data',
                                                'sendDataTime')
                                .filter(sendDataTime__range=(time, time2)).order_by("sendDataTime")
                                )
                            else :
                                logs_in_period = []
                                logs_in_period_response = Rotation.objects.values('mac_addr', 'pin', 'position',
                                                                                  'type_data_id', 'flag_on',
                                                                                  'data', 'sendDataTime').filter(
                                    mac_addr=mac).filter(pin=pin).filter(
                                    position=position).filter(type_data=type_data_id).filter(sendDataTime__lte=time).order_by("-sendDataTime")[:1]
                                logs_in_period_json = {}
                                for keys in ['mac_addr', 'pin', 'position', 'type_data_id', 'flag_on', 'data', 'sendDataTime']:
                                    if keys == 'sendDataTime':
                                        if logs_in_period_response[0][keys] < time :
                                            logs_in_period_json[keys] = time
                                        else:
                                            logs_in_period_json[keys] = logs_in_period_response[0][keys]
                                    else:
                                        logs_in_period_json[keys] = logs_in_period_response[0][keys]
                                logs_in_period.append(logs_in_period_json)

                            for item in logs_in_period:
                                if item['flag_on'] == 'on' and status_before_duration != 'null':
                                    status_before_duration = 'on'
                                    if status_on is None:
                                        status_on = 'on'
                                        time_set = item['sendDataTime']
                                    elif status_on == 'off':
                                        status_on = 'on'
                                        time_set = item['sendDataTime']

                                elif item['flag_on'] == 'off' and status_before_duration != 'null':
                                    status_before_duration = 'off'
                                    if status_on is None:  # virtual on
                                        status_on = 'off'
                                        time_set = item['sendDataTime']
                                        result_time_set = result_time_set + (
                                                    item['sendDataTime'].replace(tzinfo=utc) - time.replace(
                                                tzinfo=utc))
                                    elif status_on == 'on':
                                        status_on = 'off'
                                        result_time_set = result_time_set + (
                                                    item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                                tzinfo=utc))
                                        time_set = item['sendDataTime']
                                elif item['flag_on'] is None and status_before_duration == 'on':
                                    status_before_duration = 'null'
                                    time_set = item['sendDataTime']
                                    status_on = 'null'
                                    result_time_set = result_time_set + (
                                            item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                        tzinfo=utc))
                                elif item['flag_on'] is None and status_before_duration == 'off':
                                    status_before_duration = 'null'
                                    time_set = item['sendDataTime']
                                    status_on = 'null'
                                elif (item['flag_on'] == 'on' or item['flag_on'] == 'off') and status_before_duration == 'null':
                                    status_before_duration = item['flag_on']
                                    time_set = item['sendDataTime']
                                    status_on = item['flag_on']
                                    specific_time_null = specific_time_null + (
                                            item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                        tzinfo=utc))


                            if status_on == 'on':  # virtual off
                                result_time_set = result_time_set + (
                                            time2.replace(tzinfo=utc) - time_set.replace(tzinfo=utc))

                            elif status_on is None and status_before_duration == 'on':
                                result_time_set = time2 + timedelta(
                                    minutes=float(request.data['dur_time'])) - temp_time

                            if status_on == 'null':  # virtual off
                                specific_time_null = specific_time_null + (
                                            time2.replace(tzinfo=utc) - time_set.replace(tzinfo=utc))

                            elif status_on is None and status_before_duration == 'null':
                                specific_time_null = time2 + timedelta(
                                    minutes=float(request.data['dur_time'])) - temp_time

                            if result_time_set == '0:00:00':
                                time = time2
                            else:
                                response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                                  "type_data_id": type_data_id, "sendDataTime": time, "status": "real",
                                                  "data": result_time_set / 60}))
                            if specific_time_null == '0:00:00':
                                time = time2
                            else:
                                response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                                  "type_data_id": type_data_id, "sendDataTime": time,
                                                  "status": "fake",
                                                  "data": specific_time_null / 60}))
                                time = time2
                    return Response((response), status=status.HTTP_200_OK)
                if int(dur_time) == 1440 and report_id == str(3):
                    print("1")
                    p_start = datetime.strptime(request.data['p_start_time'], '%H:%M:%S').time()
                    p_end = datetime.strptime(request.data['p_end_time'], '%H:%M:%S').time()
                    print(2, p_start, p_end)
                    logs_in_period2 = Rotation.objects.values('mac_addr', 'pin', 'position', 'type_data_id', 'flag_on',
                                                       'data', 'sendDataTime').filter(
                        sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                        position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                    temp_time = timedelta(minutes=float(1440))
                    time_set = timedelta(minutes=float(0))
                    status_befor_duration = None
                    print("test time", p_start, p_end)
                           
                    while time < time2:

                        status_on = None
                        time_set = timedelta(minutes=float(0))
                        result_time_set = timedelta(minutes=float(0))
                        temp_time = time + timedelta(minutes=float(1440))
                        # print("time", time, temp_time, time2)
                        if temp_time < time2:
                            pass
                        else:
                            temp_time = time2
                            # print("yes", temp_time, time2)

                        queryset = logs_in_period2.filter(sendDataTime__range=(time, temp_time)).filter(
                            sendDataTime__time__range=(p_start, p_end)).order_by(
                            "sendDataTime")
                        print("queryset", queryset)
                        for item in queryset:
                            print(item)
                            if item['flag_on'] == 'on':
                                status_befor_duration = 'on'
                                if status_on is None:
                                    status_on = 'on'
                                    time_set = item['sendDataTime']
                                elif status_on == 'off':
                                    status_on = 'on'
                                    time_set = item['sendDataTime']

                            elif item['flag_on'] == 'off':
                                status_befor_duration = 'off'
                                if status_on is None:  # virtual on
                                    status_on = 'off'
                                    time_set = item['sendDataTime']
                                    #print("test time 1", item['sendDataTime'], p_start)
                                    if (p_start < item['sendDataTime'].time()):
                                        result_time_set = result_time_set + datetime.combine(date.today(), item[
                                            'sendDataTime'].time()) - datetime.combine(
                                            date.today(), p_start)
                                    print("1", result_time_set)
                                elif status_on == 'on':
                                    #print("buuuuuuuuuuuuggggs", item['sendDataTime'], time_set, item )
                                    status_on = 'off'
                                    result_time_set = result_time_set + (
                                            item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                        tzinfo=utc))
                                    time_set = item['sendDataTime']
                                    #print("2", result_time_set)
                                    #print("status_on", status_on)
                        #print("status_on", status_on)
                        if status_on == 'on':  # virtual off
                            print("virtual off")
                            if time_set.time() <= p_end:
                                print("5", time_set.time())
                                result_time_set = result_time_set + datetime.combine(date.today(),
                                                                                     p_end) - datetime.combine(
                                    date.today(), time_set.time())
                                #print("virtual on", result_time_set, p_end, time_set)

                        elif status_on is None and status_befor_duration == 'on':
                            # queryset = logs_in_period2.filter(sendDataTime__range=(time, temp_time)).order_by("sendDataTime")
                            if datetime.now().time() > p_end:
                                result_time_set = datetime.combine(date.today(), p_end) - datetime.combine(
                                    date.today(), p_start)
                            #print(3, result_time_set)
                        print("this",status_befor_duration, status_on, len(queryset), result_time_set )
                        if status_on is None and len(queryset) == 0:
                            queryset2 = Rotation.objects.filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).filter(sendDataTime__range=(time, temp_time)).order_by(
                                "sendDataTime")
                            #print(queryset2)
                            min_time = timedelta(minutes=float(1440))
                            template = None
                            for item in queryset2:
                                # print(item.sendDataTime, item.flag_on, datetime.combine(date.today(), item.sendDataTime.time()) - datetime.combine(
                                        # date.today(), p_start.time()) > timedelta(
                                    # minutes=float(0)),  datetime.combine(date.today(),
                                                                           # item.sendDataTime.time()) - datetime.combine(
                                    # date.today(), p_start.time()) < min_time)
                                    
                                if (datetime.combine(date.today(), item.sendDataTime.time()) - datetime.combine(
                                        date.today(), p_start) > timedelta(
                                    minutes=float(0)) and  datetime.combine(date.today(),
                                                                           item.sendDataTime.time()) - datetime.combine(
                                    date.today(), p_start) < min_time) and item.sendDataTime.time()<p_end:
                                    #print("item", item)
                                    template = item
                                    min_time = datetime.combine(date.today(),
                                                                item.sendDataTime.time()) - datetime.combine(
                                        date.today(), p_start)
                                    status_on = item.flag_on
                                #else: status_on=item.flag_on
                            #print("7",result_time_set,status_on, min_time)
                            if status_on == 'off':##in the last moment this is change to off last state is on 
                                result_time_set = datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start)
                            for item in queryset2:
                                #print(item.sendDataTime, item.flag_on, datetime.combine(date.today(), item.sendDataTime.time()) - datetime.combine(
                                        # date.today(), p_start.time()) < timedelta(
                                    # minutes=float(0)),  datetime.combine(date.today(),
                                                                           # item.sendDataTime.time()) - datetime.combine(
                                    # date.today(), p_start.time()) < min_time)
                                    
                                if (datetime.combine(date.today(), item.sendDataTime.time()) - datetime.combine(
                                        date.today(), p_start) < timedelta(
                                    minutes=float(0)) and  datetime.combine(date.today(),
                                                                           p_start) - datetime.combine(
                                    date.today(), item.sendDataTime.time()) < min_time):
                                    #print("item", item)
                                    template = item
                                    min_time = datetime.combine(date.today(),
                                                                p_start) - datetime.combine(
                                        date.today(), item.sendDataTime.time())
                                    status_on = item.flag_on
                                #else: status_on=item.flag_on
                            #print("9",result_time_set,status_on, min_time)
                            #print("10", datetime.now().time(), p_start.time(), p_end.time())
                            if status_on == 'on' :##in the last moment this is change to off last state is on (to check the bug)
                                print("hsuidbg", datetime.now().time(), p_start)
                                result_time_set = datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start)
                        if result_time_set == timedelta(minutes=float(0)):
                            time = temp_time
                        else:
                            #print("8", result_time_set)
                            if result_time_set > datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start):
                                result_time_set = datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start)
                            if datetime.date(time) != datetime.date(datetime.today()):
                                print(datetime.date(time), datetime.date(datetime.today()))
                            # print("resu", result_time_set, type(result_time_set), result_time_set == '0:00:00')
                                response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                                  "type_data_id": type_data_id, "sendDataTime": time, "status": "real",
                                                  "data": result_time_set / 60}))
                            time = temp_time
                    return Response((response), status=status.HTTP_200_OK)
                if int(dur_time) == 10080 and report_id == str(3):
                    print("3333333333333333333333333333333333333333333333")
                    p_start = datetime.strptime(request.data['p_start_time'], '%H:%M:%S').time()
                    p_end = datetime.strptime(request.data['p_end_time'], '%H:%M:%S').time()
                    logs_in_period2 = Rotation.objects.values('mac_addr', 'pin', 'position', 'type_data_id',
                                                              'flag_on',
                                                              'data', 'sendDataTime').filter(
                        sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(pin=pin).filter(
                        position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                    temp_time = timedelta(minutes=float(1440))
                    time_set = timedelta(minutes=float(0))
                    status_befor_duration = None
                    total_result_time = timedelta(minutes=float(0))
                    counter = 0
                    time_show = time
                    while time < time2:
                        counter = counter + 1
                        status_on = None
                        time_set = timedelta(minutes=float(0))
                        result_time_set = timedelta(minutes=float(0))
                        temp_time = time + timedelta(minutes=float(1440))
                        print(time, temp_time, time2)
                        if temp_time < time2:
                            pass
                        else:
                            temp_time = time2
                            print("yes", temp_time, time2)

                        queryset = logs_in_period2.filter(sendDataTime__range=(time, temp_time)).filter(
                            sendDataTime__time__range=(p_start.time(), p_end.time())).order_by(
                            "sendDataTime")
                        print("query", queryset)
                        for item in queryset:
                            if item['flag_on'] == 'on':
                                status_befor_duration = 'on'
                                if status_on is None:
                                    status_on = 'on'
                                    time_set = item['sendDataTime']
                                elif status_on == 'off':
                                    status_on = 'on'
                                    time_set = item['sendDataTime']

                            elif item['flag_on'] == 'off':
                                status_befor_duration = 'off'
                                if status_on is None:  # virtual on
                                    status_on = 'off'
                                    time_set = item['sendDataTime']
                                    if (p_start.time() < item['sendDataTime'].time()):
                                        result_time_set = result_time_set + datetime.combine(date.today(), item[
                                            'sendDataTime'].time()) - datetime.combine(
                                            date.today(), p_start.time())
                                    print("1", result_time_set)
                                elif status_on == 'on':
                                    status_on = 'off'
                                    result_time_set = result_time_set + (
                                            item['sendDataTime'].replace(tzinfo=utc) - time_set.replace(
                                        tzinfo=utc))
                                    time_set = item['sendDataTime']

                        if status_on == 'on':  # virtual off
                            if time_set.time() <= p_end.time():
                                result_time_set = result_time_set + datetime.combine(date.today(),
                                                                                     p_end.time()) - datetime.combine(
                                    date.today(), time_set.time())
                                print("virtual on", result_time_set, p_end, time_set)

                        elif status_on is None and status_befor_duration == 'on':
                            # queryset = logs_in_period2.filter(sendDataTime__range=(time, temp_time)).order_by("sendDataTime")
                            if datetime.now().time() > p_end.time():
                                result_time_set = datetime.combine(date.today(),
                                                                   datetime.now().time()) - datetime.combine(
                                    date.today(), p_start.time())
                        if status_on is None and len(queryset) == 0:
                            queryset2 = Rotation.objects.filter(mac_addr=mac).filter(pin=pin).filter(
                            position=position).filter(type_data=type_data_id).filter(sendDataTime__range=(time, temp_time)).order_by(
                                "sendDataTime")
                            print("queryset", queryset2)
                            min_time = timedelta(minutes=float(1440))
                            template = None
                            for item in queryset2:
                                print(item.sendDataTime, item.id)
                                if datetime.combine(date.today(), item.sendDataTime.time()) - datetime.combine(
                                        date.today(), p_start.time()) > timedelta(
                                    minutes=float(0)) and datetime.combine(date.today(),
                                                                           item.sendDataTime.time()) - datetime.combine(
                                    date.today(), p_start.time()) < min_time:
                                    template = item
                                    min_time = datetime.combine(date.today(),
                                                                item.sendDataTime.time()) - datetime.combine(
                                        date.today(), p_start.time())
                                    status_on = item.flag_on
                            if status_on == 'on':
                                result_time_set = datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start)
                        if result_time_set == timedelta(minutes=float(0)):
                            time = temp_time
                        else:
                            if result_time_set > datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start):
                                result_time_set = datetime.combine(date.today(), p_end) - datetime.combine(date.today(), p_start)
                            total_result_time = total_result_time + result_time_set
                        if counter % 7 == 0:
                            #print("counter",counter)
                            response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                              "type_data_id": type_data_id,"status": "real",
                                              "sendDataTime": time_show + timedelta(minutes=float(5040)),
                                              "data": total_result_time / 60}))
                            total_result_time = timedelta(minutes=float(0))
                            time_show = temp_time
                        time = temp_time
                    response.append(({"mac_addr": mac, "pin": pin, "position": position,
                                                  "type_data_id": type_data_id,"status": "real",
                                                  "sendDataTime": time_show + timedelta(minutes=float(5040)),
                                                  "data": total_result_time / 60}))
                    return Response((response), status=status.HTTP_200_OK)
                return Response((logs_in_period), status=status.HTTP_200_OK)
                # except:
                    # traceback.print_exc()
                    # return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logsInPeriodData(request):
    #ResultSheet_01_MinuteNumberOfRowsEntered = 0
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data):
            if (request.data['start_time'] and request.data['end_time']):
                response = []
                time = parse_datetime(request.data['start_time'])
                time2 = parse_datetime(request.data['end_time'])
                mac = request.data['mac_address']
                pin = request.data['pin']
                position = request.data['position']
                type_data_id = request.data['type_data']
                print(request.data)
                try:
                    logs_in_period = (LogData.objects
                                      .values('id', 'mac_addr', 'pin', 'position', 'type_data_id', 'data',
                                              'sendDataTime')
                                      .filter(sendDataTime__range=(time, time2)).filter(mac_addr=mac).filter(
                        pin=pin).filter(position=position).filter(type_data=type_data_id).order_by("sendDataTime")
                                      )
                    # ResultSheet_01_MinuteNumberOfRowsEntered = ResultSheet_01_MinuteNumberOfRowsEntered + 1
                    # for item in logs_in_period:
                        
                        # ResultSheet_01_Minute.write(ResultSheet_01_MinuteNumberOfRowsEntered,1, str(item["sendDataTime"]))
                        # ResultSheet_01_MinuteNumberOfRowsEntered = ResultSheet_01_MinuteNumberOfRowsEntered + 1
                    # ResultBook.save(ResultFileName)
                    print(logs_in_period)
                    response.append((logs_in_period))
                    return Response((logs_in_period), status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)

