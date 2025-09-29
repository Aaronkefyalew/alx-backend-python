import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method}\n"

        # Write log entry to a file
        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current time
        current_time = datetime.datetime.now().time()
        
        # Define restricted hours (10 PM to 6 AM)
        start_restriction = datetime.time(22, 0)  # 10:00 PM
        end_restriction = datetime.time(6, 0)     # 6:00 AM
        
        # Check if current time is within restricted hours
        if start_restriction <= current_time or current_time <= end_restriction:
            # Allow access to admin URLs and authentication URLs
            if not (request.path.startswith('/admin/') or 
                   request.path.startswith('/api/token/') or
                   request.path.startswith('/api/token/refresh/')):
                return HttpResponseForbidden(
                    "Access restricted between 10 PM and 6 AM. Please try again during allowed hours."
                )
        
        response = self.get_response(request)
        return response
