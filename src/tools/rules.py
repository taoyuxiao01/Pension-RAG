import os
from pathlib import Path

from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "bge-m3")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@tool
def search_house_rules_vector_db(query: str) -> str:
    """
    当客人询问白马民宿的入住规则、垃圾分类、雪板存放、退房时间等〖非电器类〗杂项规定时，调用此工具。
    参数 query 是客人问题的核心关键词的中文。
    """
    print(f"\n[决策分支2] 客人询问民宿规则，激活向量检索模块（RAG），搜索词：{query}")

    db_dir = PROJECT_ROOT / "data" / "vector_db" / "house_rules"

    if not db_dir.exists():
        return "严重错误：向量数据库不存在"

    embeddings = OllamaEmbeddings(
        model=OLLAMA_EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    vector_store = Chroma(
        persist_directory=str(db_dir),
        embedding_function=embeddings,
    )

    docs = vector_store.similarity_search(query=query, k=2)

    if not docs:
        return "未在数据库中找到相关规则。"

    result = "找到以下相关民宿规则片段（仅供提炼）：\n\n"

    for i, doc in enumerate(docs):
        result += f"[规则片段{i + 1}]：\n{doc.page_content}\n\n"

    print(f"[RAG检索完毕] 成功捞出 {len(docs)} 个知识片段。")
    print(result)

    return result