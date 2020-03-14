
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

