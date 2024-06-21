from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def mentions(request):
    return render(request, 'mentions.html')

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)