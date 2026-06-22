import json
from pydantic import BaseModel, Field
from typing import Optional, List
from src.config import llm
from src.memory_engine import MemoryEngine
from src.prompts import get_chat_prompt

# 定義結構化輸出的資料格式，用於長期記憶提取
class FactModel(BaseModel):
    has_fact: bool = Field(description="對話中是否包含值得永久記住的長輩個人事實、喜好、健康狀況或重要行程")
    entity: Optional[str] = Field(None, description="主體，通常是 '使用者'、'長輩' 或特定的親友名字")
    relation: Optional[str] = Field(None, description="關係動作，例如 '喜歡吃'、'對...過敏'、'下週要去'")
    target: Optional[str] = Field(None, description="客體或目標，例如 '粥歡喜'、'芒果'、'醫院看診'")

class ChatAgent:
    def __init__(self):
        print("⚙️ 正在啟動雙軌記憶系統...")
        self.memory = MemoryEngine()
        # 建立一個專門用來提取事實的結構化 LLM 物件
        self.extractor_llm = llm.with_structured_output(FactModel)
        
    def chat(self, user_input):
        print("🔍 正在大腦中檢索相關記憶...")
        try:
            st, lt = self.memory.get_combined_context(user_input)
        except Exception as e:
            print(f"⚠️ 記憶檢索失敗: {e}，將使用空白背景繼續對話。")
            st, lt = "無相關短期記憶", ""
        
        # 使用獨立出來的 prompt 函數
        prompt = get_chat_prompt(st, lt, user_input)
        
        print("🧠 正在思考回覆...")
        try:
            response = llm.invoke(prompt)
            ai_reply = response.content
        except Exception as e:
            print(f"❌ LLM 呼叫失敗: {e}")
            return "阿布（AI）現在頭暈暈的，可能網絡有些不聽話。但我一直在聽，您剛剛說什麼呢？"
        
        # 1. 儲存短期記憶（原有機制）
        new_memory = f"長輩說：{user_input}。系統回覆：{ai_reply}"
        try:
            self.memory.add_short_term(new_memory)
        except Exception as e:
            print(f"⚠️ 短期記憶寫入失敗: {e}")
        
        # 2. 自動觸發長期記憶提取與寫入（新增優化）
        self._auto_extract_long_term_fact(user_input, ai_reply)
        
        return ai_reply

    def _auto_extract_long_term_fact(self, user_input, ai_reply):
        """後台或同步提取長期事實並寫入圖形資料庫"""
        print("💡 正在分析是否有值得記住的長期事實...")
        extract_prompt = f"""
        請分析以下對話，評估其中是否包含關於「長輩（使用者）」的長期重要事實（例如喜好、禁忌、健康狀況、重要日常行程或人際關係）。
        
        長輩說：{user_input}
        AI回覆：{ai_reply}
        """
        try:
            # 呼叫結構化 LLM 進行分析
            fact_result = self.extractor_llm.invoke(extract_prompt)
            
            # 如果發現有價值的事實，則自動寫入 Neo4j
            if fact_result.has_fact and fact_result.entity and fact_result.relation and fact_result.target:
                print(f"🎯 偵測到新事實！嘗試寫入圖形庫...")
                self.memory.add_long_term(
                    entity=fact_result.entity,
                    relation=fact_result.relation,
                    target=fact_result.target
                )
            else:
                print("ℹ️ 本次對話未偵測到新的長期事實。")
        except Exception as e:
            print(f"⚠️ 長期記憶自動提取或寫入時發生錯誤: {e}")

if __name__ == "__main__":
    # 簡單測試優化後的代理人
    agent = ChatAgent()
    reply = agent.chat("我肚子好餓喔，等一下想去買粥歡喜的皮蛋瘦肉粥來吃。")
    print(f"\nAI 回覆：{reply}")