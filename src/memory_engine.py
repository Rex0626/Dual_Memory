import uuid
from src.config import graph, embeddings, llm
from langchain_chroma import Chroma

# 1. 初始化本地向量庫
vector_db = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embeddings,
    collection_name="short_term_store"
)

class MemoryEngine:
    def __init__(self):
        self.graph = graph
        self.vector_db = vector_db

    def add_short_term(self, text):
        """存入對話片段到向量庫"""
        self.vector_db.add_texts(texts=[text], metadatas=[{"id": str(uuid.uuid4())}])
        print(f"DEBUG: 已存入向量庫 -> {text[:20]}...")

    def add_long_term(self, entity, relation, target):
        """存入事實到圖形庫"""
        query = (
            f"MERGE (e:Entity {{name: '{entity}'}}) "
            f"MERGE (t:Target {{name: '{target}'}}) "
            f"MERGE (e)-[:{relation}]->(t)"
        )
        self.graph.query(query)
        print(f"DEBUG: 已存入圖形庫 -> ({entity})-[{relation}]->({target})")

    def get_combined_context(self, query):
        """混合檢索測試"""
        # 向量搜尋
        docs = self.vector_db.similarity_search(query, k=1)
        st_context = docs[0].page_content if docs else "無相關短期記憶"
        
        # 圖形搜尋 (查詢與 '使用者' 相關的所有事實)
        graph_data = self.graph.query(
            "MATCH (e:Entity {name: '使用者'})-[r]->(t) RETURN type(r) as rel, t.name as val"
        )
        lt_context = ", ".join([f"{d['rel']}: {d['val']}" for d in graph_data])
        
        return st_context, lt_context

if __name__ == "__main__":
    engine = MemoryEngine()
    
    # 測試寫入
    engine.add_short_term("使用者昨天說他關節痛，心情很沮喪")
    engine.add_long_term("使用者", "喜歡吃", "粥歡喜")
    
    # 測試檢索
    st, lt = engine.get_combined_context("肚子餓且心情不好")
    print(f"\n檢索結果：\n短期：{st}\n長期：{lt}")