from accstore.settings import SITENAME


def sitename(request):
    return {'sitename': SITENAME}