from django.shortcuts import render

def index(request):
    return render(request, "taloflash/index.html")

def login(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "taloflash/login.html")
    
def register(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "taloflash/register.html")
