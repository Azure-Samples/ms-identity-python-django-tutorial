from django.shortcuts import render, redirect
from django.urls import reverse
from my_tenant.msal_middleware import ms_identity_web
from django import template
import requests

register = template.Library()

def index(request):
    return render(request, "my_tenant/auth/status.html")

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'my_tenant/auth/token.html')

@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    # trim the results down to 5 and format them.
    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:5]

    return render(request, 'my_tenant/auth/call-graph.html', context=dict(results=results))