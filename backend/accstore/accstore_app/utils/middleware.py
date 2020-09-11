from datetime import datetime

from accstore_app.models_pack.models_user import Session


class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            key = request.COOKIES.get('sessid', '')
            session = Session.objects.get(key=key, expired__gt=datetime.now())
            request.session1 = session
            request.user = session.user

        except Session.DoesNotExist:
            request.user, request.session = None, None
        response = self.get_response(request)
        return response
