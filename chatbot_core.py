# 修改後的 chatbot_core.py 片段
from config import llm
from memory_engine import MemoryEngine
from prompts import get_chat_prompt  # 引入剛寫好的提示詞模組

class ChatAgent:
    def __init__(self):
        print("⚙️ 正在啟動雙軌記憶系統...")
        self.memory = MemoryEngine()
        
    def chat(self, user_input):
        print("🔍 正在大腦中檢索相關記憶...")
        st, lt = self.memory.get_combined_context(user_input)
        
        # 使用獨立出來的 prompt 函數
        prompt = get_chat_prompt(st, lt, user_input)
        
        print("🧠 正在思考回覆...")
        response = llm.invoke(prompt)
        ai_reply = response.content
        
        # 儲存記憶
        new_memory = f"長輩說：{user_input}。系統回覆：{ai_reply}"
        self.memory.add_short_term(new_memory)
        
        return ai_reply