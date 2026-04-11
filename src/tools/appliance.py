from langchain.tools import tool
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
@tool
def read_specific_appliance_manual(appliance_name: str) -> str:
    """
    当且仅当客人询问【具体电器设施】（如洗衣机，取暖器，智能马桶）怎么使用时，调用此工具。
    参数appliance_name必须是经过大脑判断后的标准ID。
    **可用的标准ID**：
    heater(房间内取暖器)
    washlet(智能马桶)
    washmachine(洗衣机)
    NE(其他所有电器设施,暂时还未添加以NE表示)
    """

    print(f"\n[决策分支1] 客人询问特定电器，激活说明书加载模块：{appliance_name}")

    trusted_appliances_map = {
        "washmachine": "washmachine.md",
        "heater": "heater.md",
        "washlet": "washlet.md"
    }

    file_name = trusted_appliances_map.get(appliance_name)

    if not file_name:
        return "客人询问的电器不存在于我的知识库中。请回复客人，对不起关于该电器的使用方法请咨询民宿员工。"
    
    file_path = PROJECT_ROOT/"data"/"processed"/file_name

    if not file_path.exists():
        return f"错误：本地文件{file_name}不存在，请检查系统配置"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    strict_instruction = f"""
        =========================================
        **极其重要的系统强制指令 (System Override)**
        以上是 {appliance_name} 的说明书。
        你在回答客人时，必须严格遵守以下规则：
        1. 说明书中出现的所有类似 [IMAGE:xxx] 的图片标签，是极其重要的前端交互按钮。
        2. 你在回答中，必须**原封不动**地保留并输出这些 [IMAGE:xxx] 标签，绝对不能省略、修改或翻译它们！
        3. 请把这些标签自然地穿插在你的步骤说明中。
        =========================================
    """
    return content + strict_instruction