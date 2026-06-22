from src.config import graph

def test_neo4j():
    try:
        # 執行一個簡單的 Cypher 查詢
        result = graph.query("RETURN 'Connection Successful!' as message")
        print(f"🚀 Neo4j 狀態: {result[0]['message']}")
        
        # 試著建立一個測試節點
        graph.query("MERGE (t:TestNode {name: 'Alice_Connection_Test'})")
        print("📝 測試節點已成功寫入雲端。")
        
    except Exception as e:
        print(f"❌ 連線失敗: {e}")

if __name__ == "__main__":
    test_neo4j()