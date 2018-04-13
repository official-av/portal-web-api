from django.contrib import admin
from .models import Account,Department,PortalQuestion,PortalRecommendation

admin.site.register(Account)
admin.site.register(Department)
admin.site.register(PortalQuestion)
admin.site.register(PortalRecommendation)
# Register your models here.
