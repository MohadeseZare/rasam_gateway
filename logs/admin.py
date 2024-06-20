from django.contrib import admin
from .models import LogData, LiveData, TypeData,  OneHourFlow, ThirtyMinFlow, FifteenMinFlow, FiveMinFlow, OneMinFlow, \
    Rotation, LastOffline, ChargeCounts, Pin

# Register your models here.
# admin.site.register(BoardProperty)
admin.site.register(TypeData)
admin.site.register(LogData)
admin.site.register(LiveData)
admin.site.register(OneHourFlow)
admin.site.register(ThirtyMinFlow)
admin.site.register(FifteenMinFlow)
admin.site.register(FiveMinFlow)
admin.site.register(OneMinFlow)
admin.site.register(Rotation)
admin.site.register(LastOffline)
admin.site.register(ChargeCounts)
admin.site.register(Pin)
