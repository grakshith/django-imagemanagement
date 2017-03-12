from django.contrib import admin
from .models import Image,AccessKey
# Register your models here.

admin.site.register(Image)

class AccessKeyAdmin(admin.ModelAdmin):
	readonly_fields = ('accessKey',)
	
admin.site.register(AccessKey,AccessKeyAdmin)
