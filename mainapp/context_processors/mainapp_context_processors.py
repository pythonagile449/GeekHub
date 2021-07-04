from mainapp.models import Hub


def mainapp_context(request):
    return {
        'hubs': Hub.objects.all()
    }
