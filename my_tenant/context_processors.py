from django.urls import reverse
from my_tenant.msal_middleware import config

def context(request):
    claims = request.identity_context_data._id_token_claims
    exclude_claims = ['iat', 'exp', 'nbf', 'uti', 'aio']
    claims_to_display = {claim: value for claim, value in claims.items() if claim not in exclude_claims}

    client_id=config.client.client_id
    aad_link="https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/Authentication/appId/" + client_id +"/isMSAApp/"
    
    return dict(claims_to_display=claims_to_display,
                redirect_uri_external_link = request.build_absolute_uri(reverse('aad_redirect')),
                aad_link=aad_link)
