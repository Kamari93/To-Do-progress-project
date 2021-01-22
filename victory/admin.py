from django.contrib import admin
from .models import Victory

class VictoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Victory, VictoryAdmin)


