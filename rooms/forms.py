from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    # host = forms.ModelMultipleChoiceField
    # start_date = forms.cleaned_data.get("start_date")
    # end_date = forms.cleaned_data.get("end_date")
    # start_time = forms.cleaned_data.get("start_time")
    # end_time = forms.cleaned_data.get("end_time")

    # def ok_reservation(self, start_date, end_date, qs=None):
    #     if start_date and end_date:
    #         qs = qs.exclude(reservations__check_in__lte=end_date, reservations__check_out__gte=start_date)
    #     return qs


# 1. host 필드를 추가하고, 2. host 필드의 queryset을 설정합니다.


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
            "host",
            "start_date",
            "end_date",
            "start_time",
            "end_time",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
