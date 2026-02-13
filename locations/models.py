from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse


class SportsFieldLocation(models.Model):
    FIELD_TYPES = [
        ('football', 'Football'),  # كرة القدم
        ('basketball', 'Basketball'),  # كرة السلة
        ('volleyball', 'Volleyball'),  # كرة الطائرة
        ('tennis', 'Tennis'),  # التنس
    ]

    name = models.CharField(max_length=100, verbose_name="Field Name")
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPES,
        verbose_name="Field Type",
    )
    latitude = models.FloatField(verbose_name="Latitude")  # خط العرض
    longitude = models.FloatField(verbose_name="Longitude")  # خط الطول
    address = models.TextField(verbose_name="Address")  # العنوان
    image = models.ImageField(upload_to='field_images/', blank=True, null=True,
                              verbose_name="Field Image")
    favorites = models.ManyToManyField(
        User, related_name='favorite_sports_fields', blank=True)

    description = models.TextField(blank=True, null=True,
                                   verbose_name="Description")
    average_rating = models.FloatField(
        default=0.0, verbose_name="Average Rating")
    requires_payment = models.BooleanField(
        default=False,
        verbose_name="Requires Payment",
        help_text="Check if this field requires payment to use."
    )  # هل يتطلب الدفع؟
    price_per_hour = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Price Per Hour",
        help_text="Specify the hourly price if the field requires payment."
    )  # السعر لكل ساعة
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")  # تاريخ الإنشاء
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated At")  # تاريخ التحديث

    def get_absolute_url(self):
        """إرجاع الرابط الخاص بالملعب."""
        return reverse('field_detail', args=[str(self.id)])

    def get_share_link(self):
        """إرجاع رابط المشاركة الخاص بالملعب."""
        return f"https://wa.me/?text=شاهد%20هذا%20الملعب:%20{self.name}%20-https://yourdomain.com{self.get_absolute_url()}"# noqa

    class Meta:
        verbose_name = "Sports Field Location"
        verbose_name_plural = "Sports Field Locations"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()})"


class Rating(models.Model):
    field = models.ForeignKey(
        SportsFieldLocation, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # تقييم من 1 إلى 5

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return f"{self.field.name} - {self.rating}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(
        SportsFieldLocation,
        on_delete=models.CASCADE, related_name="favorite_entries")

    class Meta:
        unique_together = ('user', 'field')
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user.username} - {self.field.name}"


class Booking(models.Model):
    field = models.ForeignKey(
        'SportsFieldLocation', on_delete=models.CASCADE,
        verbose_name="Sports Field")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User")
    date = models.DateField(verbose_name="Booking Date")
    time = models.TimeField(verbose_name="Start Time")
    duration = models.IntegerField(verbose_name="Duration (hours)")

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-date", "time"]

    def __str__(self):
        return f"{self.field.name} - {
            self.date} {self.time} ({self.duration} hours)"

    def end_time(self):
        """
        تحسب وقت انتهاء الحجز بناءً على وقت البداية والمدة.
        """
        start_datetime = datetime.combine(self.date, self.time)
        end_datetime = start_datetime + timedelta(hours=self.duration)
        return end_datetime.time()

    def overlaps_with(self, other_booking):
        """
        تتحقق من التداخل بين هذا الحجز وحجز آخر.
        """
        if self.date != other_booking.date:
            return False  # لا يوجد تداخل إذا لم يكن التاريخان متطابقين

        self_start = datetime.combine(self.date, self.time)
        self_end = self_start + timedelta(hours=self.duration)

        other_start = datetime.combine(other_booking.date, other_booking.time)
        other_end = other_start + timedelta(hours=other_booking.duration)

        return self_start < other_end and self_end > other_start