import psycopg2
from datetime import datetime, timedelta
import requests

def add_data_to_rotation_table(mac, pin, position, type_data_id, start_time, end_time):
    
    try:
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
            if (LastCurrent <= 15 or Current <= 15) and not(LastCurrent <= 15 and Current <= 15):

                if LastCurrent <= 15:
                    query_temp = """insert into logs_rotation  (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at, flag_on) values (%s, %s, %s, %s, %s,%s, 0.0, %s, %s); """
                    query_param = (mac, pin, position, type_data_id, item['data'], item['sendDataTime'], item['sendDataTime'], "on")
                    cursor.execute(query_temp, query_param)
                if LastCurrent > 15:
                    query_temp = """insert into logs_rotation  (mac_addr, pin, position, type_data_id, data, "sendDataTime", diff_data, updated_at, flag_on) values (%s, %s, %s, %s, %s,%s, 0.0, %s, %s); """
                    query_param = (mac, pin, position, type_data_id, item['data'], item['sendDataTime'], item['sendDataTime'], "off")
                    cursor.execute(query_temp, query_param)

            LastCurrent = Current
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as error:
        print(error)
        pass


add_data_to_rotation_table(mac="ST:CH:01:01", pin="1", position="1", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("چمفر یک")
add_data_to_rotation_table(mac="ST:CH:01:01", pin="1", position="2", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("چمفر دو")
add_data_to_rotation_table(mac="ST:CH:01:01", pin="1", position="3", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("چمفر سه")
add_data_to_rotation_table(mac="ST:CH:01:01", pin="1", position="4", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("چمفر چهار")
add_data_to_rotation_table(mac="ST:CH:01:01", pin="1", position="0", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("چمفر ورودی")
add_data_to_rotation_table(mac="ST:PB:02:01", pin="1", position="1", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("1")
add_data_to_rotation_table(mac="ST:PB:02:01", pin="1", position="2", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("2")
add_data_to_rotation_table(mac="ST:PB:02:01", pin="1", position="3", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("3")
add_data_to_rotation_table(mac="ST:PB:02:01", pin="1", position="4", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("4")
add_data_to_rotation_table(mac="ST:PB:02:01", pin="1", position="5", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("5")
add_data_to_rotation_table(mac="ST:PB:01:02", pin="1", position="1", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("6")
add_data_to_rotation_table(mac="ST:PB:01:02", pin="1", position="2", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("7")
add_data_to_rotation_table(mac="ST:PB:01:01", pin="1", position="1", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("8")
add_data_to_rotation_table(mac="ST:PB:01:01", pin="1", position="2", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("9")
print("shams")
add_data_to_rotation_table(mac="SH:PB:01:01", pin="1", position="1", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("1")
add_data_to_rotation_table(mac="SH:PB:01:01", pin="1", position="2", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("2")
add_data_to_rotation_table(mac="SH:PB:01:01", pin="1", position="3", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("3")
add_data_to_rotation_table(mac="SH:PB:01:01", pin="1", position="4", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("4")
add_data_to_rotation_table(mac="SH:PB:01:01", pin="1", position="5", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("5")
add_data_to_rotation_table(mac="SH:PB:01:01", pin="1", position="6", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("6")
add_data_to_rotation_table(mac="SH:PB:02:01", pin="1", position="1", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("7")
add_data_to_rotation_table(mac="SH:PB:02:01", pin="1", position="2", type_data_id="2", start_time="2024-03-16T00:00:00", end_time="2024-03-17T23:59:00")
print("8")

print("successfully!!!")

