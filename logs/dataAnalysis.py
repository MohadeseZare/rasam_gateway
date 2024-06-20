import psycopg2
import requests
import datetime


def add_data_to_sub_table(mac, pin, position, type_data_id, start_time, end_time):
    URL = "http://localhost:7000/gatewaya/gateway/api/getLogs/inPeriod/data/"
    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "mac_address": mac,
        "pin": pin,
        "position": position,
        "type_data": type_data_id,
        "report_id": "1"
    }
    logs_datas = requests.post(url=URL, data=BODY)
    print("logs return data:", logs_datas)
    logs_data = logs_datas.json()
    if len(logs_data) == 0:
        return
    first_time = logs_data[0]["sendDataTime"].split(":")
    first_time[2] = "00"
    first_time1 = first_time[0]+":"+first_time[1]+":"+first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")
    print("frst2", first_time2)
    next_time = first_time2+datetime.timedelta(minutes=1)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    conn = psycopg2.connect(database="gateway", user='gatewayuser', password='gateway123', host='localhost', port='')
    cursor = conn.cursor()
    for item in logs_data:
        first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        #print(type(first_time2), type(datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")), type(next_time))
        if first_time2 < next_time and flag_write:
            query_temp = """insert into logs_oneminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac, pin, position, type_data_id, before_item['data'], before_item['sendDataTime'], before_item['sendDataTime'])
            cursor.execute(query_temp, query_param)
            first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            flag_write = False
        if first_time2 >= next_time:
            next_time = next_time + datetime.timedelta(minutes=1)
            flag_write = True
        before_item = item
    print("one_min_flow complete")
    first_time = logs_data[0]["sendDataTime"].split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")
    print("frst2",first_time2)
    next_time = first_time2+datetime.timedelta(minutes=5)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        #print(type(first_time2), type(datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")), type(next_time))
        if first_time2 < next_time and flag_write:
            query_temp = """insert into logs_fiveminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac, pin, position, type_data_id, before_item['data'], before_item['sendDataTime'], before_item['sendDataTime'])
            cursor.execute(query_temp, query_param)
            first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            flag_write = False
        if first_time2 >= next_time:
            next_time = next_time + datetime.timedelta(minutes=5)
            flag_write = True
        before_item = item
    print("five_min_flow complete")
    first_time = logs_data[0]["sendDataTime"].split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")
    next_time = first_time2 + datetime.timedelta(minutes=15)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # print(type(first_time2), type(datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")), type(next_time))
        if first_time2 < next_time and flag_write:
            query_temp = """insert into logs_fifteenminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac, pin, position, type_data_id, before_item['data'], before_item['sendDataTime'], before_item['sendDataTime'])
            cursor.execute(query_temp, query_param)
            first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            flag_write = False
        if first_time2 >= next_time:
            next_time = next_time + datetime.timedelta(minutes=15)
            flag_write = True
        before_item = item
    print("fifteen_min_flow complete")
    first_time = logs_data[0]["sendDataTime"].split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")
    next_time = first_time2 + datetime.timedelta(minutes=30)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # print(type(first_time2), type(datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")), type(next_time))
        if first_time2 < next_time and flag_write:
            query_temp = """insert into logs_thirtyminflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac, pin, position, type_data_id, before_item['data'], before_item['sendDataTime'], before_item['sendDataTime'])
            cursor.execute(query_temp, query_param)
            first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            flag_write = False
        if first_time2 >= next_time:
            next_time = next_time + datetime.timedelta(minutes=30)
            flag_write = True
        before_item = item
    print("thirty_min_flow complete")
    first_time = logs_data[0]["sendDataTime"].split(":")
    first_time[2] = "00"
    first_time1 = first_time[0] + ":" + first_time[1] + ":" + first_time[2]
    first_time2 = datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")
    next_time = first_time2 + datetime.timedelta(minutes=60)
    flag_write = True
    before_item = logs_data[0]
    print(before_item)
    for item in logs_data:
        first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        # print(type(first_time2), type(datetime.datetime.strptime(first_time1, "%Y-%m-%dT%H:%M:%S")), type(next_time))
        if first_time2 < next_time and flag_write:
            query_temp = """insert into logs_onehourflow (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at) values (%s, %s, %s, %s, %s,%s, 0.0, %s); """
            query_param = (mac, pin, position, type_data_id, before_item['data'], before_item['sendDataTime'], before_item['sendDataTime'])
            cursor.execute(query_temp, query_param)
            first_time2 = datetime.datetime.strptime(item['sendDataTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            flag_write = False
        if first_time2 >= next_time:
            next_time = next_time + datetime.timedelta(minutes=60)
            flag_write = True
        before_item = item
    print("one_hour_flow complete")
    conn.commit()
    cursor.close()
    conn.close()



def add_data_to_rotation_table(mac, pin, position, type_data_id, start_time, end_time):
    URL = "http://localhost:7000/gatewaya/gateway/api/getLogs/inPeriod/data/"
    BODY = {
        "start_time": start_time,
        "end_time": end_time,
        "mac_address": mac,
        "pin": pin,
        "position": position,
        "type_data": type_data_id,
        "report_id": "1"
    }
    logs_datas = requests.post(url=URL, data=BODY)
    print("logs return data:", logs_datas)
    logs_data = logs_datas.json()
    first_item = True
    LastCurrent = logs_data[0]['data']
    conn = psycopg2.connect(database="gateway", user='gatewayuser', password='gateway123', host='localhost', port='')
    cursor = conn.cursor()
    for item in logs_data:
        if first_item:
            first_item = False
            continue
        Current = item['data']

        if (LastCurrent == 0 or Current == 0) and not(LastCurrent == 0 and Current == 0):

            if LastCurrent == 0:
                query_temp = """insert into logs_rotation  (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at, flag_on) values (%s, %s, %s, %s, %s,%s, 0.0, %s, %s); """
                query_param = (mac, pin, position, type_data_id, item['data'], item['sendDataTime'], item['sendDataTime'], "on")
                cursor.execute(query_temp, query_param)
            if LastCurrent != 0:
                query_temp = """insert into logs_rotation  (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at, flag_on) values (%s, %s, %s, %s, %s,%s, 0.0, %s, %s); """
                query_param = (mac, pin, position, type_data_id, item['data'], item['sendDataTime'], item['sendDataTime'], "off")
                cursor.execute(query_temp, query_param)
        LastCurrent = Current
    conn.commit()
    cursor.close()
    conn.close()

