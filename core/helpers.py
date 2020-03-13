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


class ValidationError(Exception):
    pass


class EmptyValueError(Exception):
    pass


def input_validate(request, keys):
    """
    :param keys -> list: input keys
    :return:
    """
    input_values = []
    try:
        for key in keys:
            input_values.append(request.POST[key])

    except KeyError as e:
        raise ValidationError(', '.join(e.args))

    if '' in input_values:
        raise EmptyValueError()

    return input_values

