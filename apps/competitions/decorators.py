from functools import wraps

from rest_framework.generics import get_object_or_404

from apps.competitions.models import Competition


def is_owner(func):
    @wraps(func)
    def wrapper(view, request, *args, **kwargs):
        get_object_or_404(Competition, pk=kwargs['competition_pk'], author__email=request.user.email)
        response = func(view, request, *args, **kwargs)
        return response

    return wrapper
