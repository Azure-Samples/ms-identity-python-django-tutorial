# from ms_identity_web import IdentityWebContextAdapter
# from typing import Any
# from functools import wraps

# # # decorator to make sure access within request context
# # def require_request_context(f):
# #     @wraps(f)
# #     def assert_context(self, *args, **kwargs):
# #         if not flask_has_request_context():
# #             self.logger.info(f"{self.__class__.__name__}.{f.__name__}: No request context, aborting")
# #         else:
# #             return f(self, *args, **kwargs)
# #     return assert_context


# class DjangoContextAdapter(IdentityWebContextAdapter):
#     """Context Adapter to enable IdentityWebPython to work within the Flask environment"""
#     def __init__(self, app) -> None:
#         assert isinstance(app, flask_app)
#         super().__init__()
#         self.app = app
#         with self.app.app_context():
#             self.logger = app.logger
#             app.before_request(self._on_request_init)
#             app.after_request(self._on_request_end)

#     @property
#     @require_request_context
#     def identity_context_data(self) -> 'IdentityContextData':
#         # TODO: make the key name configurable
#         self.logger.debug("Getting identity_context from g")
#         identity_context_data = flask_g.get(IdentityContextData.SESSION_KEY)
#         if not identity_context_data:
#             identity_context_data = self._deserialize_identity_context_data_from_session()
#             setattr(flask_g, IdentityContextData.SESSION_KEY, identity_context_data)
#         return identity_context_data

#     # method is called when flask gets an app/request context
#     # Flask-specific startup here?    
#     def _on_request_init(self) -> None:
#         try:
#             idx = self.identity_context_data # initialize it so it is available to request context
#         except Exception as ex:
#             self.logger.error(f'Adapter failed @ _on_request_init\n{ex}')

#     # this is for saving any changes to the identity_context_data
#     def _on_request_end(self, response_to_return=None) -> None:
#         try:
#             if IdentityContextData.SESSION_KEY in flask_g:
#                 self._serialize_identity_context_data_to_session()
#         except Exception as ex:
#             self.logger.error(f'flask adapter failed @ _on_request_ended\n{ex}')

#         return response_to_return

#     # TODO: order is reveresed? create id web first, then attach flask adapter to it!?
#     def attach_identity_web_util(self, identity_web: 'IdentityWebPython') -> None:
#         """attach the identity web instance to session so it is accessible everywhere.
#         e.g., ms_id_web = current_app.config.get("ms_identity_web")\n
#         Also attaches the application logger."""
#         aad_config = identity_web.aad_config
#         config_key = aad_config.flask.id_web_configs

#         with self.app.app_context():
#             self.app.config[config_key] = aad_config

#         identity_web.set_logger(self.logger)
#         auth_endpoints = FlaskAADEndpoints(identity_web)
#         self.app.context_processor(lambda: dict(ms_id_url_for=auth_endpoints.url_for))
#         self.app.register_blueprint(auth_endpoints)        
        
        

#     @property
#     def has_context(self) -> bool:
#         return flask_has_request_context()

#     ### not sure if this method needs to be public yet :/
#     @property
#     @require_request_context
#     def session(self) -> None:
#         return flask_session

#     # TODO: only clear IdWebPy vars
#     @require_request_context
#     def clear_session(self) -> None:
#         """this function clears the session and refreshes context. TODO: only clear IdWebPy vars"""
#         # TODO: clear ONLY msidweb session stuff
#         flask_session.clear()

#     @require_request_context
#     def redirect_to_absolute_url(self, absolute_url: str) -> None:
#         """this function redirects to an absolute url"""
#         return flask_redirect(absolute_url)

#     @require_request_context
#     def get_request_params_as_dict(self) -> dict:
#         """this function returns the params dict from any flask request"""
#         try:
#             # this is query and form-post params merged,
#             # preferring query param if there is a key collision
#             return flask_request.values
#         except:
#             if self.logger is not None:
#                 self.logger.warning("failed to get param dict from request, substituting empty dict instead")
#             return dict()

#     # does this need to be public method?
#     @require_request_context
#     def _deserialize_identity_context_data_from_session(self) -> 'IdentityContextData':
#         blank_id_context_data = IdentityContextData()
#         try:
#             id_context_from_session = self.session.get(IdentityContextData.SESSION_KEY, dict())
#             blank_id_context_data.__dict__.update(id_context_from_session)
#         except Exception as exception:
#             self.logger.warning(f"failed to deserialize identity context from session: creating empty one\n{exception}")
#         return blank_id_context_data

#     # does this need to be public method?
#     @require_request_context
#     def _serialize_identity_context_data_to_session(self) -> None:
#         try:
#             identity_context = self.identity_context_data
#             if identity_context.has_changed:
#                 identity_context.has_changed = False
#                 identity_context = identity_context.__dict__
#                 self.session[IdentityContextData.SESSION_KEY] = identity_context
#         except Exception as exception:
#             self.logger.error(f"failed to serialize identity context to session.\n{exception}")
