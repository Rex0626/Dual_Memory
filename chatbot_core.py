from config import llm
from memory_engine import MemoryEngine

class ChatAgent:
    """處理 RAG 對話生成的代理人"""
    def __init__(self):
        print("⚙️ 正在啟動雙軌記憶系統...")
        self.memory = MemoryEngine()
        
    def chat(self, user_input):
        print("🔍 正在大腦中檢索相關記憶...")
        # 1. 檢索 (Retrieval)：利用使用者的輸入去匹配記憶
        st, lt = self.memory.get_combined_context(user_input)
        
        # 2. 生成 (Generation)：建構 RAG 專用的 Prompt
        prompt = f"""
        你是一個具備同理心、負責照顧長輩的陪伴 AI，代號為 Project A.L.I.C.E.。
        請根據以下從資料庫提取的「背景記憶」以及使用者的「最新對話」，給出自然、溫暖的回覆。
        請表現得像家人一樣，不要像冷冰冰的客服或 AI 助理。

        【短期記憶 (近期的對話與情緒)】: 
        {st}
        
        【長期事實 (長輩的喜好與常識)】: 
        {lt}

        【長輩現在說】：{user_input}

        請直接給予回覆：
        """
        
        print("🧠 正在思考回覆...")
        response = llm.invoke(prompt)
        ai_reply = response.content
        
        # 3. 儲存 (Storage)：將這次的互動存入短期記憶，供未來檢索
        new_memory = f"長輩說：{user_input}。系統回覆：{ai_reply}"
        self.memory.add_short_term(new_memory)
        
        return ai_reply

# --- 終端機對話介面 ---
if __name__ == "__main__":
    agent = ChatAgent()
    
    print("\n========================================")
    print(" 啟動成功！現在可以開始對話了 (輸入 'quit' 離開)")
    print("========================================\n")
    
    while True:
        user_text = input("👤 你：")
        if user_text.lower() == 'quit':
            print("👋 系統已關閉。")
            break
            
        if not user_text.strip():
            continue
            
        reply = agent.chat(user_text)
        print(f"\n🤖 A.L.I.C.E.：{reply}\n")
        print("-" * 40)