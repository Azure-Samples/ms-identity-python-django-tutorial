from django.shortcuts import render
from django.conf import settings
import requests

ms_identity_web = settings.MS_IDENTITY_WEB

def index(request):
    return render(request, "auth/status.html")

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')

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
    else:
        results['value'] =[{'displayName': 'call-graph-error', 'id': 'call-graph-error'}]
    return render(request, 'auth/call-graph.html', context=dict(results=results))
