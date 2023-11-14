from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView
# Create your views here.

class ChatAPI(CreateAPIView):
    pass

class ReviewAPI(CreateAPIView):
    pass

class ChatListAPI(ListAPIView):
    pass

class ReviewListAPI(ListAPIView):
    pass