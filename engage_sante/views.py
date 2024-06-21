from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def mentions(request):
    return render(request, 'mentions.html')