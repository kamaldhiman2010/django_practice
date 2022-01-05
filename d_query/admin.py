from django.contrib import admin
from .models import Post,NewsPaper,Comments,MultipleUsers,Payment
from django.contrib.auth.models import User
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','subject')

admin.site.register(Post,PostAdmin)
admin.site.register(NewsPaper)
admin.site.register(Comments)
admin.site.register(MultipleUsers)
admin.site.register(Payment)

