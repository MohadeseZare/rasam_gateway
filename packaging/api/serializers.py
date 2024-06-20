from django.db.models import fields
from rest_framework import serializers
from packaging.models import PackagingLlogData, PackagingLiveData, TypeOfAlarm, Alarm, AggregateData,  StoppageTime


class PackagingLlogDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingLlogData
        fields = '__all__'


class PackagingLiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagingLiveData
        fields = '__all__'


class TypeOfAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfAlarm
        fields = '__all__'


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'


class StoppageTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoppageTime
        fields = '__all__'

class AggregateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AggregateData
        fields = '__all__'
