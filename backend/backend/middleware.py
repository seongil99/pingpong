# your_app/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class RedirectToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Exclude the login and registration pages from the redirect
            if request.path not in [reverse('login'), reverse('register')]:
                return redirect('login')  # Change 'login' to your actual login URL name

        response = self.get_response(request)
        return response

