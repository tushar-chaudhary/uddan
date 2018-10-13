from django.db.models import Q
from rest_framework import serializers
from .models import Movie_details


#Serializers are used to take the JSON input

class MovieDetailsSerializer(serializers.Serializer):

    #taking name in the json format
    name = serializers.CharField(
        required=True,
        label="Name"
    )

    #taking everything except the name all
    seatInfo = serializers.StringRelatedField()

    #It is representing the fields that are to be passed in the json
    class Meta(object):
        model  = Movie_details
        fields = ['name', 'seatInfo']

    #validating the name
    def validate_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Name should not be blank.")
        return value

class MovieReserveConfirmation(serializers.Serializer):

    #to take seats while movie reservation
    seats = serializers.StringRelatedField()

    # It is representing the fields that are to be passed in the json
    class Meta(object):
        model  = Movie_details
        fields = ['seats']

    # validating the seats
    def validate_seats(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Seats should not be blank.")
        return value


class AvailableSeats(serializers.Serializer):

    seats = serializers.StringRelatedField()

    class Meta(object):
        model  = Movie_details
        fields = ['seats']



