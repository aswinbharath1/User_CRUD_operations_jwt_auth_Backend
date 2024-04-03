from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializers
from .models import User
import jwt ,datetime
# Create your views here.
class Register(APIView):
    def post(self,request):
        email = request.data['email']
        user = User.objects.filter(email = email).first()

        if user:
            raise AuthentiationFailed(data="User already exists")  # return error
        serializer = UserSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)   # validate the data
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthentiationFailed("User does not exists")
        if not user.check_password(password):
            raise AuthentiationFailed("Password is incorrect")
        
        payload = {
            'id': user.id,
            'exp':datetime.datetime.utcnow()+ datetime.timedelta(minutes = 60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret', algorithm = 'HS256')
        response = Response()
        response.set_cookie(key = 'jwt', value = token , httponly = True , samesite = 'none' , secure = True)
        response.data = {
            'jwt': token
        }
        print(response)

        return response 
    
class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthentiationFailed('Authentication cookie missing ')
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed( "Token has expired ")
        user = User.objects.get(id = payload['id'])
        serializer = UserSerializers(user)
        
        return Response(serializer.data)
class UpdateView(APIView):
    def post(self, request):
        token = request.COOKIES.get( 'jwt' )

        if not token :
            raise AuthentiationFailed('Authenticateion cookie missing ')
        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError :
            raise AuthentiationFailed('Token has Expired Signature Error')
        user = User.objects.get(id = payload['id'])
        serializer = UserSerializers(user, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response
    
class LogoutView(APIView):
    def post(self, request):
        tocken = request.COOKIES.get('jwt')
        response = Response()
        response.set_cookie(key='jwt', value=tocken, httponly=True, samesite="none", secure=True, max_age=0)

        response.data = {
            'message': 'success'
        }
        return response