from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    html = open('index.html')
    return HttpResponse(html)

# Create your views here.
