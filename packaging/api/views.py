import traceback
from datetime import datetime
from django.utils.dateparse import parse_datetime
import json
import requests
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.models import Sum, F
from packaging.api.serializers import PackagingLiveDataSerializer, PackagingLlogDataSerializer, AlarmSerializer, \
    TypeOfAlarmSerializer, AggregateDataSerializer, StoppageTimeSerializer
from packaging.models import *
from packaging.ConfigData import list_of_alarm
import time 
global aggregate_data_flag, aggregate_data, aggregate_data_array
aggregate_data = {}
aggregate_data_flag = False
aggregate_data_array = []


@api_view(['POST'])
def SendDataPackaging(request):
    global aggregate_data_flag, aggregate_data
    if request.method == 'POST':
        print(len(request.data), request.data)
        if len(request.data) == 0:
            return Response({"no data recieved"}, status=status.HTTP_400_BAD_REQUEST)
        # for i in range(0, len(request.data)):
        try:
            before_data = PackagingLiveData.objects.get(mac_addr=request.data['mac_addr'])
            # print("before_live_data", before_data)
        except:
            print("Notfound  before live data")
        if request.data['type_of_data'] == 'production':
            print('production')
            data = {'mac_addr': request.data['mac_addr'], 'datatime': request.data['time'],
                    'degree1': request.data['degree1'], 'degree2': request.data['degree2'],
                    'degree3': request.data['degree3'], 'degree4': request.data['degree4'],
                    'degree5': request.data['degree5'], 'degree6': request.data['degree6']}
            try:
                if request.data['degree1'] is None and request.data['degree2'] is None and request.data[
                    'degree3'] is None and request.data['degree4'] is None and request.data['degree5'] is None and \
                        request.data['degree6'] is None:
                    return Response({"data": "None data in row"}, status=status.HTTP_200_OK)
                packaginglivedata = PackagingLiveData.objects.get(mac_addr=data['mac_addr'])
                try:
                    PackagingLiveData.objects.filter(mac_addr=data['mac_addr']). \
                        update(datatime=data['datatime'], degree1=data['degree1'], degree2=data['degree2'],
                               degree3=data['degree3'], degree4=data['degree4'],
                               degree5=data['degree5'], degree6=data['degree6'])
                except:
                    return Response(traceback.print_exc(), status=status.HTTP_400_BAD_REQUEST)

            except PackagingLiveData.DoesNotExist:
                packaging_serializer = PackagingLiveDataSerializer(data=data)
                if packaging_serializer.is_valid():
                    packaging_serializer.save()
                else:
                    return Response(packaging_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if (data['degree1'] < before_data.degree1 or data['degree2'] < before_data.degree2 or
                    data['degree3'] < before_data.degree3 or data['degree4'] < before_data.degree4
                    or data['degree5'] < before_data.degree5 or data['degree6'] < before_data.degree6):
                flag_start = True
                aggregate_data_array.append(aggregate_data)
                aggregate_data_flag = True
                print("start")
                print(aggregate_data_array)
                print("time", datetime.fromtimestamp(data['datatime']))
            else:
                flag_start = False
                aggregate_data = data
            # if not flag_start:
            # print(aggregate_data, data)
            # aggregate_data = before_data
            aggregate_data_time = datetime.fromtimestamp(data['datatime'])
            print((aggregate_data_time.hour == 10 and aggregate_data_time.minute == 30), (
                    aggregate_data_time.hour == 18 and aggregate_data_time.minute == 30), (
                        aggregate_data_time.hour == 2 and aggregate_data_time.minute == 30))
            if ((aggregate_data_time.hour == 10 and aggregate_data_time.minute == 30) or (
                    aggregate_data_time.hour == 18 and aggregate_data_time.minute == 30) or (
                        aggregate_data_time.hour == 2 and aggregate_data_time.minute == 30) and  aggregate_data_flag):
                print("aggregate")
                save_aggregate = {'mac_addr': data['mac_addr'], 'datatime': data['datatime'],
                                  'degree1': 0, 'degree2': 0,
                                  'degree3': 0, 'degree4': 0,
                                  'degree5': 0, 'degree6': 0}
                for item in aggregate_data_array:
                    print(1, item)
                    if data['mac_addr'] == item['mac_addr']:
                        print(2)
                        save_aggregate['degree1'] = save_aggregate['degree1'] + item['degree1']
                        save_aggregate['degree2'] = save_aggregate['degree2'] + item['degree2']
                        save_aggregate['degree3'] = save_aggregate['degree3'] + item['degree3']
                        save_aggregate['degree4'] = save_aggregate['degree4'] + item['degree4']
                        save_aggregate['degree5'] = save_aggregate['degree5'] + item['degree5']
                        save_aggregate['degree6'] = save_aggregate['degree6'] + item['degree6']
                        aggregate_data_array.remove(item)
                aggregatedata_serializer = AggregateDataSerializer(data=save_aggregate)
                if aggregatedata_serializer.is_valid():
                    aggregatedata_serializer.save()
                else:
                    print("error in aggregate_data!!")
                        
                    
                aggregate_data_flag = False
            elif not ((aggregate_data_time.hour == 10 and aggregate_data_time.minute == 30) or (
                    aggregate_data_time.hour == 18 and aggregate_data_time.minute == 30) or (
                              aggregate_data_time.hour == 2 and aggregate_data_time.minute == 30)):
                aggregate_data_flag = False
            # if aggregate_data_flag:
            #     try:
            #         aggregate_record = AggregateData.objects.filter(mac_addr=data['mac_addr']).filter(
            #             datatime=data['datatime'])
            #     except:
            #         pass
            #     if aggregate_record:
            #         AggregateData.objects.filter(mac_addr=data['mac_addr']).filter(datatime=data['datatime']).update(
            #             degree1=aggregate_data['degree1'], degree2=aggregate_data['degree2'],
            #             degree3=aggregate_data['degree3'], degree4=aggregate_data['degree4'],
            #             degree5=aggregate_data['degree5'], degree6=aggregate_data['degree6'])
            #     else:
            #         aggregatedata_serializer = AggregateDataSerializer(data=aggregate_data)
            #         print("aggregate data", aggregate_data.degree1, data, aggregatedata_serializer)
            #         if aggregatedata_serializer.is_valid():
            #             aggregatedata_serializer.save()
            #         else:
            #             print("error in aggregate_data!!")

            # try:
            # before_data = PackagingLlogData.objects.filter(mac_addr=request.data['mac_addr']).order_by('datatime').latest('id')
            try:
                check_duplicated = PackagingLlogData.objects.get(datatime=request.data['time'])
                if check_duplicated:
                    print("duplicated")
                    return Response(status=status.HTTP_202_ACCEPTED)
            except:
                pass
            if not flag_start:
                print(data['degree1'], before_data.degree1, data['degree2'], before_data.degree2, data['degree3'],
                      before_data.degree3, data['degree4'], before_data.degree4,
                      data['degree5'], before_data.degree5,
                      data['degree6'], before_data.degree6)
                data_log = {'mac_addr': request.data['mac_addr'], 'datatime': request.data['time'],
                            'degree1': data['degree1'] - before_data.degree1,
                            'degree2': data['degree2'] - before_data.degree2,
                            'degree3': data['degree3'] - before_data.degree3,
                            'degree4': data['degree4'] - before_data.degree4,
                            'degree5': data['degree5'] - before_data.degree5,
                            'degree6': data['degree6'] - before_data.degree6}
            else:
                data_log = {'mac_addr': request.data['mac_addr'], 'datatime': request.data['time'],
                            'degree1': data['degree1'],
                            'degree2': data['degree2'],
                            'degree3': data['degree3'],
                            'degree4': data['degree4'],
                            'degree5': data['degree5'],
                            'degree6': data['degree6']}
            # except PackagingLlogData.DoesNotExist:
            # data_log = {'mac_addr': request.data['mac_addr'], 'datatime': request.data['time'],
            # 'degree1': data['degree1'],
            # 'degree2': data['degree2'],
            # 'degree3': data['degree3'],
            # 'degree4': data['degree4'],
            # 'degree5': data['degree5'],
            # 'degree6': data['degree6']}
            packagingLlogData_serializer = PackagingLlogDataSerializer(data=data_log)
            if packagingLlogData_serializer.is_valid():
                packagingLlogData_serializer.save()
            else:
                return Response(packagingLlogData_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data['type_of_data'] == 'error':
            id_code = TypeOfAlarm.objects.filter(code=request.data['code'])
            print('error')
            if id_code:
                id_code = TypeOfAlarm.objects.filter(code=request.data['code'])
                duplicated = Alarm.objects.filter(mac_addr=request.data['mac_addr']).filter(
                    alarm_row=request.data['error_id']).filter(start_time=request.data['start_time'])
                if duplicated:
                    try:
                        Alarm.objects.filter(mac_addr=request.data['mac_addr']).filter(
                            alarm_row=request.data['error_id']) \
                            .filter(start_time=request.data['start_time']).update(end_time=request.data['end_time'])

                    except:
                        return Response(traceback.print_exc(), status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {'mac_addr': request.data['mac_addr'],
                            'alarm_row': request.data['error_id'], 'start_time': request.data['start_time'],
                            'end_time': request.data['end_time'], 'type_of_alarm': id_code[0].id}
                    Alarm_serializer = AlarmSerializer(data=data)
                    if Alarm_serializer.is_valid():
                        Alarm_serializer.save()
                    else:
                        return Response(Alarm_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # all code save when start the program for first time
            else:
                data = {'code': str(request.data['code']), 'section': request.data['section'],
                        'description': request.data['description']}
                # update type of alarm table
                type_alarm_serializer = TypeOfAlarmSerializer(data=data)
                if type_alarm_serializer.is_valid():
                    type_alarm_serializer.save()
                else:
                    return Response(type_alarm_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                id_code = TypeOfAlarm.objects.filter(code=request.data['code'])
                # append to list of code
                data = {'mac_addr': request.data['mac_addr'],
                        'alarm_row': request.data['error_id'], 'start_time': request.data['start_time'],
                        'end_time': request.data['end_time'], 'type_of_alarm': id_code[0].id}
                alarm_serializer = AlarmSerializer(data=data)
                if alarm_serializer.is_valid():
                    alarm_serializer.save()
                else:
                    return Response(alarm_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data created"}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def LiveDataPackaging(request):
    # queryset = PackagingLiveData.objects.all()
    # serializer_class = PackagingLiveDataSerializer
    # permission_classes = [AllowAny]
    result = []
    alarm_now = []
    livedata = PackagingLiveData.objects.all()
    for item in livedata:
        data_time = time.time()
        alarm_page = Alarm.objects.filter(mac_addr=item.mac_addr).filter(start_time__lt=data_time).filter(
            end_time__gte=data_time)
        if len(alarm_page) == 0:
            alarm_flag = 0
        else:
            alarm_flag = 1
        for alarm in alarm_page:
            row = {}
            row['mac_addr'] = alarm.mac_addr
            row['start_time'] = alarm.start_time
            row['end_time'] = alarm.end_time
            row['diff_time'] = alarm.end_time - alarm.start_time
            type_of_alarm = TypeOfAlarm.objects.get(id=alarm.type_of_alarm.id)
            row['code'] = type_of_alarm.code
            row['section'] = type_of_alarm.section
            row['description'] = type_of_alarm.description
            alarm_now.append(row)
        result.append(
            {
                "id": item.id,
                "mac_addr": item.mac_addr,
                "datatime": item.datatime,
                "degree1": item.degree1,
                "degree2": item.degree2,
                "degree3": item.degree3,
                "degree4": item.degree4,
                "degree5": item.degree5,
                "degree6": item.degree6,
                "alarm_flag": alarm_flag,
                "alarm": alarm_now
            }
        )

    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def DailyStaticPackaging(request):
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data) and ('dur_time' in request.data):
            if request.data['start_time'] and request.data['end_time'] and request.data['dur_time']:
                response = []
                time = request.data['start_time']
                time2 = request.data['end_time']
                mac = request.data['mac_addr']
                degree = request.data['degree']
                dur_time = request.data['dur_time']
                logs_in_period = PackagingLlogData.objects.filter(
                    datatime__range=(time, time2)).filter(mac_addr=mac).order_by("datatime")
                while time <= time2:
                    print(".......................................................................................................................................................")
                    #try:
                    part_query = logs_in_period.filter(datatime__gte = time, datatime__lt = time+dur_time)
                    degrees = part_query.aggregate(degree_1=Sum('degree1'), degree_2=Sum('degree2'),
                                                  degree_3=Sum('degree3'), degree_4=Sum('degree4'),
                                                  degree_5=Sum('degree5'), degree_6=Sum('degree6'))
                    print(degrees)
                    if len(degrees) == 0:
                        time = time + dur_time
                        continue
                    # ts = time + (dur_time * 0.1)
                    response_field = {"mac_addr": mac, "DataTime": datetime.utcfromtimestamp(time+dur_time/2)}
                    if 1 in degree:
                        print(degrees['degree_2'])
                        response_field["degree1"] = degrees['degree_1']
                    if 2 in degree:
                        response_field["degree2"] = degrees['degree_2']
                    if 3 in degree:
                        response_field["degree3"] = degrees['degree_3']
                    if 4 in degree:
                        response_field["degree4"] = degrees['degree_4']
                    if 5 in degree:
                        response_field["degree5"] = degrees['degree_5']
                    if 6 in degree:
                        response_field["degree6"] = degrees['degree_6']
                    response.append(response_field)
                        # response.append(
                        #     {"mac_addr": mac, "degree1": degrees[0].degree_1, "degree2": degrees[0].degree_2,
                        #      "degree3": degrees[0].degree_3, "degree4": degrees[0].degree_4,
                        #      "degree5": degrees[0].degree_5,
                        #      "degree6": degrees[0].degree_6, "DataTime": datetime.utcfromtimestamp(ts)})
                    # except:
                        # traceback.print_exc()

                    time = time + dur_time

                try:

                    return Response(response, status=status.HTTP_200_OK)
                    # return Response((logs_in_period), status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def StoppageTimePackaging(request):
    if request.method == 'POST':
            if ('start_time' in request.data) and ('end_time' in request.data) and ('dur_time' in request.data):
                dur_start = request.data['start_time']
                dur_end = request.data['end_time']
                dur_dur = request.data['dur_time']
                mac = request.data['mac_addr']
                stoppage_record = StoppageTime.objects.filter(
                    dur_start__range=(dur_start, dur_end), mac_addr=mac)
                stoppage_record_ser = StoppageTimeSerializer(stoppage_record, many=True)
                stoppage_lst = []
                while dur_start < dur_end:
                    stacker_sum = 0
                    packaging_sum = 0
                    for record in stoppage_record_ser.data:
                        if record['dur_start'] in range(dur_start, dur_start + dur_dur):
                            if record['section'] == "Stacker":
                                if stacker_sum is None:
                                    stacker_sum = record['dur_stoppage']
                                else:
                                    stacker_sum += record['dur_stoppage']
                            elif record['section'] == "Packaging machine":
                                if packaging_sum is None:
                                    packaging_sum = record['dur_stoppage']
                                else:
                                    packaging_sum += record['dur_stoppage']
                    stoppage_json = {'mac_addr': mac,
                                     'DataTime': datetime.utcfromtimestamp(dur_start + dur_dur / 2),
                                     'stoppage_time_stacker': stacker_sum,
                                     'stoppage_time_packaging': packaging_sum,
                                     }
                    stoppage_lst.append(stoppage_json)

                    dur_start += dur_dur
                try:
                    return Response(stoppage_lst, status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def LogDataPackaging(request):
    global logs_in_period
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data):
            response = []
            time = request.data['start_time']
            time2 = request.data['end_time']
            mac = request.data['mac_addr']
            if ('start_time' in request.data) and ('end_time' in request.data) and ('section' not in request.data) \
                    and ('description' not in request.data):
                if request.data['start_time'] and request.data['end_time']:
                    logs_in_period = Alarm.objects.values('mac_addr', 'start_time', 'end_time', 'type_of_alarm'
                                                          , 'alarm_row').filter(
                        start_time__range=(time, time2)).filter(mac_addr=mac).order_by("start_time")
                else:
                    return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
            elif ('start_time' in request.data) and ('end_time' in request.data) and \
                    (('section' in request.data) or ('description' in request.data)):
                if request.data['start_time'] and request.data['end_time'] and request.data['section']:
                    type_of_alarm = TypeOfAlarm.objects.filter(section=request.data['section'])
                    logs_in_period = Alarm.objects.values('mac_addr', 'start_time', 'end_time', 'type_of_alarm'
                                                          , 'alarm_row').filter(
                        start_time__range=(time, time2)).filter(mac_addr=mac).filter(
                        type_of_alarm__in=type_of_alarm).order_by("start_time")

                elif request.data['start_time'] and request.data['end_time'] and request.data['description']:

                    type_of_alarm = TypeOfAlarm.objects.filter(description=request.data['description'])
                    logs_in_period = Alarm.objects.values('mac_addr', 'start_time', 'end_time', 'type_of_alarm'
                                                          , 'alarm_row').filter(
                        start_time__range=(time, time2)).filter(mac_addr=mac).filter(
                        type_of_alarm__in=type_of_alarm).order_by("start_time")

                elif request.data['start_time'] and request.data['end_time'] and request.data['description'] and \
                        request.data['section']:
                    type_of_alarm = TypeOfAlarm.objects.filter(section=request.data['section']).filter(
                        description=request.data['description'])
                    logs_in_period = Alarm.objects.values('mac_addr', 'start_time', 'end_time', 'type_of_alarm'
                                                          , 'alarm_row').filter(
                        start_time__range=(time, time2)).filter(mac_addr=mac).filter(
                        type_of_alarm__in=type_of_alarm).order_by("start_time")
                else:
                    return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
            id_of_table = 0
            for item in logs_in_period:
                row = {}
                id_of_table = id_of_table + 1
                row['id'] = id_of_table
                row['mac_addr'] = mac
                row['start_time'] = item['start_time']
                row['end_time'] = item['end_time']
                row['diff_time'] = row['end_time'] - row['start_time']
                type_of_alarm = TypeOfAlarm.objects.get(id=item['type_of_alarm'])
                row['code'] = type_of_alarm.code
                row['section'] = type_of_alarm.section
                row['description'] = type_of_alarm.description
                response.append(row)
            try:
                return Response(response, status=status.HTTP_200_OK)
            except:
                traceback.print_exc()
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def ErrorFrequencyPackaging(request):
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data):
            if request.data['start_time'] and request.data['end_time']:
                response = []
                time = request.data['start_time']
                time2 = request.data['end_time']
                mac = request.data['mac_addr']
                error = request.data['error']
                error_id = TypeOfAlarm.objects.filter(code__in=error)
                for error_item in error_id:
                    logs_in_period = Alarm.objects.filter(
                        start_time__range=(time, time2)).filter(mac_addr=mac).filter(type_of_alarm=error_item.id)
                    row = {}
                    row['diff_time'] = 0
                    row['code'] = error_item.code
                    row['section'] = error_item.section
                    row['description'] = error_item.description
                    for item in logs_in_period:
                        row['diff_time'] = row['diff_time'] + (item.end_time - item.start_time)

                    response.append(row)
                try:

                    return Response(response, status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def CumulativeChartPackaging(request):
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data) and ('dur_time' in request.data):
            if request.data['start_time'] and request.data['end_time'] and request.data['dur_time']:
                response = []
                time = request.data['start_time']
                time2 = request.data['end_time']
                mac = request.data['mac_addr']
                degree = request.data['degree']
                dur_time = request.data['dur_time']
                logs_in_period = AggregateData.objects.filter(
                    datatime__range=(time, time2)).filter(mac_addr=mac).order_by("datatime")
                while time <= time2:
                    try:
                        part_query = logs_in_period.filter(datatime__range=(time, time + dur_time))
                        degrees = part_query.annotate(degree_1=Sum('degree1'), degree_2=Sum('degree2'),
                                                      degree_3=Sum('degree3'), degree_4=Sum('degree4'),
                                                      degree_5=Sum('degree5'), degree_6=Sum('degree6'))
                        if len(degrees) == 0:
                            time = time + dur_time
                            continue
                        # ts = time + (dur_time * 0.1)
                        response_field = {"mac_addr": mac, "DataTime": datetime.utcfromtimestamp(time+dur_time/2)}
                        if 1 in degree:
                            response_field["degree1"] = degrees[0].degree_1
                        if 2 in degree:
                            response_field["degree2"] = degrees[0].degree_2
                        if 3 in degree:
                            response_field["degree3"] = degrees[0].degree_3
                        if 4 in degree:
                            response_field["degree4"] = degrees[0].degree_4
                        if 5 in degree:
                            response_field["degree5"] = degrees[0].degree_5
                        if 6 in degree:
                            response_field["degree6"] = degrees[0].degree_6
                        response.append(response_field)
                        # response.append(
                        #     {"mac_addr": mac, "degree1": degrees[0].degree_1, "degree2": degrees[0].degree_2,
                        #      "degree3": degrees[0].degree_3, "degree4": degrees[0].degree_4,
                        #      "degree5": degrees[0].degree_5,
                        #      "degree6": degrees[0].degree_6, "DataTime": datetime.utcfromtimestamp(ts)})
                    except:
                        traceback.print_exc()

                    time = time + dur_time

                try:

                    return Response(response, status=status.HTTP_200_OK)
                    # return Response((logs_in_period), status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)


class ErrorListPackaging(generics.ListAPIView):
    queryset = TypeOfAlarm.objects.all()
    serializer_class = TypeOfAlarmSerializer
    permission_classes = [AllowAny]
