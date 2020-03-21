from django.http import HttpResponse

def ping(req):
    return HttpResponse('<h1>pong</h1>')