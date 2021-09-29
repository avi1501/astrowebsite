from django.contrib import admin

# Register your models here.
from . import models

from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
import pprint

class OrderAdmin(admin.ModelAdmin):
    list_display = ("name","email","order_id","payment_status")
    def has_add_permission(self, request, object=None):
        return False
    def has_change_permission(self, request, object=None):
        return False
    def has_delete_permission(self, request, object=None):
        return False

class ContactAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, object=None):
        return False

class AboutAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, object=None):
        return False
    
    def has_add_permission(self, request, object=None):
        a = models.About.objects.first()
        print(a)
        if a == None:
            return True
        return False

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title' , 'image_tag')

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace("\n","<br>\n")
    _session_data.allow_tags=True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['session_data']




admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(models.VedicAstrology)
admin.site.register(models.Vastu)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.About, AboutAdmin)
admin.site.register(models.Banner)

admin.site.register(Session, SessionAdmin)

admin.site.register(models.Order, OrderAdmin)
