from django.db.models import fields
from rest_framework import serializers
from .models import  LogData, LiveData, OneHourFlow, ThirtyMinFlow, FifteenMinFlow, FiveMinFlow, OneMinFlow, Rotation, \
    Data, LastOffline, ChargeCounts



class LogDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = LogData
        fields = '__all__'

class LiveDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = LiveData
        fields = '__all__'

# class BoardPropertySerializer (serializers.ModelSerializer):
    # class Meta:
        # model = BoardProperty
        # fields = '__all__'


class OneHoursSerializers(serializers.ModelSerializer):
    class Meta:
        model = OneHourFlow
        fields = '__all__'


class ThirtyMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = ThirtyMinFlow
        fields = '__all__'
        
        
class FifteenMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = FifteenMinFlow
        fields = '__all__'
        
        
class FiveMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = FiveMinFlow
        fields = '__all__'


class OneMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = OneMinFlow
        fields = '__all__'
        
class RotateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rotation
        fields = '__all__'
        
class DataSerializer (serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'
        

class LastOfflineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastOffline
        fields = '__all__'


class ChargeCountsSerializers(serializers.ModelSerializer):
    time_difference = serializers.SerializerMethodField()

    def get_time_difference(self, obj):
        time_diff = obj.charge_end_time - obj.charge_start_time
        return time_diff

    class Meta:
        model = ChargeCounts
        exclude = ['id', 'mac_addr', 'pin', 'position', 'type_data']
