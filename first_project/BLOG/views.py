from django.shortcuts import render
from rest_framework.views import APIView #our API view handler 
from rest_framework.response import Response #what defines the response
from rest_framework import status 
from django.http import HttpResponse #http - string -> response
from . import serializers 
from . import models 
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
import jwt #the jwt library


# def generate_access_token(user) -> None :
#      payload = { 
#         'user_id' : user.id,
#         'exp' : datetime.utcnow() + timedelta(days=30),
#         'iat': datetime.utcnow()
#      }

#      access_token = jwt.encode(payload, 'secret', algorithm='HS256')
#      return access_token

def generate_access_token(user) : 
    payload = { 
        'user_id' : user.id,
        'exp' : datetime.utcnow() + timedelta(days=5),
        'iat' : datetime.utcnow()
    }
    access_token = jwt.encode(payload, 'secret', algorithm='HS256')

    return access_token

class Test(APIView):
    def get(self, request):
        #return HttpResponse("This API works.")
        return Response({"message" : "this api works", "date" : "11/08/23"})
    
    def post(self, request):
        name = request.data['name']

        return Response({"name" : f"welcome {name}"})

class Signup(APIView):
    def post(self, request) : 
        serializer = serializers.BlogUserSerializer(data=request.data)
        if serializer.is_valid():
           # username = request.data.get('username')
            user_name = serializer.validated_data.get('username')
            if models.BlogUser.objects.filter(username=user_name).exists() : 
                return Response({'user already exists'})
            serializer.save(password=make_password(serializer.validated_data.get('password')))
            return Response({"message" : "user signed up successfully"}, status=status.HTTP_201_CREATED)
        else :
            return Response({"error" : serializer.errors})

class Login(APIView):
    def post(self, request):
        serializer = serializers.BlogUserSerializer(data=request.data)
        if serializer.is_valid() : 
            user_name = serializer.validated_data.get('username')
            pass_word = serializer.validated_data.get('password')
            try : 
                logged_user = models.BlogUser.objects.get(username=user_name)
            except Exception as e :
                return Response({'error' : str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            #check_password(login_input, db_current_password)
            password_check = check_password(pass_word, logged_user.password)
            if password_check : 
               token = generate_access_token(logged_user)
               response  = Response()
               response.set_cookie('access_token', value=token, httponly=True)
               response.data = { 
                'message' : 'login success',
                'access_token' : token
               }
               return response


            return Response({'message' : 'invalid credentials'})

# class Post(APIView):
#     def post(self, request) : 
#         token = request.COOKIES.get('access_token')
#         if not token : 
#                  return Response({'message' : 'unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#         try : 
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except Exception as e :
#             return Response({'error' : str(e), 'message' : 'an error occured'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = serializers.PostSerializer(data=request.data)
#         logged_user = models.BlogUser.objects.get(id=payload['user_id'])
#         if serializer.is_valid():
#             try : 
#                 serializer.save(postOwner=logged_user)
#             except Exception as e : 
#                 return Response({'error' : str(e)})
#             return Response({'message' : 'post has been created successfully'}, status=status.HTTP_201_CREATED)
#         return Response({'message' : 'data not valid'}, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request) : 
#         token = request.COOKIES.get('access_token')
#         if not token : 
#                  return Response({'message' : 'unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#         try : 
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except Exception as e :
#             return Response({'error' : str(e), 'message' : 'an error occured'}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = serializers.PostSerializer(models.Post.objects.all(), many=True)
#        # if serializer.is_valid() : 
#         return Response({'data' : serializer.data })
        



class Post(APIView):
    def post(self, request) : 
        token = request.COOKIES.get('access_token')
        if not token : 
            return Response({'message' : 'unauthenticated'})
        try : 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e : 
            return Response({'error' : str(e)})
        serializer = serializers.PostSerializer(data=request.data)
        try : 
            logged_user = models.BlogUser.objects.get(id=payload['user_id'])
        except Exception as e : 
            return Response({'error' : str(e)})
        if serializer.is_valid() : 
            serializer.save(postOwner=logged_user)
            return Response({'message' : 'post created successfully', 'post_data' : serializer.data})
        return Response({'error' : 'data is not valid'})

# post_5 = Post.objects.get(id=5)
# post_5.delete()



