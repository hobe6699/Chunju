from django.contrib import admin
from webcore.models.organization import *

# Register your models here.
admin.site.register(OrgGroup)
admin.site.register(OrgInfo)
admin.site.register(OrgDept)
admin.site.register(OrgPosition)
admin.site.register(OrgEmp)

