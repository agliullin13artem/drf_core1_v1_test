from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from home.models import Person
from home.serializers import LoginSerializer, PeopleSerializer, RegisterSerializer

from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": False,
                    "message": serializer.errors,
                },
                status.HTTP_400_BAD_REQUEST,)
        
        print(serializer.data)
        user = authenticate(username=serializer.data["username"], password=serializer.data["password"])
        
        if not user:
            return Response(
                {
                    "status": False,
                    "message": 'invalid creanet',
                },
                status.HTTP_400_BAD_REQUEST,)

        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({
            'status': True, 
            'message': 'user login',
            'token': str(token),
        }, status.HTTP_201_CREATED)
    

class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {"status": False, "message": serializer.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(
            {"status": True, "message": "user created"}, status.HTTP_201_CREATED
        )


@api_view(["GET", "POST", "PUT"])
def index(request):
    course = {
        "course_name": "Python",
        "learn": ["Flask", "Django", "Tornado", "FastApi"],
        "course_provider": "Scarler",
    }
    if request.method == "GET":
        print(request.GET.get("search"))
        print("YOU GET")
        return Response(course)

    elif request.method == "POST":
        data = request.data
        print("*******")
        print(data["age"])
        print("*****")
        print("YOU POST")
        return Response(course)

    elif request.method == "PUT":
        print("YOU PUT")
        return Response(course)
    else:
        data = request.data
        print(data)
        json_response = {
            "name": "Scarlet",
            "course": ["C++", "Python"],
            "method": "POST",
        }
    return Response(json_response)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        obj = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = PeopleSerializer(obj, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "person delete"})


@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({"message": "success"})

    return Response(serializer.errors)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def person(request):
    if request.method == "GET":
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "person deleted"})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response(
            {"status": 200, "data": serializer.data}, status=status.HTTP_204_NO_CONTENT
        )
