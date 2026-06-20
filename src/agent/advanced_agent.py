import os
import uuid

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from src.tools.appliance import read_specific_appliance_manual
from src.tools.rules import search_house_rules_vector_db
from src.tools.shuttle_logic import find_best_shuttle
from src.tools.weather import query_hakuba_weather

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen3.5:9b-q4_K_M")

def run_hakuba_agent():
    tools = [read_specific_appliance_manual, search_house_rules_vector_db, find_best_shuttle, query_hakuba_weather]

    llm = ChatOllama(
        model=OLLAMA_CHAT_MODEL,
        temperature=0,
        base_url=OLLAMA_BASE_URL,
    )

    system_prompt = """你是一个白马（Hakuba）滑雪民宿的专业AI管家，你的任务是解答客人的问题。
    【回答风格要求】(极其重要)：
    1. **精准提炼，拒绝全文背诵**：绝不能把整篇说明书复制粘贴出来！客人问什么，你就只回答什么。例如客人问“怎么用洗衣机”，你只需要提炼出“洗涤步骤”即可，**绝对不要**主动列出“故障代码”或“按键图鉴”！
    2. **严格按照民宿规则内容回答**： 关于民宿规则的提问必须与本民宿规则一致。
    3. **口语化服务**：用自然、热情的语气回答，像真人在服务一样。
    
    =========================================
    **绝对指令：语言镜像协议 (Language Mirroring Protocol)**
    1. 你必须首先识别客人最后一次提问所使用的语言（如：英语、日语、中文）。
    2. 你最终输出的回答，【必须 100% 使用与客人相同的语言】！
    3. 即使你查阅的说明书或工具返回的结果是中文，你也必须在脑海中将其翻译成客人的语言后再输出。
    4. 如果客人用英文问，你绝不能出现任何中文字符；如果客人用日文问，必须用纯正日语回复！
    =========================================

    """

    memory = MemorySaver()

    agent_app = create_agent(
        model = llm, 
        tools = tools, 
        system_prompt= system_prompt,
        checkpointer=memory
    )

    return agent_app

if __name__ == "__main__":
    print("白马民宿智能助手上线！")
    print("-" * 50)
    
    steward = run_hakuba_agent()

    test_thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": test_thread_id}}
    
    while True:
        user_input = input("\n 客人提问 (quit退出): ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        print("\n 决策中...")
        
        inputs = {"messages": [("user", user_input)]}
        
        # 使用 invoke 同步模式方便看 X 光全过程
        result = steward.invoke(inputs, config=config)
        
        print("\n" + "="*50)
        print("助手最终回复:")
        print(result["messages"][-1].content)
        print("="*50)
        
        # 调试核心：看决策链条
        print("\n[开发者透视镜 - 分支决策链]")
        for msg in result["messages"]:
            if msg.type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
                print(f"   AI决定调用工具: {msg.tool_calls[0]['name']}")
                print(f"    参数: {msg.tool_calls[0]['args']}")
            elif msg.type == "tool":
                status = " 成功加载文件/RAG数据" if not msg.content.startswith("error") else " 工具内部拒绝/报错"
                print(f"   工具返回状态: {status}")