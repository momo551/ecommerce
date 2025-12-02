from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from utils.llm_client import ResilientLiteLLM

llm = ResilientLiteLLM()

class ChatAPI(View):
    def post(self, request):
        prompt = request.POST.get('prompt', '')
        if not prompt:
            return JsonResponse({'error': 'الرجاء إدخال نص.'}, status=400)

        try:
            response = llm.chat(prompt)
        except Exception as e:
            response = f"حدث خطأ أثناء الاتصال بـ LLM: {str(e)}"

        return JsonResponse({'prompt': prompt, 'response': response})
