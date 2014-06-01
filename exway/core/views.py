from django.shortcuts import render

def home(request):
    """ This view just returns the html for the draw page """
    return render(request, 'home.html', {})
