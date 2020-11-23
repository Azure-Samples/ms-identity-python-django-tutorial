from django.shortcuts import render, redirect
from django.urls import reverse
from my_tenant.msal_middleware import ms_identity_web, config
import logging

logger = logging.getLogger('MsalViewsLogger')

prefix = config.django.auth_endpoints.prefix + "/"
endpoints = config.django.auth_endpoints

def index(request):
    return render(request, "my_tenant/auth/status.html")

def sign_in(request):
    logger.debug(f"{prefix}{endpoints.sign_in}: request received. will redirect browser to login")
    auth_url = ms_identity_web.get_auth_url(redirect_uri=request.build_absolute_uri(reverse(endpoints.redirect)))
    return redirect(auth_url)

def edit_profile(request):
    logger.debug(f"{prefix}{endpoints.edit_profile}: request received. will redirect browser to edit profile")
    auth_url = ms_identity_web.get_auth_url(
            redirect_uri=request.build_absolute_uri(reverse(endpoints.redirect)),
            b2c_policy=ms_identity_web.aad_config.b2c.profile)
    return redirect(auth_url)

def aad_redirect(request):
    logger.debug(f"{prefix}{endpoints.redirect}: request received. will process params")
    next_action = redirect(reverse('index'))
    return ms_identity_web.process_auth_redirect(next_action, # TODO: remove 'next_action' -> add redirect function to django adapter?
        redirect_uri=request.build_absolute_uri(reverse(endpoints.redirect))) 


def sign_out(request):
    logger.debug(f"{prefix}{endpoints.sign_out}: signing out username: {request.identity_context_data.username}")
    return ms_identity_web.sign_out(request.build_absolute_uri(reverse(endpoints.post_sign_out)))    # send the user to Azure AD logout endpoint


def post_sign_out(request):
    logger.debug(f"{prefix}{endpoints.post_sign_out}: clearing session for username: {request.identity_context_data.username}")
    ms_identity_web.remove_user(request.identity_context_data.username)  # remove user auth from session on successful logout
    return redirect(reverse('index'))                   # take us back to the home page

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'my_tenant/auth/token.html')