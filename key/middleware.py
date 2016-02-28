from django.shortcuts import redirect


class KeyMiddleware(object):
    def process_request(self, request):
        return redirect('/')
