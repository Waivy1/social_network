from django.http import JsonResponse


def check_login_password_input(request):
    """
    checks and returns login data

    :return is_ok, login, password
    """
    try:
        login = request.POST['login']
        password = request.POST['password']

    # KeyError якщо нема значаення по цьому ключу
    except KeyError as e:
        return False, None, None

    if login == '' or password == '':
        return False, login, password

    return True, login, password

