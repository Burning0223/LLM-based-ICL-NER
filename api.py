import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
API_REGISTRY={
    "deepseek-flash":{"api_key":'DEEPSEEK_API_KEY',
                    "base_url":"https://api.deepseek.com",
                    "model":"deepseek-flash"},
    "openrouter":{"api_key":'OPENROUTER_API_KEY',
                "base_url":"https://openrouter.ai/api/v1",
                "model":"openrouter/free"},
    "DeepSeek-V4.1-Flash":{"api_key":'GUOCHAN_API_KEY',
                        "base_url":"http://tuluo.top:8000/v1",
                        "model":"DeepSeek-V4.1-Flash"},
    "Qwen3.8-27B":{"api_key":'GUOCHAN_API_KEY',
                    "base_url":"http://tuluo.top:8000/v1",
                    "model":"Qwen3.8-27B"},
    "gpt-5.6-luna":{"api_key":'GPT_API_KEY',
                    "base_url":"http://tuluo.top:8000/v1",
                    "model":"gpt-5.6-luna"},
    "glm-5.3-flash":{"api_key":'GUOCHAN_API_KEY',
                    "base_url":"http://tuluo.top:8000/v1",
                    "model":"glm-5.3-flash"}
}
class APIClient:
    def __init__(self,api_name,temperature):
        self.config=API_REGISTRY[api_name]
        self.client=OpenAI(
                    api_key=os.environ.get(self.config["api_key"]),
                    base_url=self.config["base_url"])
        self.temperature=temperature
    def generate(self,prompt):
        response=self.client.chat.completions.create(
                    model=self.config["model"],
        messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
                ],
        temperature=self.temperature,
        response_format={"type": "json_object"}
        )

        return response.choices[0].message.content