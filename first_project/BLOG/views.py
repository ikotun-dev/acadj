from django.shortcuts import render
from rest_framework.views import APIView #our API view handler 
from rest_framework.response import Response #what defines the response
from rest_framework import status 
from django.http import HttpResponse #http - string -> response
from . import serializers 
from . import models 
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from django.db.models import Q

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

    def get(self, request) : 
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

        posts = models.Post.objects.all() 
        serializer = serializers.PostSerializer(posts, many=True)
        return Response({'data' : serializer.data})
    def delete(self, request)  :
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
        post_id = request.query_params.get('post_id')
        post_to_delete = models.Post.objects.get(id=post_id)
        post_to_delete.delete()
        return Response({'message' : 'post has been deleted'})
    def put(self, request) : 
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
        post_id = request.query_params.get('post_id')
        try : 
            post_to_update = models.Post.objects.get(id=post_id)
            if post_to_update.postOwner != logged_user : 
                return Response({'message' : 'this post does not belong to you'})
        except Exception as e :
            return Response({'error' : str(e)})
        serializer = serializers.PostSerializer(post_to_update, data=request.data, partial=True)
        if serializer.is_valid() : 
            serializer.save()
            return Response({'message' : 'post has been updated successfully', 'data' : serializer.data})
        return Response({'message' : 'serializer is not valid'})



class PersonalView(APIView) : 
    def get(self, request) : 
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

        posts = models.Post.objects.filter(postOwner = logged_user)
        posts_to_show = serializers.PostSerializer(posts, many=True)
        return Response({'data' : posts_to_show.data})

class SearchPost(APIView) : 
    def get(self, request) : 
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
        search_query = request.query_params.get('search')
        posts = models.Post.objects.filter(Q(postTitle__icontains=search_query))
        if posts : 
            posts_to_show = serializers.PostSerializer(posts, many=True)
            return Response({'data' : posts_to_show.data})
        return Response({'message' : 'Nothing found '})




class HirerSignup(APIView) : 
    def post(self, request) : 
        serializer = serializers.HirerSerializer(data=request.data)
        if serializer.is_valid() : 
            user_name = serializer.validated_data['username']
            if models.Hirer.objects.filter(username=user_name).exists(): 
                return Response({'message' : 'user with the username already exists'})
            serializer.save(password=make_password(serializer.validated_data.get('password')))
            return Response({'message' : 'account has been created successfully'})
        return Response({'message' : 'serializer is not valid'})

class HirerLogin(APIView) : 
    def post(self, request) : 
        serializer = serializers.HirerSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            if models.Hirer.objects.filter(username=user_name).exists(): 
                logged_user = models.Hirer.objects.get(username=user_name)
                validate = check_password(serializer.validated_data['password'], logged_user.password)
                if validate : 
                    token = generate_access_token(logged_user)  
                    response = Response()
                    response.set_cookie('access_token', value=token, httponly=True)
                    response.data = { 
                        'message' : 'login successful',
                        'access_token' : token
                    }
                    return response 

                return Response({'message' : 'invalid credentials'})
            return Response({'message' : 'invalid credentials'})
        return Response({'message' : 'serializer is not valid'})

class FreelancerSignup(APIView) : 
    def post(self, request) : 
        serializer = serializers.FreelancerSerializer(data=request.data)
        if serializer.is_valid() : 
            user_name = serializer.validated_data['username']
            if models.Hirer.objects.filter(username=user_name).exists(): 
                return Response({'message' : 'user with the username already exists'})
            serializer.save(password=make_password(serializer.validated_data.get('password')))
            return Response({'message' : 'account has been created successfully'})
        return Response

class FreelancerLogin(APIView) : 
    def post(self, request) : 
        serializer = serializers.FreelancerSerializer(data=request.data)
        if serializer.is_valid():
            user_name = serializer.validated_data.get('username')
            if models.Freelancer.objects.filter(username=user_name).exists(): 
                logged_user = models.Freelancer.objects.get(username=user_name)
                validate = check_password(serializer.validated_data['password'], logged_user.password)
                if validate : 
                    token = generate_access_token(logged_user)  
                    response = Response()
                    response.set_cookie('free_access_token', value=token, httponly=True)
                    response.data = { 
                        'message' : 'login successful',
                        'free_access_token' : token
                    }
                    return response 

                return Response({'message' : 'invalid credentials'})
            return Response({'message' : 'invalid credentials'})
        return Response({'message' : 'serializer is not valid'})

class CreateJob(APIView):
    def post(self, request) : 
        token = request.COOKIES.get('access_token')
        if not token : 
            return Response({'message' : 'unauthenticated'})
        try : 
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except Exception as e : 
            return Response({'error' : str(e)})
        try : 
            logged_user = models.Hirer.objects.get(id=payload['user_id'])
           # logged_user = models.Freelancer.objects.get(id=payload['user_id'])
            if not logged_user : 
                return Response({'message' : 'only an hirer can create job'})
        except Exception as e : 
            return Response({'error' : str(e)})
        serializer = serializers.JobSerializer(data=request.data)
        if serializer.is_valid() : 
            serializer.save(jobOwner=logged_user)
            return Response({'message' : 'job added succesfully'})
        return Response({'message' : 'serializer is not valid'})
