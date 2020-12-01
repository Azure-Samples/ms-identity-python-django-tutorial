from django.urls import path
from . import views
from msal_auth_app.msal_middleware import ms_identity_web
endpoints = ms_identity_web.aad_config.django.auth_endpoints

urlpatterns = [
    path(endpoints.sign_in, views.sign_in, name=endpoints.sign_in),
    path(endpoints.edit_profile, views.edit_profile, name=endpoints.edit_profile),
    path(endpoints.redirect, views.aad_redirect, name=endpoints.redirect),
    path(endpoints.sign_out, views.sign_out, name=endpoints.sign_out),
    path(endpoints.post_sign_out, views.post_sign_out, name=endpoints.post_sign_out),
]