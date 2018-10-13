from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.utils import json
from . import serializers
from rest_framework.parsers import JSONParser
from .models import Movie_details
import re

class MovieDetailsAPIView(views.APIView):

    """
    Endpoint for posting movie details

    """

    permission_classes = (permissions.AllowAny, ) #Allows permission to all users to access this endpoint
    serializer_class = serializers.MovieDetailsSerializer
    parser_classes = (JSONParser, )  #To parse the json content


    def post(self, request): #For post request
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):   # Checking the JSON input
            theatre_name = request.data.get('name')  #getting name from the json input
            seat_info = request.data.get('seatInfo')
            for seat in seat_info.keys():  # Dict has keys and values, It is passing all the keys
                row_name = seat
                noOfSeats = seat_info[seat]['numberOfSeats']
                aisleSeats = seat_info[seat]['aisleSeats']

                # Checking if all the required information is present or not
                if row_name == "" or theatre_name == "" or noOfSeats == "" or aisleSeats == "":
                    return Response({"Fail" : "Please provide all the required details"}, status=status.HTTP_400_BAD_REQUEST)
            Movie_details(theatre_name=theatre_name, seatInfo=seat_info).save()
            return Response({"Success" : request.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class MovieReserveDetailsAPIView(views.APIView):

    """
    Endpoint for reserving movie seats

    """

    permission_classes = (permissions.AllowAny,)  #Allows permission to all users to access this endpoint
    serializer_class = serializers.MovieReserveConfirmation
    parser_classes = (JSONParser,) #To parse the json content

    # {screen-name} that we are passing in the url is automatically retrieved by this class so to use this screename is used, it is only a variable it can be anything
    def post(self, request, screenname):  # For post request
        screen_name = screenname
        #json.loads is converting the string-like json to json format as it is retrived from the database
        screen_details_json = json.loads(Movie_details.objects.get(theatre_name=screen_name).seatInfo.replace("'", "\""))
        serializer = self.serializer_class(data=request.data)
        data = request.data.get('seats')

        if serializer.is_valid(raise_exception=True):  # Checking the JSON input

            #Below code is used for ticket reserving
            for row_name in data.keys():
                try:
                    if screen_details_json[row_name]:
                        if data[row_name] != "" or screen_name != "" or row_name != "":
                            # checking if there are already reserved seats in the database for this row
                            try:
                                if screen_details_json[row_name]['reservedSeats'] is False:
                                    screen_details_json[row_name]['reservedSeats'] = []
                            except:
                                screen_details_json[row_name]['reservedSeats'] = []

                            #we are appending the data taken from the json-input to the reservedSeats
                            for seats in data[row_name]:
                                screen_details_json[row_name]['reservedSeats'].append(seats)

                            #we are removing the reserved seats from the continious list of seats
                            screen_details_json[row_name]['availableSeats'] = [i for i in list(range(0, screen_details_json[row_name]['numberOfSeats'])) if not i in screen_details_json[row_name]['reservedSeats']]

                            #saving and updating it the database
                            movie_object = Movie_details.objects.get(theatre_name=screen_name)
                            movie_object.seatInfo = screen_details_json
                            movie_object.save()
                        else:
                            return Response({"Fail": "Please provide all the required details"},
                                             status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print(e)
                    return Response({"Fail": row_name + " " + "not found in" + " " + screen_name},
                                    status=status.HTTP_400_BAD_REQUEST)

        return Response({"Screen Name": screen_name, "Success": screen_details_json},
                        status=status.HTTP_200_OK)




class AvailableSeatsAPIView(views.APIView):

    """
    Endpoint for showing Available Seats

    """

    permission_classes = (permissions.AllowAny,) #Allows permission to all users to access this endpoint

    # {screen-name} that we are passing in the url is automatically retrieved by this class so to use this screename is used, it is only a variable it can be anything
    def get(self, request, screenname):  # For get request

        #getting get-parameters that were passed to url , if they are found it is ok bit if not we are placing its value equal to empty string
        #If status is eqal to unreserved the only it will respond
        if request.query_params.get('status', "") != "" and request.query_params.get('status', "") == "unreserved":
            screen_name = screenname
            screen_details_json = json.loads(
                Movie_details.objects.get(theatre_name=screen_name).seatInfo.replace("'", "\""))

            #making dictionary to save the data
            data = {}
            data['seats'] = {}

            #getting available seats from the database if not found we are creating it
            for available_seats in screen_details_json.keys():
                try:
                    if screen_details_json[available_seats]['availableSeats']:
                        data['seats'][available_seats] = screen_details_json[available_seats]['availableSeats']
                except:
                    screen_details_json[available_seats]['availableSeats'] = list(
                        range(0, screen_details_json[available_seats]['numberOfSeats']))
                    data['seats'][available_seats] = screen_details_json[available_seats]['availableSeats']
            return Response({"Screen Name": screen_name, "Success": data}, status=status.HTTP_200_OK)

        #If numSeats and choice is passed it will choice is passed it will perform
        elif request.query_params.get('numSeats', "") != "" and request.query_params.get('choice', "") != "":
            numSeats = request.query_params['numSeats'] #getting numSeats from url
            choice   = request.query_params['choice'] #getting choice from the url
            row_name = re.sub('[^a-zA-Z]+', '', choice) #seperating alphabet from the seat number
            row_name_choice_seat = re.sub('\D+', '', choice) #seperating digit from the row_name
            screen_details_json = json.loads(Movie_details.objects.get(theatre_name=screenname).seatInfo.replace("'", "\""))
            data = {}
            seatsfound = []
            data['availableSeats'] = {}

            # getting available seats from the database if not found we are creating it
            for available_seats in screen_details_json.keys():
                try:
                    if screen_details_json[available_seats]['availableSeats']:
                        data['availableSeats'][available_seats] = screen_details_json[available_seats]['availableSeats']
                except:
                    data['availableSeats'][available_seats] = list(
                        range(0, screen_details_json[available_seats]['numberOfSeats']))

            #Logic for creating seating arrangement
            for i in group_consecutives(data['availableSeats'][row_name]):
                try:
                    if i.index(int(row_name_choice_seat)) is not None:
                        if len(i) >= int(numSeats):
                            index = i.index(int(row_name_choice_seat))
                            #if choice is found at the starting
                            if index == 0:
                                for k in range(0, len(i)):
                                    seatsfound.append(i[k])
                                    if k == int(numSeats)-1:
                                        break

                            # if choice is found at the ending
                            elif(index == len(i)-1):
                                for k in range(len(i)-1, -1, -1):
                                    seatsfound.append(i[k])
                                    if len(seatsfound) == int(numSeats):
                                        break

                            # if choice is found at the anywhere between starting and ending
                            else:
                                if index-(int(numSeats)-1) > 0:
                                    for k in range(index-(int(numSeats)-1), index+1):
                                        seatsfound.append(i[k])
                                else:
                                    for k in range(index, index+int(numSeats)):
                                        seatsfound.append(i[k])
                except:
                    continue

            #checkinng for aisle Seats if found it is showing error
            if(len(seatsfound) == 1):
                return Response({"availableSeats": seatsfound}, status=status.HTTP_200_OK)
            elif(len(seatsfound) > 1):
                for i in seatsfound:
                    if i in screen_details_json[row_name]['aisleSeats']:
                        seatsfound = []
                        seatsfound.append("Aisle Seat found Error!!")
                        break
                return Response({"availableSeats": seatsfound}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Seats not found for the user"}, status=status.HTTP_404_NOT_FOUND)
        elif request.query_params.get('status', "") != "" and request.query_params.get('status', "") != "unreserved":
            return Response({"Error" : "Status not recognized"}, status=status.HTTP_400_BAD_REQUEST)



def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result