import datetime
from .models import LiveData

cupSize = 20000
inf = 300000
timeCheck = datetime.timedelta(minutes=120)
offline_counter = 0
# log_offline = []
counter_flow = 0
flag_rotate = False
live_data = LiveData.objects.all().values('id', 'mac_addr', 'data', 'pin', 'sendDataTime', 'type_data_id', 'position')
before_data = []
for item in live_data:
    before_data.append(item)
    #rint(before_data[0])
