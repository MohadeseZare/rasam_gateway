from django.db.models.fields import DateTimeField
from django.shortcuts import render
from rest_framework import serializers, viewsets
from .serializers import *
from .models import LogData, LiveData, LastOffline
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
import requests
from django.http import HttpResponse, JsonResponse, response
from django.forms.models import model_to_dict
from django.db.models import Avg, Count, Sum, F, DateTimeField, Q
import datetime
from django.utils.dateparse import parse_datetime
from .configData import cupSize, inf, timeCheck, counter_flow, flag_rotate, before_data, offline_counter
from .dataAnalysis import add_data_to_sub_table, add_data_to_rotation_table
import traceback
import pytz
from .offline_data import add_data_to_sub_table, add_data_to_rotation_table, update_last_record_offline_table
import time
utc = pytz.UTC

import psycopg2
import xlrd
import xlwt

ResultFileName = "packaging.xls"
ResultBook = xlwt.Workbook(encoding="utf-8")
ResultSheet = ResultBook.add_sheet("result1")
ResultSheet_NumberOfRowsEntered = 0


def log_out_device():  # to understand the device post has problem
    conn = None
    rows_deleted = 0
    try:
        time_now = datetime.datetime.now()
        conn = psycopg2.connect(database="gateway", user='gatewayuser', password='gateway123', host='localhost',
                                port='')
        cursor = conn.cursor()
        live_data = LiveData.objects.all()
        for item in live_data:
            if datetime.timedelta(minutes=4) <= time_now.replace(tzinfo=utc) - item.sendDataTime.replace(tzinfo=utc):
                cursor.execute("DELETE FROM logs_livedata where id = %s", (item.id,))
                rows_deleted = cursor.rowcount + rows_deleted
                conn.commit()
                cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


class LogDataViewSet(viewsets.ModelViewSet):
    serializer_class = LogDataSerializer
    queryset = LogData.objects.all()


class LiveDataViewSet(viewsets.ModelViewSet):
    serializer_class = LiveDataSerializer
    queryset = LiveData.objects.all()


def checkDiff(currData, prevData, prev_time, present_time):
    diffdata = currData - prevData
    if diffdata < 0:
        diffdata += cupSize
    # ###############################################################################################################################################################
    #  important :
    #       the invalid data is going to bhe replaced with a negetive large number but not inf, sql couldn't store it
    #       and the sum could be positive and cause bug
    # ###############################################################################################################################################################

    if (present_time - prev_time) > timeCheck:
        diffdata = -inf
    return diffdata


@api_view(['POST'])
def add_data(request):
    search_flag = False
    time_flow = datetime.datetime.now()
    global counter_flow, use_new
    use_new = True
    print("online", request.data, len(request.data))
    if request.method == 'POST':
        if (len(request.data) == 0):
            return Response({"no data recieved"}, status=status.HTTP_400_BAD_REQUEST)
        for i in range(0, len(request.data)):
            data = {}
            data['mac_addr'] = request.data[i]['mac_addr']
            if data['mac_addr'] == "ff:ff:ff:ff:ff:ff":
                continue
            #print(type(request.data[i]['unixTime']))
            import time
            localTime = time.localtime()
            #print("timeeeeeeeeeeeeeeees",datetime.datetime.now(utc), datetime.datetime.utcfromtimestamp(float(request.data[i]['unixTime'])), time.time(), (request.data[i]['unixTime']))
            data['sendDataTime'] = datetime.datetime.utcfromtimestamp(float(request.data[i]['unixTime']))
            # print("types_for_time", type(data['sendDataTime']), datetime.datetime.utcfromtimestamp(request.data[i]['unixTime']))
            # for pin in request.data[i]['Data']:
            # if pin['pin'] == 11:
            # data['pin'] = pin['pin']
            # data['data'] = pin['sensor_data']
            # data['position'] = request.data[i]['Modbus'][9]['modbus_data']
            # data['type_data'] = 1
            # if data['data'] == "None":
            # continue
            # diff = 0
            # try:
            # livedata = LiveData.objects.get(mac_addr=data['mac_addr'], pin=data['pin'], position=data['position'], type_data=data['type_data'])
            # prev_data = livedata.data

            # prev_time_updated = (livedata.sendDataTime)
            # prev_time_updated = prev_time_updated.replace(tzinfo=None)
            # # print(prev_time_updated, type(prev_time_updated))
            # present_time = data['sendDataTime']
            # #diff = checkDiff(float(data['data']), float(prev_data), prev_time_updated, present_time)
            # diff = 0.0
            # data['diff_data'] = diff
            # data['updated_at'] = datetime.datetime.now()
            # #print("online_time", data['updated_at'], data['sendDataTime'])
            # # print("time", datetime.datetime.now())
            # # print("data",data)
            # # print("livedata model", livedata)
            # # print("unix time",data['sendDataTime'], "exchanged time", datetime.datetime.fromtimestamp(data['sendDataTime']))
            # try:
            # LiveData.objects.filter(mac_addr=data['mac_addr'], pin=data['pin'], type_data=data['type_data'], position=data['position']).update(data=data['data'], diff_data=data['diff_data'], updated_at=data['updated_at'].replace(tzinfo=None), sendDataTime=data['sendDataTime'].replace(tzinfo=None))
            # except:
            # return Response(traceback.print_exc(),status=status.HTTP_400_BAD_REQUEST)
            # # live_serializer = LiveDataSerializer(data=data)
            # # print("new model", live_serializer)
            # # if live_serializer.is_valid():
            # # live_serializer.save()
            # # livedata.update(live_serializer)
            # # else:
            # #     return Response(live_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # except LiveData.DoesNotExist:
            # live_serializer = LiveDataSerializer(data=data)
            # if live_serializer.is_valid():
            # live_serializer.save()
            # else:
            # return Response(live_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # log_serializer = LogDataSerializer(data=data)
            # if log_serializer.is_valid():
            # log_serializer.save()

            # else:
            # return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # #print(request.data[i]['Modbus'][9]['modbus_data'])
            for pin in request.data[i]['Modbus']:
                if pin['tag'] == 1:
                    #print(request.data[i]['Modbus'])
                    data['pin'] = pin['tag']
                    data['data'] = pin['modbus_data']
                    data['position'] = request.data[i]['Modbus'][9]['modbus_data']
                    data['type_data'] = 2
                    try:
                        livedata = LiveData.objects.get(mac_addr=data['mac_addr'], pin=data['pin'],
                                                        position=data['position'], type_data=data['type_data'])
                        prev_data = livedata.data
                        prev_time_updated = (livedata.sendDataTime)
                        prev_time_updated = prev_time_updated.replace(tzinfo=None)

                        present_time = data['sendDataTime']

                        diff = 0.0
                        data['diff_data'] = diff
                        data['updated_at'] = datetime.datetime.now()
                        # print(data['updated_at'], datetime.datetime.fromtimestamp(data['sendDataTime']))
                        try:

                            LiveData.objects.filter(mac_addr=data['mac_addr'], pin=data['pin'],
                                                    type_data=data['type_data'], position=data['position']
                                                    ).update(data=data['data'],
                                                             diff_data=data['diff_data'],
                                                             updated_at=data[
                                                                 'updated_at'].replace(
                                                                 tzinfo=None),
                                                             sendDataTime=data['sendDataTime'].replace(
                                                                 tzinfo=None))

                        except:
                            return Response(traceback.print_exc(), status=status.HTTP_400_BAD_REQUEST)

                    except LiveData.DoesNotExist:
                        present_time = data['sendDataTime']
                        live_serializer = LiveDataSerializer(data=data)
                        if live_serializer.is_valid():
                            live_serializer.save()
                        else:
                            return Response(live_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        """ add the calculate table!!!!!!"""
                    # # print( present_time, present_time.second)
                    # if present_time.second in range(10):
                        # # print("TEST", present_time, present_time.second)
                        # if counter_flow == 60:
                            # counter_flow = 1
                        # counter_flow = counter_flow + 1
                        # # print(counter_flow)
                        # one_min_serializer = OneMinSerializers(data=data)
                        # if one_min_serializer.is_valid():
                            # one_min_serializer.save()
                        # else:
                            # return Response(one_min_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    # if ((present_time.minute) % 5 == 0) and present_time.second in range(10):
                        # five_min_serializers = FiveMinSerializers(data=data)
                        # if five_min_serializers.is_valid():
                            # five_min_serializers.save()
                        # else:
                            # return Response(five_min_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                    # if ((present_time.minute) % 15 == 0) and present_time.second in range(10):
                        # fifteen_min_serializers = FifteenMinSerializers(data=data)
                        # if fifteen_min_serializers.is_valid():
                            # fifteen_min_serializers.save()
                        # else:
                            # return Response(fifteen_min_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                    # if ((present_time.minute) % 30 == 0) and present_time.second in range(10):
                        # thirty_min_serializers = ThirtyMinSerializers(data=data)
                        # if thirty_min_serializers.is_valid():
                            # thirty_min_serializers.save()
                        # else:
                            # return Response(thirty_min_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                    # if ((present_time.minute) % 60 == 0) and present_time.second in range(10):
                        # one_hour_serializers = OneHoursSerializers(data=data)
                        # if one_hour_serializers.is_valid():
                            # one_hour_serializers.save()
                        # else:
                            # return Response(five_min_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                    """insert the rotate data"""
                    # global before_data, flag_rotate
                    # # print("global data", before_data, len(before_data))
                    # ms_live_data = LiveData.objects.all()
                    # if len(ms_live_data) != len(before_data):
                        # for item in ms_live_data:
                            # if item in before_data:
                                # pass
                            # else:
                                # before_data.append(item)
                                # use_new = False
                                # print("items", item, item.data)
                                # if item.data > 15:
                                    # rotate_data = data
                                    # rotate_data['flag_on'] = 'on'
                                    # rotate_serializers = RotateSerializers(data=data)
                                    # if rotate_serializers.is_valid():
                                        # rotate_serializers.save()
                                    # else:
                                        # return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                # elif item.data <= 15:
                                    # rotate_data = data
                                    # rotate_data['flag_on'] = 'off'
                                    # rotate_serializers = RotateSerializers(data=data)
                                    # if rotate_serializers.is_valid():
                                        # rotate_serializers.save()
                                    # else:
                                        # return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # for item in before_data:
                        # # print("test fors",data['mac_addr'], item['mac_addr'])
                        # if data['mac_addr'] == item['mac_addr'] and str(data['pin']) == str(item['pin']) and str(
                                # data['position']) == str(item['position']) and str(data['type_data']) == str(
                            # item['type_data_id']):
                            # index_before_data = before_data.index(item)
                            # # print("item",item)
                            # search_flag = True
                            # break
                        # else:
                            # search_flag = False
                    # if search_flag and use_new:
                        # # print(flag_rotate, before_data[index_before_data]['data'] )
                        # if before_data[index_before_data]['data'] > 15 and data['data'] <= 15:
                            # before_data[index_before_data]['data'] = data['data']
                            # rotate_data = data
                            # rotate_data['flag_on'] = 'off'
                            # # print("roooooooooootate", rotate_data)
                            # rotate_serializers = RotateSerializers(data=data)
                            # if rotate_serializers.is_valid():
                                # rotate_serializers.save()
                            # else:
                                # return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        # elif before_data[index_before_data]['data'] <= 15 and data['data'] > 15:
                            # before_data[index_before_data]['data'] = data['data']
                            # rotate_data = data
                            # rotate_data['flag_on'] = 'on'
                            # # print("roooooooooootate", rotate_data)
                            # rotate_serializers = RotateSerializers(data=data)
                            # if rotate_serializers.is_valid():
                                # rotate_serializers.save()
                            # else:
                                # return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    # log_serializer = LogDataSerializer(data=data)
                    # if log_serializer.is_valid():
                        # log_serializer.save()
                        # # print(data, datetime.datetime.fromtimestamp(data['sendDataTime']))
                    # else:
                        # return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data created"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def offline_data(request):
    data_identify = False
    global offline_counter
    offline_counter = offline_counter + 1
    # print("offline_counter", offline_counter)
    # print("offline_data", request.data, len(request.data))
    if request.method == 'POST':
        if (len(request.data) == 0):
            return Response({"no data received"}, status=status.HTTP_400_BAD_REQUEST)
        # for i in range(0, len(request.data)):
        data = {}
        #print("check data", request.data[0]['Modbus'])
        data['mac_addr'] = request.data[0]['mac_addr']  # data['mac_addr'] = request.data[i]['mac_addr']
        if data['mac_addr'] == "ff:ff:ff:ff:ff:ff":
            return  # continue
        data['sendDataTime'] = datetime.datetime.fromtimestamp(
            request.data[0]['unixTime'])  # data['sendDataTime'] = request.data[i]['unixTime']
        for pin in request.data[0]['Modbus']:  # for pin in request.data[i]['Modbus']:
            #print("pin", request.data[0]['Modbus'])
            if pin['tag'] == 1:
                data['pin'] = pin['tag']
                data['data'] = pin['modbus_data']
                data['position'] = request.data[0]['Modbus'][9][ 'modbus_data']
                # data['position'] = request.data[i]['Modbus'][9]['modbus_data']
                data['type_data'] = 2
                diff = 0.0
                data['diff_data'] = diff
                data['updated_at'] = datetime.datetime.now()
                # print("timeeeeeeeees", data['updated_at'], data['sendDataTime'])
                """add script for data that use for report type of data """
                try:
                    delete_null = Rotation.objects.filter(mac_addr=data['mac_addr']).filter(pin=data['pin']).filter(
                        position=data['position']).filter(type_data_id=data['type_data']).order_by("sendDataTime").last()
                    if delete_null.flag_on is None:
                        # print(delete_null.sendDataTime)
                        if datetime.timedelta(minutes=float(20)) >= data['sendDataTime'].replace(tzinfo=utc) - delete_null.sendDataTime.replace(tzinfo=utc) > datetime.timedelta(minutes=float(1)):
                            Rotation.objects.filter(mac_addr=data['mac_addr']).filter(pin=data['pin']).filter(
                                position=data['position']).filter(type_data_id=data['type_data']).order_by("sendDataTime").last().delete()
                    log_offline = LastOffline.objects.filter(mac_addr=data['mac_addr']).filter(pin=data['pin']).filter(position=data['position']).filter(type_data=data['type_data'])
                    is_avalaible = False
                    if len(log_offline)>0:
                        is_avalaible =True
                    if not is_avalaible:
                        offline_serializer = LastOfflineSerializer(data=data)
                        if offline_serializer.is_valid():
                            offline_serializer.save()
                        else:
                            return Response(offline_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    print("timeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeees",datetime.datetime.now().minute)
                # if (datetime.datetime.now().minute) % 60 == 0:
                    # #print("yes offline counter 20", offline_counter)
                    # try:
                        # log_offline = LastOffline.objects.all()
                    # except LastOffline.DoesNotExist:
                        # offline_serializer = LastOfflineSerializer(data=data_set)
                        # if offline_serializer.is_valid():
                            # offline_serializer.save()
                        # else:
                            # return Response(offline_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    # log_offline = LastOffline.objects.filter(mac_addr=data['mac_addr'], pin=data['pin'], position=data['position'], type_data_id=data['type_data']).last()
                    # for item in log_offline:
                    # print("iteeem", data['mac_addr'], data['pin'], data['position'], data['type_data'], log_offline.sendDataTime)
                    # add_data_to_sub_table(data['mac_addr'], data['pin'], data['position'], data['type_data'], log_offline.sendDataTime)
                    # add_data_to_rotation_table(data['mac_addr'], data['pin'], data['position'], data['type_data'], log_offline.sendDataTime)
                    # last_data = LogData.objects.filter(mac_addr=data['mac_addr'], pin=data['pin'], position=data['position'], type_data_id=data['type_data']).order_by("sendDataTime").last()
                    # update_last_record_offline_table(last_data.mac_addr, last_data.pin, last_data.position, last_data.sendDataTime, last_data.type_data_id, last_data.data)
                    # print("Yesyes yes yes yes yes")
                    # time.sleep(10)
                    # offline_counter = 0
                except:
                    Response(traceback.print_exc(), status=status.HTTP_406_NOT_ACCEPTABLE)

                log_serializer = LogDataSerializer(data=data)
                if log_serializer.is_valid():
                    log_serializer.save()

                else:
                    return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data created"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def test(request):
    print("test_data", request.data, len(request.data))
    if request.method == 'POST':
        if (len(request.data) == 0):
            return Response({"no data received"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            global ResultSheet_NumberOfRowsEntered
            ResultSheet_NumberOfRowsEntered = ResultSheet_NumberOfRowsEntered + 1
            ResultSheet.write(ResultSheet_NumberOfRowsEntered, 0, str(request.data))
            for item in request.data:
                text = {}
                text['text'] = str(item)
                data_serializer = DataSerializer(data=text)
                if data_serializer.is_valid():
                    data_serializer.save()

                    return Response({"data received"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logsInPeriod(request):
    if request.method == 'POST':
        if ('start_time' in request.data) and ('end_time' in request.data) and ('dur_time' in request.data):
            if (request.data['start_time'] and request.data['end_time'] and request.data['dur_time']):
                response = []
                time = parse_datetime(request.data['start_time'])
                time2 = parse_datetime(request.data['end_time'])

                try:
                    # logs_in_shift = (LogData.objects
                    #                     .values('mac_addr','pin', 'sendDataTime')
                    #                     .annotate(sum_of_diff = Sum('diff_data'))
                    #                     )
                    # response.append((logs_in_shift))

                    ####

                    while time < time2:
                        temp_time = time + datetime.timedelta(minutes=float(request.data['dur_time']))
                        # print(LogData.objects.values('mac_addr','pin'))

                        logs_in_period = (LogData.objects
                                          .values('mac_addr', 'pin', 'sendDataTime')
                                          .filter(sendDataTime__range=(time, temp_time))
                                          .annotate(sum_of_diff=Sum('diff_data'))
                                          )

                        time = temp_time
                        if len(logs_in_period) > 0:
                            response.append((logs_in_period))
                        # if logs_in_shift :
                        #     response.append((logs_in_shift))
                    ####

                    # logs_in_shift = (LogData.objects.filter(sendDataTime__range = (time, time2))
                    #                     .extra(select={'sendDataTime_slice': "FLOOR (EXTRACT (EPOCH FROM sendDataTime) / '900' )"})
                    #                     .values('mac_addr','pin', 'sendDataTime_slice')
                    #                     .annotate(sum_of_diff = Sum('diff_data'))
                    #                     )
                    # response.append((logs_in_shift))

                    ####

                    return Response((response), status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_charges_in_time_range_as_date_status(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        if ('mac_addr' in data) and ('pin' in data) and ('position' in data) and \
            ('type_data' in data) and ('charge_start_time' in data) and \
                ('charge_end_time' in data) and ('complete_status' in data):
            if data['mac_addr'] and data['pin'] and data['position'] and data['type_data'] \
               and data['charge_start_time'] and data['charge_end_time'] and data['complete_status']:
                mac_addr = data.get('mac_addr')
                pin = data.get('pin')
                position = data.get('position')
                type_data = data.get('type_data')
                start_time = data.get('charge_start_time')
                end_time = data.get('charge_end_time')
                complete_status = data.get('complete_status')
                try:
                    charges = ChargeCounts.objects.filter(Q(mac_addr=mac_addr, pin=pin, position=position,
                                                            type_data=type_data,
                                                            charge_start_time__range=(start_time, end_time),
                                                            charge_end_time__range=(start_time, end_time)) |
                                                          Q(mac_addr=mac_addr, pin=pin, position=position,
                                                            type_data=type_data,
                                                            charge_start_time__gte=start_time,
                                                            charge_start_time__lt=end_time,
                                                            charge_end_time__gte=end_time,
                                                            ) |
                                                          Q(mac_addr=mac_addr, pin=pin, position=position,
                                                            type_data=type_data,
                                                            charge_start_time__lt=start_time,
                                                            charge_end_time__gt=start_time,
                                                            charge_end_time__lt=end_time)).order_by('charge_start_time')

                    if complete_status == '2':
                        charges = charges
                    elif complete_status == '1':
                        charges = charges.filter(complete_status=False)
                    elif complete_status == '0':
                        charges = charges.filter(complete_status=True)
                    else:
                        return Response({'msg': 'invalid data', 'status': status.HTTP_400_BAD_REQUEST})

                    serializer = ChargeCountsSerializers(charges, many=True)
                    print(serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except ChargeCounts.DoesNotExist:
                    return Response({'msg': 'result not found', 'status_code': status.HTTP_404_NOT_FOUND})
            return Response({'msg': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Missing required fields in request data'}, status=status.HTTP_400_BAD_REQUEST)