from django.contrib import admin
from .models import HelpRequest


class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'reply',
                    'created_at')  # الحقول الصحيحة من نموذج HelpRequest
    search_fields = ('user__username', 'user__email', 'message')  # للبحث
    list_filter = ('created_at',)  # لتصفية الطلبات حسب التاريخ


admin.site.register(HelpRequest, HelpRequestAdmin)

# Register your models here.
