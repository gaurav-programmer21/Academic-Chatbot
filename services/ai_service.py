from typing import List, Dict
from openai import OpenAI
from google import genai

class AIService:
    def __init__(self, config):
        self.openai_api_key = config.get("OPENAI_API_KEY")
        self.gemini_api_key = config.get("GEMINI_API_KEY")

        if not self.openai_api_key and not self.gemini_api_key:
            raise RuntimeError("No AI API keys configured")

        self.openai_client = None
        self.gemini_client = None

        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)

        if self.gemini_api_key:
            self.gemini_client = genai.Client(api_key=self.gemini_api_key)

    def generate_response(
        self,
        message: str,
        history: List[Dict],
        knowledge: List[Dict],
        model: str = "openai",
    ) -> str:
        context = self._build_context(history, knowledge)
        prompt = f"{context}\n\nUser Question: {message}"

        if model == "openai":
            return self._openai_response(prompt)
        elif model == "gemini":
            return self._gemini_response(prompt)
        else:
            raise ValueError(f"Unknown model: {model}")

    def _build_context(self, history: List[Dict], knowledge: List[Dict]) -> str:
        context = "You are an academic AI assistant. Help students clearly and accurately.\n\n"

        if knowledge:
            context += "Knowledge Base:\n"
            for item in knowledge[-5:]:
                context += f"- {item.get('topic')}: {item.get('content')}\n"
            context += "\n"

        if history:
            context += "Recent Conversation:\n"
            for msg in history[-5:]:
                context += f"{msg.get('role', 'user').capitalize()}: {msg.get('content')}\n"

        return context

    def _openai_response(self, prompt: str) -> str:
        if not self.openai_client:
            return "OpenAI is not configured"

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful academic assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {e}"

    def _gemini_response(self, prompt: str) -> str:
        if not self.gemini_client:
            return "Gemini is not configured"

        try:
            response = self.gemini_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"