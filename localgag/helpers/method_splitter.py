from django.http import Http404


def method_splitter(request, **kwargs):
    get = kwargs.pop('GET', None)
    post = kwargs.pop('POST', None)
    delete = kwargs.pop('DELETE', None)

    if request.method == 'GET' and get:

        return get(request, **kwargs)
    elif request.method == 'POST' and post:

        return post(request, **kwargs)
    elif request.method == 'DELETE' and delete:

        return delete(request, **kwargs)

    raise Http404()
