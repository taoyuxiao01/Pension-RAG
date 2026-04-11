from langchain.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def query_hakuba_weather(resort_name: str = "general") -> str:
    """
    当客人群问白马村天气，降雪量，风速或者雪场能见度时调用此工具。
    参数resort_name限定为雪场英文名，共有10个候选，分别为Jigatake，Kashimayari，Sanosaka，Goryu, 47, Happo, Iwatake, Tsugaike, Norikura, Cortina
    如果没有具体指定雪场，或只是问“白马天气怎么样”时，传入参数‘general’
    """

    print(f"[决策分支]激活天气爬虫工具，目标{resort_name}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    resort_slugs = {
        "jigatake": "detail_jiigatake",
        "kashimayari": "detail_kashimayari",
        "sanosaka": "detail_sanosaka",
        "goryu": "detail_goryu",
        "47": "detail_hakuba47",
        "happo": "detail_happo",
        "iwatake": "detail_iwatake",
        "tsugaike": "detail_tsugaike",
        "norikura": "detail_norikura",
        "cortina": "detail_cortina"
    }

    target_slug = resort_slugs.get(resort_name.lower())
    if resort_name.lower() == "general" or not target_slug:
        url = "https://www.hakubavalley.com/weather/"
    else:
        url = f"https://www.hakubavalley.com/weather/{target_slug}/"

    print(url)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            element.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        final_text = clean_text[:1500]
        result = f"这是从 {url} 抓取到的最新网页数据（已清洗）：\n\n{final_text}\n\n"
        result += "🚨 系统指令：请像一个专业的滑雪向导一样，从上面的杂乱文本中提取出【当前天气、气温、降雪量、风速】等核心指标，并用极其自然、热情的语气回答客人。如果数据缺失，请直接告知客人。"
        return result
    
    except requests.exceptions.Timeout:
        return "抱歉，天气网站响应超时。请提示客人稍后再试，或查看窗外实况。"
    except Exception as e:
        return f"抱歉，天气接口抓取失败（错误码：{str(e)}）。请提示客人前往前台观看电子天气大屏。"
