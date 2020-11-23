from django.shortcuts import render, redirect
from django.urls import reverse
from my_tenant.msal_middleware import ms_identity_web
from django import template
register = template.Library()

def index(request):
    return render(request, "my_tenant/auth/status.html")

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'my_tenant/auth/token.html')