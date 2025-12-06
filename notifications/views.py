from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .services import process_chat_input

@method_decorator(csrf_exempt, name='dispatch')
class ChatAPI(View):
    """
    API view for handling chat interactions.
    """

    def get(self, request):
        """
        Handle GET requests to the chat API.
        """
        return JsonResponse({"message": "Hello from ChatAPI!"})

    def post(self, request):
        """
        Handle POST requests to the chat API.
        """
        try:
            data = json.loads(request.body)
            user_input = data.get("input", "")
        except json.JSONDecodeError:
            user_input = ""

        response_text = process_chat_input(user_input)

        return JsonResponse({"response": response_text})
