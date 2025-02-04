# core/middleware.py
import time
from django.http import JsonResponse

class ScrapeThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_request = 0

    def __call__(self, request):
        if '/api/pages/' in request.path:
            current_time = time.time()
            if current_time - self.last_request < 30:  # 30-second delay
                return JsonResponse(
                    {"error": "Too many requests. Please wait 30 seconds between scrapes."},
                    status=429
                )
            self.last_request = current_time
        return self.get_response(request)