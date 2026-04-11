import datetime
from langchain.tools import tool
import re

# Bus stop ( Key)
# Cortina, Satomi, Norikura, Tsugaike, Ochikura, Iwatake, JR_Hakuba, Happo_Terminal, Nakiyama, Echoland, Hakuba47, Goryu
stop = ["Cortina", "Satomi", "Norikura", "Tsugaike", "Ochikura", "Iwatake", "JR_Hakuba", "Happo_Terminal", "Nakiyama", "Echoland", "Hakuba47", "Goryu"]

# 1
SOUTHBOUND_RUNS = {
    1: {"Happo_Terminal": "07:31", "Nakiyama": "07:36", "Echoland": "07:44", "Hakuba47": "07:59", "Goryu": "08:06"},
    2: {"Tsugaike": "07:48", "Ochikura": "07:54", "Iwatake": "08:03", "Happo_Terminal": "08:11", "Nakiyama": "08:16", "Echoland": "08:24", "Hakuba47": "08:39", "Goryu": "08:46"},
    3: {"Cortina": "08:00", "Satomi": "08:08", "Norikura": "08:11", "Tsugaike": "08:18", "Ochikura": "08:24", "Iwatake": "08:33", "JR_Hakuba": "08:42", "Happo_Terminal": "08:48", "Nakiyama": "08:53", "Echoland": "09:01", "Hakuba47": "09:16", "Goryu": "09:23"},
    4: {"Tsugaike": "08:33", "Ochikura": "08:39", "Iwatake": "08:48", "Happo_Terminal": "08:56", "Nakiyama": "09:01", "Echoland": "09:09", "Hakuba47": "09:24", "Goryu": "09:31"},
    5: {"Cortina": "08:30", "Satomi": "08:38", "Norikura": "08:41", "Tsugaike": "08:48", "Ochikura": "08:54", "Iwatake": "09:03", "Happo_Terminal": "09:11", "Nakiyama": "09:16", "Echoland": "09:24", "Hakuba47": "09:39", "Goryu": "09:46"},
    6: {"Tsugaike": "09:18", "Ochikura": "09:24", "Iwatake": "09:33", "JR_Hakuba": "09:42", "Happo_Terminal": "09:48", "Nakiyama": "09:53", "Echoland": "10:01", "Hakuba47": "10:16", "Goryu": "10:23"},
    7: {"Cortina": "09:00", "Satomi": "09:08", "Norikura": "09:11", "Tsugaike": "09:18", "Ochikura": "09:24", "Iwatake": "09:33", "Happo_Terminal": "09:48", "Nakiyama": "09:53", "Echoland": "10:01", "Hakuba47": "10:16", "Goryu": "10:23"},
    8: {"Cortina": "09:30", "Satomi": "09:38", "Norikura": "09:41", "Tsugaike": "09:48", "Ochikura": "09:54", "Iwatake": "10:03", "Happo_Terminal": "10:11", "Nakiyama": "10:16", "Echoland": "10:24", "Hakuba47": "10:39", "Goryu": "10:46"},
    9: {"Cortina": "10:00", "Satomi": "10:08", "Norikura": "10:11", "Tsugaike": "10:18", "Ochikura": "10:24", "Iwatake": "10:33", "JR_Hakuba": "10:42", "Happo_Terminal": "10:48", "Nakiyama": "10:53", "Echoland": "11:01", "Hakuba47": "11:16", "Goryu": "11:23"},
    10: {"Tsugaike": "10:48", "Ochikura": "10:54", "Iwatake": "11:03", "Happo_Terminal": "11:11", "Nakiyama": "11:16", "Echoland": "11:24"},
    11: {"Cortina": "11:00", "Satomi": "11:08", "Norikura": "11:11", "Tsugaike": "11:18", "Ochikura": "11:24", "Iwatake": "11:33", "JR_Hakuba": "11:42", "Happo_Terminal": "11:48", "Nakiyama": "11:53", "Echoland": "12:01", "Hakuba47": "12:16", "Goryu": "12:23"},
    12: {"Tsugaike": "11:48", "Ochikura": "11:54", "Iwatake": "12:03", "Happo_Terminal": "12:11", "Nakiyama": "12:16", "Echoland": "12:24"},
    13: {"Cortina": "12:00", "Satomi": "12:08", "Norikura": "12:11", "Tsugaike": "12:18", "Ochikura": "12:24", "Iwatake": "12:33", "JR_Hakuba": "12:42", "Happo_Terminal": "12:48", "Nakiyama": "12:53", "Echoland": "13:01", "Hakuba47": "13:16", "Goryu": "13:23"},
    14: {"Tsugaike": "12:48", "Ochikura": "12:54", "Iwatake": "13:03", "Happo_Terminal": "13:11", "Nakiyama": "13:16", "Echoland": "13:24"},
    15: {"Cortina": "13:00", "Satomi": "13:08", "Norikura": "13:11", "Tsugaike": "13:18", "Ochikura": "13:24", "Iwatake": "13:33", "JR_Hakuba": "13:42", "Happo_Terminal": "13:48", "Nakiyama": "13:53", "Echoland": "14:01", "Hakuba47": "14:16", "Goryu": "14:23"},
    16: {"Tsugaike": "13:48", "Ochikura": "13:54", "Iwatake": "14:03", "Happo_Terminal": "14:11", "Nakiyama": "14:16", "Echoland": "14:24"},
    17: {"Cortina": "14:00", "Satomi": "14:08", "Norikura": "14:11", "Tsugaike": "14:18", "Ochikura": "14:24", "Iwatake": "14:33", "JR_Hakuba": "14:42", "Happo_Terminal": "14:48", "Nakiyama": "14:53", "Echoland": "15:01", "Hakuba47": "15:16", "Goryu": "15:23"},
    18: {"Tsugaike": "14:33", "Ochikura": "14:39", "Iwatake": "14:48", "Happo_Terminal": "14:56", "Nakiyama": "15:01", "Echoland": "15:09", "Hakuba47": "15:24", "Goryu": "15:31"},
    19: {"Cortina": "14:30", "Satomi": "14:38", "Norikura": "14:41", "Tsugaike": "14:48", "Ochikura": "14:54", "Iwatake": "15:03", "Happo_Terminal": "15:11", "Nakiyama": "15:16", "Echoland": "15:24", "Hakuba47": "15:39", "Goryu": "15:46"},
    20: {"Cortina": "14:45", "Satomi": "14:53", "Norikura": "14:56", "Tsugaike": "15:03", "Ochikura": "15:09", "Iwatake": "15:18", "Happo_Terminal": "15:26", "Nakiyama": "15:31", "Echoland": "15:39", "Hakuba47": "15:54", "Goryu": "16:01"},
    21: {"Tsugaike": "15:33", "Ochikura": "15:39", "Iwatake": "15:48", "Happo_Terminal": "15:56", "Nakiyama": "16:01", "Echoland": "16:09"},
    22: {"Cortina": "15:30", "Satomi": "15:38", "Norikura": "15:41", "Tsugaike": "15:48", "Ochikura": "15:54", "Iwatake": "16:03", "Happo_Terminal": "16:11", "Nakiyama": "16:16", "Echoland": "16:24", "Hakuba47": "16:39", "Goryu": "17:01"},
    23: {"Tsugaike": "16:03", "Ochikura": "16:09", "Iwatake": "16:18", "Happo_Terminal": "16:26", "Nakiyama": "16:31", "Echoland": "16:39", "Hakuba47": "16:54", "Goryu": "17:01"},
    24: {"Cortina": "16:00", "Satomi": "16:08", "Norikura": "16:11", "Tsugaike": "16:18", "Ochikura": "16:24", "Iwatake": "16:33", "JR_Hakuba": "16:42", "Happo_Terminal": "16:48", "Nakiyama": "16:53", "Echoland": "17:01", "Hakuba47": "17:16", "Goryu": "17:23"},
    25: {"Cortina": "16:30", "Satomi": "16:38", "Norikura": "16:41", "Tsugaike": "16:48", "Ochikura": "16:54", "Iwatake": "17:03", "Happo_Terminal": "17:11", "Nakiyama": "17:16", "Echoland": "17:24"},
    26: {"Tsugaike": "17:03", "Ochikura": "17:09", "Iwatake": "17:18", "Happo_Terminal": "17:26", "Nakiyama": "17:31", "Echoland": "17:39"},
    27: {"Cortina": "17:00", "Satomi": "17:08", "Norikura": "17:11", "Tsugaike": "17:18", "Ochikura": "17:24", "Iwatake": "17:33", "Happo_Terminal": "17:48"}
}

# 2
NORTHBOUND_RUNS = {
    1: {"Happo_Terminal": "07:10", "Iwatake": "07:18", "Ochikura": "07:27", "Tsugaike": "07:33", "Norikura": "07:40", "Satomi": "07:43", "Cortina": "07:51"},
    2: {"Happo_Terminal": "07:25", "Iwatake": "07:33", "Ochikura": "07:42", "Tsugaike": "07:48", "Norikura": "07:55", "Satomi": "07:58", "Cortina": "08:06"},
    3: {"Echoland": "07:27", "Nakiyama": "07:35", "Happo_Terminal": "07:40", "JR_Hakuba": "07:46", "Iwatake": "07:55", "Ochikura": "08:04", "Tsugaike": "08:10", "Norikura": "08:17", "Satomi": "08:20", "Cortina": "08:28"},
    4: {"Echoland": "07:42", "Nakiyama": "07:50", "Happo_Terminal": "07:55", "Iwatake": "08:03", "Ochikura": "08:12", "Tsugaike": "08:18"},
    5: {"Happo_Terminal": "08:10", "Iwatake": "08:18", "Ochikura": "08:27", "Tsugaike": "08:33", "Norikura": "08:40", "Satomi": "08:43", "Cortina": "08:51"},
    6: {"Echoland": "08:02", "Nakiyama": "08:10", "Happo_Terminal": "08:15", "Iwatake": "08:23", "Ochikura": "08:32", "Tsugaike": "08:38"},
    7: {"Goryu": "08:07", "Echoland": "08:27", "Nakiyama": "08:35", "Happo_Terminal": "08:40", "JR_Hakuba": "08:46", "Iwatake": "08:55", "Ochikura": "09:04", "Tsugaike": "09:10", "Norikura": "09:17", "Satomi": "09:20", "Cortina": "09:28"},
    8: {"Goryu": "08:22", "Echoland": "08:42", "Nakiyama": "08:50", "Happo_Terminal": "08:55", "Iwatake": "09:03", "Ochikura": "09:12", "Tsugaike": "09:18"},
    9: {"Goryu": "08:47", "Echoland": "09:07", "Nakiyama": "09:15", "Happo_Terminal": "09:20", "Iwatake": "09:28", "Ochikura": "09:37", "Tsugaike": "09:43", "Norikura": "09:50", "Satomi": "09:53", "Cortina": "10:01"},
    10: {"Echoland": "09:27", "Nakiyama": "09:35", "Happo_Terminal": "09:40", "JR_Hakuba": "09:46", "Iwatake": "09:55", "Ochikura": "10:04", "Tsugaike": "10:10"},
    11: {"Echoland": "09:42", "Nakiyama": "09:50", "Happo_Terminal": "09:55", "Iwatake": "10:03", "Ochikura": "10:12", "Tsugaike": "10:18", "Norikura": "10:25", "Satomi": "10:28", "Cortina": "10:36"},
    12: {"Goryu": "09:22", "Echoland": "09:57", "Nakiyama": "10:05", "Happo_Terminal": "10:10", "Iwatake": "10:18", "Ochikura": "10:27", "Tsugaike": "10:33"},
    13: {"Hakuba47": "10:00", "Goryu": "10:07", "Echoland": "10:27", "Nakiyama": "10:35", "Happo_Terminal": "10:40", "JR_Hakuba": "10:46", "Iwatake": "10:55", "Ochikura": "11:04", "Tsugaike": "11:10", "Norikura": "11:17", "Satomi": "11:20", "Cortina": "11:28"},
    14: {"Goryu": "10:07", "Echoland": "10:57", "Nakiyama": "11:05", "Happo_Terminal": "11:10", "Iwatake": "11:18", "Ochikura": "11:27", "Tsugaike": "11:33"},
    15: {"Hakuba47": "11:00", "Goryu": "11:07", "Echoland": "11:27", "Nakiyama": "11:35", "Happo_Terminal": "11:40", "JR_Hakuba": "11:46", "Iwatake": "11:55", "Ochikura": "12:04", "Tsugaike": "12:10", "Norikura": "12:17", "Satomi": "12:20", "Cortina": "12:28"},
    16: {"Goryu": "11:07", "Echoland": "11:57", "Nakiyama": "12:05", "Happo_Terminal": "12:10", "Iwatake": "12:18", "Ochikura": "12:27", "Tsugaike": "12:33"},
    17: {"Hakuba47": "12:00", "Goryu": "12:07", "Echoland": "12:27", "Nakiyama": "12:35", "Happo_Terminal": "12:40", "JR_Hakuba": "12:46", "Iwatake": "12:55", "Ochikura": "13:04", "Tsugaike": "13:10", "Norikura": "13:17", "Satomi": "13:20", "Cortina": "13:28"},
    18: {"Goryu": "12:07", "Echoland": "12:57", "Nakiyama": "13:05", "Happo_Terminal": "13:10", "Iwatake": "13:18", "Ochikura": "13:27", "Tsugaike": "13:33"},
    19: {"Hakuba47": "13:00", "Goryu": "13:37", "Echoland": "13:27", "Nakiyama": "13:35", "Happo_Terminal": "13:40", "JR_Hakuba": "13:46", "Iwatake": "13:55", "Ochikura": "14:04", "Tsugaike": "14:10", "Norikura": "14:17", "Satomi": "14:20", "Cortina": "14:28"},
    20: {"Goryu": "13:37", "Echoland": "13:57", "Nakiyama": "14:05", "Happo_Terminal": "14:10", "Iwatake": "14:18", "Ochikura": "14:27", "Tsugaike": "14:33"},
    21: {"Hakuba47": "14:00", "Goryu": "14:07", "Echoland": "14:27", "Nakiyama": "14:35", "Happo_Terminal": "14:40", "JR_Hakuba": "14:46", "Iwatake": "14:55", "Ochikura": "15:04", "Tsugaike": "15:10", "Norikura": "15:17", "Satomi": "15:20", "Cortina": "15:28"},
    22: {"Goryu": "14:37", "Echoland": "14:57", "Nakiyama": "15:05", "Happo_Terminal": "15:10", "Iwatake": "15:18", "Ochikura": "15:27", "Tsugaike": "15:33"},
    23: {"Hakuba47": "15:00", "Goryu": "15:07", "Echoland": "15:27", "Nakiyama": "15:35", "Happo_Terminal": "15:40", "JR_Hakuba": "15:46", "Iwatake": "15:55", "Ochikura": "16:04", "Tsugaike": "16:10", "Norikura": "16:17", "Satomi": "16:20", "Cortina": "16:28"},
    24: {"Goryu": "15:37", "Echoland": "15:57", "Nakiyama": "16:05", "Happo_Terminal": "16:10", "Iwatake": "16:18", "Ochikura": "16:27", "Tsugaike": "16:33"},
    25: {"Hakuba47": "16:00", "Goryu": "16:07", "Echoland": "16:27", "Nakiyama": "16:35", "Happo_Terminal": "16:40", "JR_Hakuba": "16:46", "Iwatake": "16:55", "Ochikura": "17:04"},
    26: {"Hakuba47": "16:15", "Goryu": "16:22", "Echoland": "16:42", "Nakiyama": "16:50", "Happo_Terminal": "16:55", "Iwatake": "17:03"},
    27: {"Hakuba47": "16:30", "Goryu": "16:37", "Echoland": "16:57", "Nakiyama": "17:05", "Happo_Terminal": "17:10", "Iwatake": "17:18", "Ochikura": "17:27", "Tsugaike": "17:33"},
    28: {"Hakuba47": "17:00", "Goryu": "17:07", "Echoland": "17:27", "Nakiyama": "17:35", "Happo_Terminal": "17:40", "Iwatake": "17:46"}
}

@tool
def find_best_shuttle(user_location:str, user_destination:str, target_time: str=None) -> str:
    """
    此工具可以查阅从民宿出发与到达民宿的穿梭巴士的时间。
    **参数为以下标准ID**:
    - Cortina
    - Satomi
    - Norikura
    - Tsugaike
    - Ochikura（此站点为距离民宿最近的站点）
    - Iwatake
    - JR_Hakuba
    - Happo_Terminal
    - Nakiyama
    - Echoland
    - Hakuba47
    - Goryu
    如果用户提示地名不在上述列表中则使用NA
    其中参数
    - user_location为上车站点
    - user_destination为下车站点。
    - target_time: (可选) 客人期望的出发时间，必须是 "HH:MM" 格式（24小时制，如 "08:30"或"15:00"）。如果客人未指定时间或查询"现在"的班车，请务必留空。
    """
    print("系统调用穿梭巴士查询工具！")
    if user_location in stop and user_destination in stop:
        current_time = datetime.datetime.now().strftime("%H:%M")
        reference_time = current_time
        if target_time:
            if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", target_time):
                reference_time = target_time
            else:
                return f"系统错误：传入的时间格式 {target_time} 有误，请转换为 HH:MM 格式重试。"

        available_options = []
        directions = [
            ("南行线 (Southbound)", SOUTHBOUND_RUNS), 
            ("北行线 (Northbound)", NORTHBOUND_RUNS)
        ]


        for direction_name, direction_time in directions:
            for run_id, stops in direction_time.items():
                if user_location in stops and user_destination in stops:
                    dep_time = stops[user_location]
                    arr_time = stops[user_destination]
                    
                    if dep_time > reference_time and dep_time < arr_time:
                        available_options.append({
                            "direction": direction_name,
                            "run_id": run_id,
                            "departure": dep_time,
                            "arrival": arr_time
                        })

        if not available_options:
            return f"在时间 {reference_time} 之后，未找到从 {user_location} 直达 {user_destination} 的班车。请提示客人班车可能已结束，或建议呼叫出租车。"
        
        available_options.sort(key=lambda x: x["departure"])
        best = available_options[0]
        best_2 = available_options[1]
        best_3 = available_options[2]
        return f"为您找到：{best['departure']} 从 {user_location} 出发，{best['arrival']} 到达 {user_destination}。下一班为{best_2['departure']} 从 {user_location} 出发，{best_2['arrival']} 到达 {user_destination}。在下一班为{best_3['departure']} 从 {user_location} 出发，{best_3['arrival']} 到达 {user_destination}。"
    else:
        return "提示的位置无法直接前往民宿，建议呼叫出租车。"