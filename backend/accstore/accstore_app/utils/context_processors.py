from accstore.settings import SITENAME


def accstore_app_context(request):
    return {'lang': request.lang, 'sitename': SITENAME}