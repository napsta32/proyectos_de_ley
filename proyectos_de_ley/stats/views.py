from django.shortcuts import render



def index(request):
    print("hola")
    return render(request, "stats/index.html")
