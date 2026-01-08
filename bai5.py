"""
BÀI 5: Planner → Executor Pipeline
"""
import json
import re
from typing import List, Dict, Any
from dataclasses import dataclass, field
from google.genai import types
from common import Config, GoogleAIService

PLANNER_PROMPT = """Bạn là chuyên gia lập kế hoạch. Chia nhỏ yêu cầu thành các bước đơn giản.
Trả về JSON: {"steps": ["bước 1", "bước 2", ...]}"""


@dataclass
class StepResult:
    step: str
    result: str
    success: bool = True


@dataclass
class AgentState:
    input: str
    plan: List[str] = field(default_factory=list)
    past_steps: List[StepResult] = field(default_factory=list)
    current_step: int = 0


class PlanningService(GoogleAIService):
    def create_plan(self, user_input: str) -> Dict[str, Any]:
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{PLANNER_PROMPT}\n\nYêu cầu: {user_input}",
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1000,
                response_mime_type="application/json"
            )
        )
        
        text = response.text.strip() if response.text else "{}"
        
        # Clean markdown
        if text.startswith("```"): text = text[7:] if text.startswith("```json") else text[3:]
        if text.endswith("```"): text = text[:-3]
        text = text.strip()
        
        try:
            data = json.loads(text)
        except:
            # Fallback
            data = {"steps": [f"Xử lý: {user_input}", "Thực hiện", "Trả lời"]}
        
        return data if "steps" in data else {"steps": [f"Xử lý: {user_input}"]}
    
    def execute_step(self, step: str) -> str:
        return f"✓ Hoàn thành: {step}"
    
    def synthesize(self, user_input: str, steps: List[StepResult]) -> str:
        summary = "\n".join([f"- {s.step}: {s.result}" for s in steps])
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"Tổng hợp và trả lời:\n\nCâu hỏi: {user_input}\n\nĐã thực hiện:\n{summary}",
            config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=1000)
        )
        return response.text.strip() if response.text else "Đã hoàn thành."


class PlanningAgent:
    def __init__(self, service: PlanningService):
        self.service = service
    
    def run(self, user_input: str) -> str:
        state = AgentState(input=user_input)
        
        # Planner
        print("Đang lập kế hoạch...")
        plan_data = self.service.create_plan(user_input)
        state.plan = plan_data["steps"]
        
        print("\nKế hoạch:")
        for i, step in enumerate(state.plan, 1):
            print(f"  {i}. {step}")
        
        # Executor
        print("\nĐang thực hiện...")
        for step in state.plan:
            result = self.service.execute_step(step)
            state.past_steps.append(StepResult(step=step, result=result))
            print(f"  {result}")
        
        # Synthesize
        print("\nĐang tổng hợp...")
        return self.service.synthesize(user_input, state.past_steps)


def main():
    print("BÀI 5: PLANNING AGENT")
    print("Gõ 'exit' để thoát\n")
    
    Config.validate()
    service = PlanningService(Config.GOOGLE_API_KEY, Config.GOOGLE_MODEL)
    agent = PlanningAgent(service)
    
    while True:
        try:
            user_input = input("Bạn: ").strip()
            if user_input.lower() in ['exit', 'quit']: break
            if not user_input: continue
            
            Config.reload()
            service.reload_api_key(Config.GOOGLE_API_KEY)
            
            print()
            result = agent.run(user_input)
            print(f"\nKết quả:\n{result}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Lỗi: {e}\n")


if __name__ == "__main__":
    main()
