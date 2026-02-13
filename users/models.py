from django.db import models
from django.contrib.auth.models import User


class HelpRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="help_requests")  # ربط المستخدم
    message = models.TextField(verbose_name="Message")
    reply = models.TextField(verbose_name="Reply", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.username} at {self.created_at}"
