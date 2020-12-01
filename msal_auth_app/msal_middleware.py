from ms_identity_web import IdentityWebPython
from ms_identity_web.context import IdentityContextData
from ms_identity_web.adapters import IdentityWebContextAdapter
from ms_identity_web.errors import NotAuthenticatedError
from django.http.request import HttpRequest as DjangoHttpRequest
from django.conf import settings
from django.shortcuts import render, redirect as django_redirect
import logging

ms_identity_web = IdentityWebPython(settings.AAD_CONFIG)

class MsalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.ms_identity_web = ms_identity_web
    
    def process_exception(self, request, exception):
        if isinstance(exception, NotAuthenticatedError):
            return render(request, settings.ERROR_TEMPLATE.format(exception.code))
        return None

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        django_context_adapter = DjangoContextAdapter(request)
        self.ms_identity_web.set_adapter(django_context_adapter)
        django_context_adapter._on_request_init()
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        django_context_adapter._on_request_end()

        return response


class DjangoContextAdapter():
    """Context Adapter to enable IdentityWebPython to work within the Django environment"""
    def __init__(self, request: DjangoHttpRequest) -> None:
        # TODO: remove the following and add a middleware loaded before this one for global request/session context?
        self.request = request
        self._session = request.session
        self.logger = logging.getLogger('MsalMiddleWareLogger')

    @property
    def identity_context_data(self) -> 'IdentityContextData':
        # TODO: make the key name configurable
        self.logger.debug("Getting identity_context from request/session")
        identity_context_data = getattr(self.request, IdentityContextData.SESSION_KEY, None)
        if not identity_context_data:
            identity_context_data = self._deserialize_identity_context_data_from_session()
            setattr(self.request, IdentityContextData.SESSION_KEY, identity_context_data)
        return identity_context_data

    def _on_request_init(self) -> None:
        try:
            self.identity_context_data() # initialize it so it is available to request context
        except Exception as ex:
            self.logger.error(f'MsalMiddleware failed @ _on_request_init\n{ex}')

    # this is for saving any changes to the identity_context_data
    def _on_request_end(self) -> None:
        try:
            if getattr(self.request, IdentityContextData.SESSION_KEY, None):
                self._serialize_identity_context_data_to_session()
        except Exception as ex:
            self.logger.error(f'MsalMiddleware failed @ _on_request_ended\n{ex}')

    # TODO: order is reveresed? create id web first, then attach django adapter to it!?
    def attach_identity_web_util(self, identity_web: 'IdentityWebPython') -> None:
        """attach the identity web instance somewhere so it is accessible everywhere.
        e.g., ms_identity_web = current_app.config.get("ms_identity_web")\n
        Also attaches the application logger."""
        aad_config = identity_web.aad_config
        config_key = aad_config.django.id_web_configs

        setattr(self.request, config_key, aad_config)
        
    @property
    def has_context(self) -> bool:
        return True # TODO: remove this? not relevant for django?

    @property
    def session(self) -> None:
        return self._session

    # TODO: only clear IdWebPy vars
    def clear_session(self) -> None:
        """this function clears the session and refreshes context. TODO: only clear IdWebPy vars"""
        # TODO: clear ONLY msidweb session stuff
        self.session.flush()

    def redirect_to_absolute_url(self, absolute_url: str) -> None:
        """this function redirects to an absolute url"""
        return django_redirect(absolute_url)
        
    def get_request_params_as_dict(self) -> dict:
        try:
            if self.request.method == "GET":
                return self.request.GET.dict()
            elif self.request.method == "POST" :
                return self.request.POST.dict()
            else:
                raise ValueError("Django request must be POST or GET")
        except:
            if self.logger is not None:
                self.logger.warning("Failed to get param dict, substituting empty dict instead")
            return dict()

    # does this need to be public method?
    def _deserialize_identity_context_data_from_session(self) -> 'IdentityContextData':
        blank_id_context_data = IdentityContextData()
        try:
            id_context_from_session = self.session.get(IdentityContextData.SESSION_KEY, dict())
            blank_id_context_data.__dict__.update(id_context_from_session)
        except Exception as exception:
            self.logger.warning(f"failed to deserialize identity context from session: creating empty one\n{exception}")
        return blank_id_context_data

    # does this need to be public method?
    def _serialize_identity_context_data_to_session(self) -> None:
        try:
            identity_context = self.identity_context_data
            if identity_context.has_changed:
                identity_context.has_changed = False
                identity_context = identity_context.__dict__
                self.session[IdentityContextData.SESSION_KEY] = identity_context
        except Exception as exception:
            self.logger.error(f"failed to serialize identity context to session.\n{exception}")
