from django.db import models
from django.utils.timezone import now


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(default=now)  # تعيين التاريخ الافتراضي
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events_images/',
                              null=True, blank=True)

    def __str__(self):
        return self.title
