# middleware/request_logging_middleware.py

import time
from django.utils.deprecation import MiddlewareMixin
import logging



class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None, *args, **kwargs):
        self.get_response = get_response
        self.logger = logging.getLogger('django.request')
        super().__init__(get_response, *args, **kwargs)

    def __call__(self, request):
        start_time = time.time()
        try:
            response = self.get_response(request)
        except Exception as e:
            duration = time.time() - start_time
            # Log the error details
            self.logger.error(
                f"Endpoint: {request.path}, Method: {request.method}, "
                f"Error: {str(e)}, Duration: {duration:.2f}s",
                exc_info=True  # Include traceback in log
            )
            # Return a generic error response or handle it as needed
            from django.http import HttpResponseServerError
            return HttpResponseServerError("Internal Server Error")

        duration = time.time() - start_time

        # Log the request and response details
        self.logger.info(
            f"Endpoint: {request.path}, Method: {request.method}, "
            f"Response Status: {response.status_code}, Duration: {duration:.2f}s"
        )

        return response
