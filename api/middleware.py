import logging
import traceback
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Logger l'erreur complète
        error_details = {
            'error_type': type(exception).__name__,
            'error_message': str(exception),
            'traceback': traceback.format_exc(),
            'request_path': request.path,
            'request_method': request.method,
            'request_data': request.POST if request.method == 'POST' else request.GET,
        }

        logger.error(f"Erreur détaillée: {error_details}")
        print(f"=== ERREUR DÉTAILLÉE ===")
        print(f"Type: {error_details['error_type']}")
        print(f"Message: {error_details['error_message']}")
        print(f"Traceback: {error_details['traceback']}")
        print(f"Path: {error_details['request_path']}")
        print(f"Method: {error_details['request_method']}")
        print(f"Data: {error_details['request_data']}")
        print(f"========================")

        if settings.DEBUG:
            return JsonResponse({
                'error': str(exception),
                'traceback': traceback.format_exc(),
                'type': type(exception).__name__
            }, status=500)

        return None
