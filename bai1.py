"""
BÀI 1: CLI Agent đơn giản với chat loop
"""
from google.genai import types
from common import Config, GoogleAIService

SYSTEM_PROMPT = "Bạn là trợ lý AI đa năng: trả lời trực tiếp, đúng trọng tâm, an toàn, không bịa, và tối ưu độ dài để không vượt giới hạn token."


class ChatService(GoogleAIService):
    def chat(self, message: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {message}",
            config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=1000)
        )
        return response.text.strip() if response.text else "Không thể trả lời."


def main():
    print("BÀI 1: SIMPLE CHAT AGENT")
    print("Gõ 'exit' để thoát\n")
    
    Config.validate()
    chat = ChatService(Config.GOOGLE_API_KEY, Config.GOOGLE_MODEL)
    
    while True:
        try:
            user_input = input("Bạn: ").strip()
            if user_input.lower() in ['exit', 'quit']: break
            if not user_input: continue
            
            Config.reload()
            chat.reload_api_key(Config.GOOGLE_API_KEY)
            
            print(f"Bot: {chat.chat(user_input)}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Lỗi: {e}\n")


if __name__ == "__main__":
    main()
