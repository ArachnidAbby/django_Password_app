from django.http import HttpResponse
from django.shortcuts import render
from cryptography.fernet import InvalidToken

from .models import Password
import json

FORCE_HTTPS = True


# Create your views here.
def index(request):
    # if not request.session.exists:
    #     request.session.create()
    passwords = Password.objects.all()
    context = {
        "passwords": passwords
    }
    return HttpResponse(render(request, "index.html", context))


# api
def set_master_pass(request):
    if FORCE_HTTPS and not request.is_secure():
        return HttpResponse(status=401)
    if request.method != "POST":
        return HttpResponse(status=400)
    request.session["master_password"] = Password.hash_pswd(bytes(json.loads(request.body)["pswd"], 'utf-8')).decode('utf-8')
    return HttpResponse(status=200)


def get_password(request, website_name):
    if FORCE_HTTPS and not request.is_secure():
        return HttpResponse(status=401)
    if request.method != "GET":
        return HttpResponse(status=400)
    password_obj = Password.objects.filter(website=website_name).first()
    try:
        return HttpResponse(password_obj.get_password(request.session["master_password"]), status=200)
    except InvalidToken:
        return HttpResponse(status=400)


def set_password(request):
    if FORCE_HTTPS and not request.is_secure():
        return HttpResponse(status=401)
    if request.method != "POST":
        return HttpResponse(status=400)
    data = json.loads(request.body)
    password = Password()
    password.website = data['website']
    password.username = data['username']
    password.set_password(bytes(data["password"], 'utf-8'), request.session["master_password"])
    password.save()
    return HttpResponse(status=200)
