import secrets
import string
from datetime import datetime, timedelta

from accstore_app.models import *
import random

from accstore_app.utils.tools import get_sha


def get_auth_data(request):
    login_ = request.POST.get('login')
    password = request.POST.get('password')
    url = request.POST.get('continue', '/')
    return login_, password, url


def do_login(login, password):
    print(login, password)
    try:
        user = User.objects.get(login=login)
    except User.DoesNotExist:
        return None
    hashed_pass = get_sha(password)
    print(hashed_pass)
    print(user.sha_password)
    print(user.sha_password == hashed_pass)

    session = Session()
    session.key = generate_cookie()
    session.user = user
    session.expired = datetime.now() + timedelta(days=5)
    session.save()
    return session.key


def generate_cookie():
    key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(random.randint(128, 4000)))
    return key

