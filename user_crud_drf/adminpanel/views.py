from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from user.serializers import UserSerializers
from user.models import User
import jwt,datetime


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response('user does not exists')
        if not user.check_password(password):
            return Response("password is incorrect")
        if not user.is_superuser:
            raise AuthenticationFailed('Access Cannot be Granted')
        payload = {
            'id' :  user.id , 
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            'iat': datetime.datetime.utcnow()
        }
        token =  jwt.encode(payload, 'secret' , algorithm = 'HS256')
        response = Response()
        response.set_cookie(key = 'jwt' , value = token , httponly = True , samesite = "none" , secure = True)
        response.data = {
            'jwt': token
        }
        return response
    
class UserView(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Authentication Failure')
        try:
            payload = jwt.decode(token, 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired')
        users = User.objects.all().order_by('id')
        serializer = UserSerializers(users, many = True)
        return Response(serializer.data)
    
class UserUpdateView(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed( 'Unauthenticated')
        try:
            payoad = jwt.decode(token, 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed( "Auth Token has expired")
        uid = request.data['id']
        user = User.objects.get(id = uid)
        serializer = UserSerializers(user , data=request.data , partial = True)
        serializer.is_valid(raise_exceptions = True)
        serializer.save()

        users = User.objects.all().order_by('id')
        serializer = UserSerializers(users , many =True)
        return Response(serializer.data)
class UserDeleteView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed( 'Unauthenticated')
        try:
            payoad = jwt.decode(token, 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed( "Auth Token has expired")
        uid = request.data['id']
        user = User.objects.get(id =uid )
        user.delete()

        users = User.objects.all().order_by('id')
        serializer = UserSerializers(users , many=True)

        return Response(serializer.data)