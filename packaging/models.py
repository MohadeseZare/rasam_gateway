from django.db import models


class PackagingLlogData(models.Model):
    id = models.BigAutoField(primary_key=True)
    mac_addr = models.CharField(max_length=50)
    datatime = models.BigIntegerField()
    degree1 = models.IntegerField()
    degree2 = models.IntegerField()
    degree3 = models.IntegerField()
    degree4 = models.IntegerField()
    degree5 = models.IntegerField()
    degree6 = models.IntegerField()


class PackagingLiveData(models.Model):
    id = models.BigAutoField(primary_key=True)
    mac_addr = models.CharField(max_length=50)
    datatime = models.BigIntegerField()
    degree1 = models.IntegerField()
    # time1 = models.DateTimeField()
    degree2 = models.IntegerField()
    # time2 = models.DateTimeField()
    degree3 = models.IntegerField()
    # time3 = models.DateTimeField()
    degree4 = models.IntegerField()
    # time4 = models.DateTimeField()
    degree5 = models.IntegerField()
    # time5 = models.DateTimeField()
    degree6 = models.IntegerField()
    # time6 = models.DateTimeField()


class TypeOfAlarm(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=10)
    section = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code


class Alarm(models.Model):
    id = models.BigAutoField(primary_key=True)
    alarm_row = models.CharField(max_length=10)
    mac_addr = models.CharField(max_length=50)
    start_time = models.BigIntegerField()
    end_time = models.BigIntegerField(null=True)
    type_of_alarm = models.ForeignKey(to=TypeOfAlarm, on_delete=models.CASCADE)

class StoppageTime(models.Model):
    id = models.BigAutoField(primary_key=True)
    mac_addr = models.CharField(max_length=50)
    dur_start = models.BigIntegerField()
    dur_end = models.BigIntegerField()
    dur_stoppage = models.BigIntegerField()
    section = models.CharField(max_length=50)

class AggregateData(models.Model):
    id = models.BigAutoField(primary_key=True)
    mac_addr = models.CharField(max_length=50)
    datatime = models.BigIntegerField()
    degree1 = models.IntegerField(default=0)
    degree2 = models.IntegerField(default=0)
    degree3 = models.IntegerField(default=0)
    degree4 = models.IntegerField(default=0)
    degree5 = models.IntegerField(default=0)
    degree6 = models.IntegerField(default=0)
