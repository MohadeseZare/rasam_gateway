import traceback
import psycopg2
import requests
import datetime
from rest_framework.response import Response
from .models import LastOffline, LogData
from rest_framework import status
from .serializers import LastOfflineSerializer
import pytz
utc = pytz.UTC
import time

def add_data_to_sub_table(mac_addr, pin, position, type_data_id, start_time):
    conn = psycopg2.connect(database="gateway", user='gatewayuser', password='gateway123', host='localhost', port='')
    cursor = conn.cursor()
    # sql = '''SELECT * FROM logs_logdata where mac_addr=%s and pin=%s and position = %s and type_data_id= %s and "sendDataTime">= %s order by "sendDataTime";'''
    # params = (mac_addr, pin, position, type_data_id, start_time)
    # logs_data = cursor.execute(sql, params)  
    logs_data = LogData.objects.filter(mac_addr=mac_addr).filter(pin=pin).filter(position=position).filter(type_data=type_data_id).filter(sendDataTime__gte=start_time)
    print("logs return data:", logs_data)
    first_time = str(logs_data[0].sendDataTime).split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    print("fffffffff", first_time1)
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%d %H:%M:%S")
    print("frst2", first_time2)
    next_time = first_time2 + datetime.timedelta(minutes=1)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = item.sendDataTime
        if first_time2.replace(tzinfo=utc) < next_time.replace(tzinfo=utc) and flag_write:
            query_temp = """insert into logs_oneminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac_addr, pin, position, type_data_id, before_item.data, before_item.sendDataTime, before_item.sendDataTime)
            cursor.execute(query_temp, query_param)
            first_time2 = item.sendDataTime
            flag_write = False
        if first_time2.replace(tzinfo=utc) >= next_time.replace(tzinfo=utc):
            next_time = next_time + datetime.timedelta(minutes=1)
            flag_write = True
        before_item = item
    print("one_min_flow complete")
    first_time = str(logs_data[0].sendDataTime).split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%d %H:%M:%S")
    print("frst2", first_time2)
    next_time = first_time2 + datetime.timedelta(minutes=5)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = item.sendDataTime
        if first_time2.replace(tzinfo=utc) < next_time.replace(tzinfo=utc) and flag_write:
            query_temp = """insert into logs_fiveminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac_addr, pin, position, type_data_id, before_item.data, before_item.sendDataTime, before_item.sendDataTime)
            cursor.execute(query_temp, query_param)
            first_time2 = item.sendDataTime
            flag_write = False
        if first_time2.replace(tzinfo=utc) >= next_time.replace(tzinfo=utc):
            next_time = next_time + datetime.timedelta(minutes=5)
            flag_write = True
        before_item = item
    print("five_min_flow complete")
    first_time = str(logs_data[0].sendDataTime).split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%d %H:%M:%S")
    next_time = first_time2 + datetime.timedelta(minutes=15)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = item.sendDataTime
        if first_time2.replace(tzinfo=utc) < next_time.replace(tzinfo=utc) and flag_write:
            query_temp = """insert into logs_fifteenminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac_addr, pin, position, type_data_id, before_item.data, before_item.sendDataTime,
                           before_item.sendDataTime)
            cursor.execute(query_temp, query_param)
            first_time2 = item.sendDataTime
            flag_write = False
        if first_time2.replace(tzinfo=utc) >= next_time.replace(tzinfo=utc):
            next_time = next_time + datetime.timedelta(minutes=15)
            flag_write = True
        before_item = item
    print("fifteen_min_flow complete")
    first_time = str(logs_data[0].sendDataTime).split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%d %H:%M:%S")
    next_time = first_time2 + datetime.timedelta(minutes=30)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = item.sendDataTime
        if first_time2.replace(tzinfo=utc) < next_time.replace(tzinfo=utc) and flag_write:
            query_temp = """insert into logs_thirtyminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac_addr, pin, position, type_data_id, before_item.data, before_item.sendDataTime,
                           before_item.sendDataTime)
            cursor.execute(query_temp, query_param)
            first_time2 = item.sendDataTime
            flag_write = False
        if first_time2.replace(tzinfo=utc) >= next_time.replace(tzinfo=utc):
            next_time = next_time + datetime.timedelta(minutes=30)
            flag_write = True
        before_item = item
    print("thirty_min_flow complete")
    first_time = str(logs_data[0].sendDataTime).split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%d %H:%M:%S")
    next_time = first_time2 + datetime.timedelta(minutes=60)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = item.sendDataTime
        if first_time2.replace(tzinfo=utc) < next_time.replace(tzinfo=utc) and flag_write:
            query_temp = """insert into logs_onehourflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac_addr, pin, position, type_data_id, before_item.data, before_item.sendDataTime,
                           before_item.sendDataTime)
            cursor.execute(query_temp, query_param)
            first_time2 = item.sendDataTime
            flag_write = False
        if first_time2.replace(tzinfo=utc) >= next_time.replace(tzinfo=utc):
            next_time = next_time + datetime.timedelta(minutes=60)
            flag_write = True
        before_item = item
    print("one_hour_flow complete")
    conn.commit()
    cursor.close()
    conn.close()
    time.sleep(3)


def add_data_to_rotation_table(mac_addr, pin, position, type_data_id, start_time):
    conn = psycopg2.connect(database="gateway", user='gatewayuser', password='gateway123', host='localhost', port='')
    cursor = conn.cursor()
    # sql = '''SELECT * FROM logs_logdata where mac_addr=%s and pin=%s and position = %s and type_data_id= %s and "sendDataTime">= %s order by "sendDataTime";'''
    # params = (mac_addr, pin, position, type_data_id, start_time)
    # logs_data = cursor.execute(sql, params)
    logs_data = LogData.objects.filter(mac_addr=mac_addr).filter(pin=pin).filter(position=position).filter(
        type_data=type_data_id).filter(sendDataTime__gte=start_time)
    print("logs return data:", logs_data)
    first_item = True
    LastCurrent = logs_data[0].data
    for item in logs_data:
        if first_item:
            first_item = False
            continue
        Current = item.data

        if (LastCurrent <= 15 or Current <= 15) and not (LastCurrent <= 15 and Current <= 15):

            if LastCurrent <= 15:
                query_temp = """insert into logs_rotation  (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at, flag_on) values (%s, %s, %s, %s, %s,%s, 0.0, %s, %s); """
                query_param = (
                    mac_addr, pin, position, type_data_id, item.data, item.sendDataTime, item.sendDataTime,
                    "on")
                cursor.execute(query_temp, query_param)
            if LastCurrent > 15:
                query_temp = """insert into logs_rotation  (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at, flag_on) values (%s, %s, %s, %s, %s,%s, 0.0, %s, %s); """
                query_param = (
                    mac_addr, pin, position, type_data_id, item.data, item.sendDataTime, item.sendDataTime,
                    "off")
                cursor.execute(query_temp, query_param)
        LastCurrent = Current
    conn.commit()
    cursor.close()
    conn.close()
    time.sleep(3)


def update_last_record_offline_table(mac_addr, pin, position, sendDataTime, type_data, data):
    data_set = {'mac_addr': mac_addr, 'pin': pin, 'position': position, 'type_data': type_data,
                'sendDataTime': sendDataTime, 'updated_at': datetime.datetime.now(), 'data': data}
    try:
        last_offline = LastOffline.objects.get(mac_addr=mac_addr, pin=pin, position=position, type_data=type_data)
        try:
            LastOffline.objects.filter(mac_addr=mac_addr, pin=pin, type_data=type_data, position=position) \
                .update(data=data, updated_at=datetime.datetime.now().replace(tzinfo=None),
                        sendDataTime=sendDataTime.replace(tzinfo=None))

        except:
            return Response(traceback.print_exc(), status=status.HTTP_400_BAD_REQUEST)

    except LastOffline.DoesNotExist:
        live_serializer = LastOfflineSerializer(data=data_set)
        if live_serializer.is_valid():
            live_serializer.save()
        else:
            return Response(live_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    pass
