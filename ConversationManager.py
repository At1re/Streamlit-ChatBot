import os
import openai
from dotenv import load_dotenv

class ConversationManager:
    def __init__(self):
        load_dotenv()  # Load environment variables from a .env file if present
        self.conversation_history = []
        self.persona = "Default"
        self.custom_system_message = None
        self.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for API key
        print(f"API Key: {self.api_key}")  # Add this line to verify the API key is loaded
        self.model = "text-davinci-003"  # Use "text-davinci-003" for GPT-3.5
        self.temperature = 0.7
        self.max_tokens = 512
        self.token_budget = 4096

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

        openai.api_key = self.api_key

        self.conversation_history.append({"role": "user", "content": user_input})

        # Limit history length
        conversation_context = self.conversation_history[-(total_max_tokens // max_tokens):]

        # Prepare prompt for OpenAI
        prompt = self.custom_system_message or f"You are a {self.persona} assistant.\n"
        for message in conversation_context:
            prompt += f"{message['role']}: {message['content']}\n"
        prompt += f"user: {user_input}\nassistant:"

        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                temperature=temp,
                max_tokens=max_tokens,
                n=1,
                stop=None
            )
            ai_response = response.choices[0].text.strip()
        except Exception as e:
            ai_response = f"Error: {str(e)}"

        self.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response

    def reset_conversation_history(self):
        self.conversation_history = []

# Example usage:
# chat_manager = ConversationManager()
# chat_manager.set_persona("Friendly")
# response = chat_manager.chat_completion("Hello!", 0.7, 150, 2000)
# print(response)
