import os
import openai
import tiktoken
import json
from datetime import datetime
import streamlit as st

DEFAULT_API_KEY = os.environ.get("TOGETHER_API_KEY")
DEFAULT_BASE_URL = "https://api.together.xyz/v1"
DEFAULT_MODEL = "meta-llama/Llama-3-8b-chat-hf"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 512
DEFAULT_TOKEN_BUDGET = 4096
class ConversationManager:
    def __init__(self):
        self.conversation_history = []
        self.persona = "Default"
        self.custom_system_message = None
        self.api_key = DEFAULT_API_KEY
        self.base_url = DEFAULT_BASE_URL
        self.model = DEFAULT_MODEL
        self.temperature = DEFAULT_TEMPERATURE
        self.max_tokens = DEFAULT_MAX_TOKENS
        self.token_budget = DEFAULT_TOKEN_BUDGET

    def set_persona(self, persona):
        self.persona = persona
        self.custom_system_message = None

    def set_custom_system_message(self, message):
        self.custom_system_message = message

    def chat_completion(self, user_input, temp=None, max_tokens=None, total_max_tokens=None):
        if temp is None:
            temp = self.temperature
        if max_tokens is None:
            max_tokens = self.max_tokens
        if total_max_tokens is None:
            total_max_tokens = self.token_budget

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "prompt": user_input,
            "temperature": temp,
            "max_tokens": max_tokens
        }

        response = openai.Completion.create(
            engine=self.model,
            prompt=user_input,
            temperature=temp,
            max_tokens=max_tokens
        )

        return response.choices[0].text.strip()

    def reset_conversation_history(self):
        self.conversation_history = []

# Example usage:
# chat_manager = ConversationManager()
# chat_manager.set_persona("Friendly")
# response = chat_manager.chat_completion("Hello!", 0.7, 150, 2000)
# print(response)