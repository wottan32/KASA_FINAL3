import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


@login_required
def create(request, room, year, month, day, **kwargs):
    global date_obj
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=30),
            # change days number to edit how long your reservation will last
        )
        # models.BookedDay.objects.create(day=date_obj, reservation=reservation)
        # messages.success(request, "Reservation Created")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
                reservation.guest != self.request.user
                and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
            reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


def delete_reservation(request, pk):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
            reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    reservation.delete()
    messages.success(request, "Reservation Deleted")
    return redirect(reverse("core:home"))


# def pay_reservation(request, pk):
#     reservation = models.Reservation.objects.get_or_none(pk=pk)
#     if not reservation or (
#             reservation.guest != request.user and reservation.room.host != request.user
#     ):
#         raise Http404()
#     reservation.status = models.Reservation.STATUS_PAID
#     reservation.save()
#     messages.success(request, "Reservation Paid")
#     return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
#
#
# class pay(View):
#     def get(self, *args, **kwargs):
#         pk = kwargs.get("pk")
#         reservation = models.Reservation.objects.get_or_none(pk=pk)
#         if not reservation or (
#                 reservation.guest != self.request.user
#                 and reservation.room.host != self.request.user
#         ):
#             raise Http404()
#         return render(
#             self.request,
#             "reservations/pay.html",
#             {"reservation ": reservation},
#         )
#         return render(self.request, "reservations/pay.html")
#
#     def post(self, *args, **kwargs):
#         pk = kwargs.get("pk")
#         reservation = models.Reservation.objects.get_or_none(pk=pk)
#         if not reservation or (
#                 reservation.guest != self.request.user
#                 and reservation.room.host != self.request.user
#         ):
#             raise Http404()
#         reservation.status = models.Reservation.STATUS_PAID
#         reservation.save()
#         messages.success(self.request, "Reservation Paid")
#         return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
#
# def customer_info(request):
#     return None