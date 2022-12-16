from django.urls import path
from . import views

app_name = "paystack"

urlpatterns = [
    # path(
    #     "create/<int:room>/<int:year>-<int:month>-<int:day>",
    #     views.create,
    #     name="create",
    # ),
    # path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    # path("<int:pk>/<str:verb>", views.edit_reservation, name="edit"),
    # path("paystack/", views.customer_info, name="paystack"),  # paystack url
    path("paystack/", views.customer_info, name="paystack"),  # paystack url
    # path("verify/", views.verify, name="verify"),  # verify url
]
