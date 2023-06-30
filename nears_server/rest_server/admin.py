from django.contrib import admin
from .models import UserAuth, User, Staff, Device, Department, Cases, CallLogs, Messages, Modes, Types

admin.site.register(UserAuth)
admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Device)
admin.site.register(Department)
admin.site.register(Cases)
admin.site.register(CallLogs)
admin.site.register(Messages)
admin.site.register(Modes)
admin.site.register(Types)