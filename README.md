# Dual Memory Companion System (雙軌記憶陪伴系統)

這是一個專為陪伴機器人設計的雙軌記憶對話系統。系統結合了短期上下文記憶（Vector Database）與長期個人事實記憶（Graph Database），旨在提供具備持續性、關懷感且能記住使用者習慣的自然對話體驗。

## 系統架構 (Architecture)

本系統採用雙資料庫架構來模擬人類大腦的記憶機制：
* **短期記憶 (Short-term Memory)：** 使用 **ChromaDB** (本地向量資料庫) 儲存近期的對話片段，透過語意搜尋提供對話的上下文。
* **長期記憶 (Long-term Memory)：** 使用 **Neo4j** (圖形資料庫) 儲存關鍵的個人事實（如喜好、健康狀況、人際關係）。系統會透過結構化 LLM 在背景自動分析對話並提取長期記憶。
* **核心模型 (LLM)：** 採用 **Google Gemini 1.5 Pro** 處理對話生成與記憶決策。

## 專案結構 (Directory Structure)

```text
Dual_Memory/
├── .env                  # 環境變數設定檔 (API Keys, DB Credentials)
├── .gitignore            # Git 忽略清單
├── README.md             # 專案說明文件
├── chroma_db/            # ChromaDB 本地持久化資料夾 (自動生成)
└── src/
    ├── config.py         # 環境變數與資料庫連線初始化
    ├── memory_engine.py  # 記憶檢索與寫入引擎 (Chroma & Neo4j 操作)
    ├── prompts.py        # 系統提示詞與角色設定管理
    ├── chatbot_core.py   # 聊天代理人核心邏輯與事實提取
    └── test_connection.py# 基礎連線測試腳本
```

## 安裝與環境設定 (Setup)
1. 安裝依賴套件 (Requirements)：
    ### 請確保已安裝以下主要套件（建議使用虛擬環境）：

```Bash
pip install langchain langchain-google-genai langchain-neo4j langchain-chroma pydantic python-dotenv neo4j
```

2. 環境變數設定 (.env)：
    ### 在專案根目錄建立 .env 檔案，並填入以下資訊：

```
# Google Gemini API
GOOGLE_API_KEY="your_google_api_key_here"

# Neo4j Graph Database
NEO4J_URI="neo4j+s://your_database_uri"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your_neo4j_password"
NEO4J_DATABASE="neo4j"
```

## 使用方式 (Usage)
1. 測試資料庫連線：
##### 確保 Neo4j 連線正常。
```Bash
python -m src.test_connection
```
2. 啟動對話測試：
##### 執行核心腳本進行簡單的對話與記憶寫入測試。
```Bash
python -m src.chatbot_core
```

## 未來展望與優化方向 (Future Work)
- 將長期記憶提取機制改為非同步執行 (Async Background Task) 以降低回應延遲。
- 實作更動態的圖形資料庫 Cypher 查詢邏輯（動態實體提取）。
- 加入短期記憶的定期摘要與遺忘機制。