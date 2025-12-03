from django.shortcuts import render

# notifications/views.py
from django.http import JsonResponse
from django.views import View
import json

class ChatAPI(View):
    def get(self, request):
        return JsonResponse({"message": "Hello from ChatAPI!"})

    def post(self, request):
        try:
            data = json.loads(request.body)
            user_input = data.get("input", "")
        except json.JSONDecodeError:
            user_input = ""

        # هنا تحط المنطق اللي كنت هتستخدمه للـ chat
        response_text = f"You said: {user_input}"

        return JsonResponse({"response": response_text})
