from django.contrib import admin
from .models import Account,Department,AuthViewer,PortalQuestion

admin.site.register(Account)
admin.site.register(Department)
admin.site.register(PortalQuestion)
admin.site.register(AuthViewer)


# Register your models here.
