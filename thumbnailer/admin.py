from django.contrib import admin
from .models import AllUser,Children,Adult,Aged
# Register your models here.
admin.site.register(AllUser)
admin.site.register(Children)
admin.site.register(Adult)
admin.site.register(Aged)