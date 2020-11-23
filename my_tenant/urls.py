from django.urls import path
from . import views
# from my_tenant.msal_middleware import config
# prefix = config.django.auth_endpoints.prefix + "/"

urlpatterns = [
    # path('', views.index, name='index'),
    # path('sign_in_status', views.index, name='status'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('aad_redirect', views.aad_redirect, name='aad_redirect'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('post_sign_out', views.post_sign_out, name='post_sign_out'),
    # path('token_details', views.token_details, name='token_details'),
]