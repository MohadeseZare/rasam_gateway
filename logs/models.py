from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


class TypeData(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120)
    type_data = models.IntegerField()

    def __str__(self):
        return str(self.type_data)


class Pin(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    tag = models.IntegerField()

    def __str__(self):
        return str(self.tag)

class LogData(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mac_addr}, {self.data}, {self.diff_data}'

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class LiveData(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(auto_now_add=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    # counter = models.IntegerField()
    # board = models.ForeignKey(BoardProperty, on_delete=CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mac_addr}, {self.data}, {self.diff_data}'


class OneHourFlow(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class ThirtyMinFlow(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class FifteenMinFlow(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class FiveMinFlow(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class OneMinFlow(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class Rotation(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    flag_on = models.CharField(max_length=5, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class Data(models.Model):
    text = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now_add=True)


class OneHourTest(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.BigIntegerField(db_index=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    diff_data = models.FloatField(default=0)
    updated_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['sendDataTime']),
        ]


class LastOffline(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    sendDataTime = models.DateTimeField(auto_now_add=True)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    data = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ChargeCounts(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, default=1)
    position = models.CharField(max_length=10, null=True, default=None)
    type_data = models.ForeignKey(TypeData, on_delete=models.CASCADE, null=True, blank=True)
    charge_start_time = models.DateTimeField()
    charge_end_time = models.DateTimeField()
    incomplete_end = models.BooleanField(default=False, db_index=True)
    complete_status = models.BooleanField(db_index=True)
    stop_between_charge = models.IntegerField(db_index=True)

    def __str__(self):
        return f"{self.mac_addr} // complete_status: " f"{self.complete_status} // " \
               f"incomplete_end: {self.incomplete_end} "

    class Meta:
        verbose_name = 'ChargeCount'
        verbose_name_plural = 'ChargeCounts'