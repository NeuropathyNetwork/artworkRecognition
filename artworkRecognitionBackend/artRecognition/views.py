from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")

def analyze(request):
    return render(request, 'analyze.html')