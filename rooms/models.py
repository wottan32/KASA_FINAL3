from django.utils import timezone
from django.db import models
from django.urls import reverse
from core import models as core_models
from django_countries.fields import CountryField
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):
    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """RoomType Model definition"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):
    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80, default="Anywhere", blank=True, null=True, verbose_name="City")
    price = models.IntegerField()  # PositiveIntegerField
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    parking = models.BooleanField(default=False)
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False, verbose_name="Instant Book")
    host = models.ForeignKey("users.User", related_name="rooms", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        print(reverse("rooms:detail", kwargs={"pk": self.pk}))
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    # def get_calendars(year, month):
    #     now = timezone.now()
    #     this_year = now.year
    #     next_year = this_year + 1
    #     this_month = now.month
    #     next_month = this_month + 1
    #     if year == this_year and month == this_month:
    #         calendar = Calendar(this_year, this_month)
    #         return calendar.get_days()
    #     elif year == this_year and month == next_month:
    #         calendar = Calendar(this_year, next_month)
    #         return calendar.get_days()
    #     else :
    #         calendar = Calendar(next_year, next_month)
    #         return calendar.get_days()
    #     return [this_month_cal, next_month_cal]

    # def get_calendars(self):
    #     now = timezone.now()
    #     this_year = now.year
    #     next_year = this_year + 1
    #     this_month = now.month
    #     next_month = this_month + 1
    #     # next_month2 = next_month + 1
    #     if this_month == 12:
    #         next_year = this_year + 1
    #         next_month = 1
    #     this_month_cal = Calendar(this_year, this_month)
    #     next_month_cal = Calendar(next_year, next_month)
    #     next_month2_cal = Calendar(next_year, next_month + 1)
    #     return [this_month_cal, next_month_cal]

    # def get_calendars(self, year, month):
    #     now = timezone.now()
    #     this_year = now.year
    #     next_year = this_year + 1
    #     this_month = now.month
    #     next_month = this_month + 1
    #     if this_month == 12 and next_month == 13:
    #         this_month_cal = Calendar(this_year, this_month)
    #         next_month_cal = Calendar(next_year, 1)
    #     return [this_month_cal, next_month_cal]
    # elif year == this_year and month == this_month:
    #     calendar = Calendar(this_year, this_month)
    #     return calendar.get_days()
    # elif year == this_year and month == next_month:
    #     calendar = Calendar(this_year, next_month)
    #     return calendar.get_days()
    # else:
    #     calendar = Calendar(next_year, next_month)
    #     return calendar.get_days()
    # return [this_month_cal, next_month_cal]

    # this_month_cal = Calendar(this_year, this_month)
    # next_month_cal = Calendar(this_year, next_month)
    # return [this_month_cal, next_month_cal]

    # class Room(models.Model):
    #     # other fields and methods

        def get_calendar_data(self):
            start = moment().subtract(29, 'days')
            end = moment()
            ranges = {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'),
                               moment().subtract(1, 'month').endOf('month')]
            }
            return {
                'start': start,
                'end': end,
                'ranges': ranges,
            }

    """LATEST TO BE HIDE"""
    #
    # def get_calendars(self):
    #     now = timezone.now()
    #     this_year = now.year
    #     this_month = now.month
    #     next_month = this_month + 1
    #     if this_month == 12 and next_month == 13:
    #         this_month_cal = Calendar(this_year, this_month)
    #         next_month_cal = Calendar(this_year + 1, 1)
    #     else:
    #         this_month_cal = Calendar(this_year, this_month)
    #         next_month_cal = Calendar(this_year, next_month)
    #     return [this_month_cal, next_month_cal]

# class Video(models.Model):
#     """Video Model Definition """
#
#     title = models.CharField(max_length=140)
#     added_by = models.DateTimeField(auto_now_add=True)
#     url = EmbedVideoField()
#     url = EmbedVideoField(default='https://www.youtube.com/watch?v=9bZkp7q19f0')
#     file = models.FileField(upload_to="room_videos")
#     room = models.ForeignKey("Room", related_name="videos", on_delete=models.CASCADE)
