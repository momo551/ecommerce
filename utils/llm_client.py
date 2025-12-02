import time
from litellm import LiteLLM, APIError
from django.conf import settings

class ResilientLiteLLM:
    """
    Wrapper حول LiteLLM مع retry تلقائي على overloaded channels.
    يدعم chat, complete, generate_image وأي method أخرى.
    """
    def __init__(self, max_retries=5, base_delay=2):
        self.client = LiteLLM(api_key=settings.LITELLM_API_KEY)
        self.max_retries = max_retries
        self.base_delay = base_delay

    def _call_with_retry(self, method_name, *args, **kwargs):
        for attempt in range(1, self.max_retries + 1):
            try:
                method = getattr(self.client, method_name)
                return method(*args, **kwargs)
            except APIError as e:
                if "overloaded" in str(e).lower():
                    delay = self.base_delay * (2 ** (attempt - 1))
                    print(f"[Attempt {attempt}] Channel overloaded. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    raise e
        raise Exception(f"Failed after {self.max_retries} retries due to overloaded channel.")

    # Methods
    def chat(self, prompt, **kwargs):
        return self._call_with_retry("chat", prompt, **kwargs)

    def complete(self, prompt, **kwargs):
        return self._call_with_retry("complete", prompt, **kwargs)

    def generate_image(self, prompt, **kwargs):
        return self._call_with_retry("generate_image", prompt, **kwargs)
