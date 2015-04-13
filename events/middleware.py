from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions

from django.http import HttpResponse, HttpResponseBadRequest


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, 'AuthCanceled'):

        else:
            raise exception