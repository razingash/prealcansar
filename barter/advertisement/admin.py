from django.contrib import admin

from .models import Campaing, Advertisement, ViewStatistic, ClickStatistic

# Register your models here.

admin.site.register(Campaing)
admin.site.register(Advertisement)
admin.site.register(ViewStatistic)
admin.site.register(ClickStatistic)
