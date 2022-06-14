import re
import requests
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    Carserializer, Routeserializer, Scheduleserializer, Passengerserializer
)

from .models import (
    Cars,Route,Schedules, Passengers
)

imgPath = './media/qrcode/qr.png'
# Create your views here.

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer Tj10Aw8XSTbXfYnaCiMazYeLNdj7'
}

# -----------------business logic----------------


class passengerCount(APIView):

    def get(self, request):

        seats = Schedules.objects.all()
        for x in seats:
            s = x.available_seats
        return Response({"data": 'shiet'}, status=status.HTTP_200_OK)
    def post(self,request):

        return

class SchedulesView(APIView):

    def get(self, request):

        try:
            schedule_id =request.query_params['scheduleid']
            print(schedule_id)
            schedules = Schedules.objects.get(id=int(schedule_id))

            serializer = Scheduleserializer(schedules, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:

            schedules = Schedules.objects.all()

            serializer = Scheduleserializer(schedules, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        try:
            
            data = request.data
            postData = Schedules(
                car_id=data['carID'],routes_id=data['routeID'],date=data['date'],
                time=data['time'],price=data['price']
            )
            postData.save()
            serializer = Scheduleserializer(postData, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except:
            return Response({'error':'created'},status=status.HTTP_400_BAD_REQUEST)


class SearchCar(APIView):

    def post(self, request):

        try:
            data = request.data
            car = Cars.objects.filter(plate_name__icontains=data['car'])
            serailizer = Carserializer(car, many=True)

            return Response(serailizer.data, status=status.HTTP_200_OK)
        except:
            return Response({'data': 'not found'}, status=status.HTTP_404_NOT_FOUND)


class searchRoutes(APIView):

    def get(self, request):
        try:
            data = request.query_params['place']

            try:
                routes = Route.objects.filter(departure__icontains=data)
                serializer = Routeserializer(routes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Route.DoesNotExist:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PassengersView(APIView):

    def post(self, request):

        try:
            data = request.data
            try:
                passenger = Passengers(schedules_id=int(data['scheduleID']), phone_number=data['phoneNO'], seats=int(data['seats']))
                try:
                    passenger.name = data['name']
                except:
                    pass
                passenger.save()
                serializer = Passengerserializer(passenger, many=False)

                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                print('shiet1')
                id_data = int(data['passengerID'])
                fare = int(data['fare'])
                print(id_data, fare)
                passenger = Passengers.objects.get(id=id_data)
                print(int('254'+ str(passenger.phone_number[1:])))
                now = datetime.now()
                now = re.sub('[-:]', '',str(now))
                now = now.replace(' ', '').split('.')
                print(str(now[0]))
                payload = {
                    "BusinessShortCode": 174379,
                    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwNjAyMTM1MDI1",
                    "Timestamp": str(now[0]),
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": fare,
                    "PartyA": 254708374149,
                    "PartyB": 174379,
                    "PhoneNumber": int('254'+ str(passenger.phone_number[1:])),
                    "CallBackURL": "https://mydomain.com/path",
                    "AccountReference": "Qrcode",
                    "TransactionDesc": "buy a ticket" 
                }

                response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
                print(response)
                passenger.fare = data['fare']
                passenger.save()

                serializer =Passengerserializer(passenger, many=False)

                return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)