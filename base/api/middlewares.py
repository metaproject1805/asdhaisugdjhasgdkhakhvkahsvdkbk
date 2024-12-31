# middleware/request_logging_middleware.py

import time
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import logging
from .jobs.investment_job import accumulate_investment
from .jobs.user_job import daily_profile_update
from django.conf import settings
from datetime import date
from ..models import SystemState



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
    

class DailyRunMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = logging.getLogger('daily_task')
        # Check if DEBUG is False        
        system_state, created = SystemState.objects.get_or_create(key="daily_task")

        today = date.today()

        # Check if the task has already run today
        if system_state.last_run_date != today:
            try:
                accumulate_investment() 
                daily_profile_update()
            
                system_state.last_run_date = today
                system_state.save()
                logger.info("Daily task completed successfully.")
            except Exception as e:
                logger.info(f"Daily task failed: {e}")
                system_state.last_run_date = today
                system_state.save()

        response = self.get_response(request)

        return response