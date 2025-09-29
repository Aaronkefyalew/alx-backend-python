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
        """
        Restrict access to the messaging app between 9 PM (21:00) and 6 AM (06:00)
        """
        # Get current server time
        current_time = datetime.datetime.now().time()
        
        # Define restricted period: 9 PM to 6 AM
        restriction_start = datetime.time(21, 0)  # 9:00 PM
        restriction_end = datetime.time(6, 0)     # 6:00 AM
        
        # Check if current time is within restricted hours
        is_restricted = False
        
        if restriction_start < restriction_end:
            # Normal case: restriction within same day
            is_restricted = restriction_start <= current_time <= restriction_end
        else:
            # Overnight case: restriction spans midnight
            is_restricted = current_time >= restriction_start or current_time <= restriction_end
        
        # If within restricted hours, deny access to messaging endpoints
        if is_restricted:
            # Check if the request is trying to access messaging endpoints
            if (request.path.startswith('/api/conversations/') or 
                request.path.startswith('/api/messages/') or
                request.path.startswith('/chats/')):
                return HttpResponseForbidden(
                    "Access to messaging service is restricted between 9 PM and 6 AM. "
                    "Please try again during allowed hours (6 AM to 9 PM)."
                )
        
        response = self.get_response(request)
        return response
