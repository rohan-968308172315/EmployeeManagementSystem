from django.shortcuts import redirect

class LoginRequireMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        allowed_urls = [
            '/login/',
            '/admin/login/',
            '/forgot-password/',
            '/reset-password/',
            '/static/',
        ]

        if not request.user.is_authenticated:

            if not any(request.path.startswith(url) for url in allowed_urls):
                return redirect('/login/')

        response = self.get_response(request)

        return response