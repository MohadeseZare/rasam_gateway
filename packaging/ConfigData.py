from packaging.models import *

global list_of_alarm
list_of_alarm = TypeOfAlarm.objects.all()
print(list_of_alarm)
