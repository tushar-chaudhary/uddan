from django.conf.urls import url
from .views import MovieDetailsAPIView, MovieReserveDetailsAPIView, AvailableSeatsAPIView

app_name = "app"


#These are the endpoints
urlpatterns = [
    url(r'^screens/$', MovieDetailsAPIView.as_view(), name="Movie Details"),
    url(r'^screens/(?P<screenname>\w+)/reserve', MovieReserveDetailsAPIView.as_view(), name="Movie Reserve"),
    url(r'^screens/(?P<screenname>\w+)/seats', AvailableSeatsAPIView.as_view(), name="Available Seats"),
]
