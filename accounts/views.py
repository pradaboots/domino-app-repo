from django.http import HttpResponse
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "home.html"

def signup_view(request):
    return HttpResponse("Signup page placeholder")

def login_view(request):
    return HttpResponse("Login page placeholder")
