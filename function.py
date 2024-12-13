from logger_setup import LoggerSingleton
from datetime import datetime
import webbrowser
import binascii
import pytz
import sys
import os

Ending1_levels = [
    "Level 0教学关卡", "Level 1宜居地带(1)", "Level 1宜居地带(2)", "Level 1宜居地带(3)", "Level 1宜居地带(4)", "The Hub枢纽", "Level 2废弃公共带(1)", "Level 3发电站", "Level 4废弃办公室", "Level 5恐怖旅馆(1)", "Level 5恐怖旅馆(2)", "Level 5恐怖旅馆(3)", "Level 2废弃公共带(2)", "Level Fun享乐层", "Level 37崇高", "Level !", "The End终末", "Level 922……无尽的结局", "Level 94动画(1)", "Level 94动画(2)", "Level 6熄灯", "Level 7深海恐惧症", "Level 8岩洞系统", "Level 0.11腐烂的前厅", "Level 9郊区(1)", "Level 9郊区(2)", "Level 10丰裕", "Level 3999真正的结局", "Level 0.2重塑的混乱", "Level 6.1零食室", "Level !-!灵魂终末", "Level 188百叶庭", "Level 37.2暗池(1)", "Level 37.2暗池(2)","Level 37.2暗池(3)", "Level 37.2暗池(4)", "Level FUN+(1)",  "Level FUN+(2)", "Level FUN+(3)", "Level FUN+(4)", "Level FUN+(5)","Level 52学校大厅", "Level 55.1隧道"
]
Ending2_levels = []
Ending3_levels = []
Ending4_levels = []
Ending5_levels = []

Ending1_mapping = {
    "0" : "level0",
    "1" : "TopFloor",
    "2" : "MiddleFloor",
    "3" : "GarageLevel2",
    "4" : "BottomFloor",
    "5" : "thehub",
    "6" : "Pipes1",
    "7" : "ElectricalStation",
    "8" : "office",
    "9" : "hotel",
    "10" : "Floor3",
    "11" : "BoilerRoom",
    "12" : "Pipes2",
    "13" : "levelfun",
    "14" : "Poolrooms",
    "15" : "levelrun",
    "16" : "theend",
    "17" : "level922",
    "18" : "level94",
    "19" : "AnimatedKingdom",
    "20" : "lightsOut",
    "21" : "OceanMap",
    "22" : "CaveLevel",
    "23" : "level05",
    "24" : "Level9",
    "25" : "AbandonedBase",
    "26" : "Level10",
    "27" : "level3999",
    "28" : "level07",
    "29" : "Snackrooms",
    "30" : "LevelDash",
    "31" : "Level188Expanded",
    "32" : "PoolroomsExpanded",
    "33" : "WaterParkLevel01",
    "34" : "WaterParkLevel02",
    "35" : "WaterParkLevel03",
    "36" : "LevelFunExpanded",
    "37" : "Zone1",
    "38" : "Zone2",
    "39" : "Zone3",
    "40" : "Zone4",
    "41" : "level52",
    "42" : "TunnelLevel"
    }
Ending2_mapping = {}
Ending3_mapping = {}
Ending4_mapping = {}
Ending5_mapping = {}

logger = LoggerSingleton.get_instance(log_to_file=True, log_to_console=True)

Save_Games_dir = os.path.join(os.getenv("LOCALAPPDATA"), "EscapeTheBackrooms", "Saved", "SaveGames")
logger_path = os.path.join(os.getenv('LOCALAPPDATA'), 'llzgd', 'ETBSGT')

segments = {
    'Easy': '2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7230',
    'Hard': '2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7231',
    'Nightmare': '2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7232',
    'Normal': '2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43',
    }

def set_level_lists():
    if len(Ending1_levels) < 32:
        logger.error("Ending1_levels must have at least 32 elements")
        raise ValueError("Ending1_levels must have at least 32 elements")
    
    logger.debug("Extending Ending2_levels with %s", Ending1_levels[0:21])
    Ending2_levels.extend(Ending1_levels[0:21])

    logger.debug("Extending Ending3_levels with %s", Ending1_levels[0:32])
    Ending3_levels.extend(Ending1_levels[0:32])

    logger.debug("Extending Ending4_levels with %s", Ending1_levels[0:5])
    Ending4_levels.extend(Ending1_levels[0:5])

    logger.debug("Extending Ending5_levels with %s", Ending1_levels[0:17])
    Ending5_levels.extend(Ending1_levels[0:17])

    logger.info("All level lists extended successfully")
    return Ending1_levels, Ending2_levels, Ending3_levels, Ending4_levels, Ending5_levels

def set_level_mapping(Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping, indices):
    assert isinstance(Ending1_mapping, dict), "Ending1_mapping must be a dictionary"
    assert isinstance(Ending2_mapping, dict), "Ending2_mapping must be a dictionary"
    assert isinstance(Ending3_mapping, dict), "Ending3_mapping must be a dictionary"
    assert isinstance(Ending4_mapping, dict), "Ending4_mapping must be a dictionary"
    assert isinstance(Ending5_mapping, dict), "Ending5_mapping must be a dictionary"

    # 验证 indices 是否有效
    if not all(0 <= index <= len(Ending1_mapping) for index in indices):
        logger.error("Indices must be non-negative and within the range of Ending1_mapping keys")
        raise ValueError("Indices must be non-negative and within the range of Ending1_mapping keys")

    # 更新目标映射
    for i, target_ending in enumerate([Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping]):
        for key in list(Ending1_mapping.keys())[0:indices[i]]:
            target_ending[key] = Ending1_mapping[key]
        logger.debug("Set %s to %s in %s", key, Ending1_mapping[key], target_ending)

    logger.info("All level dicts extended successfully")
    return Ending1_mapping, Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping

def get_resource_path(relative_path):
    # 尝试获取PyInstaller创建的临时目录，用于确定是否在打包后的可执行文件环境中运行
    try:
        base_path = sys._MEIPASS
    # 如果获取不到临时目录，即在普通Python脚本环境中运行，则获取当前脚本的目录路径
    except AttributeError as e:
        # 记录错误信息
        logger.warning(f"Failed to get _MEIPASS attribute: {e}")
        base_path = os.path.dirname(os.path.abspath(__file__))

    # 验证相对路径的安全性
    if not os.path.isabs(relative_path) and ".." not in relative_path:
        # 拼接基目录路径和相对路径，得到资源文件的绝对路径，并返回
        return os.path.join(base_path, relative_path)
    else:
        logger.error("Invalid relative path")
        raise ValueError("Invalid relative path")

def show_folder():
     if os.path.exists(Save_Games_dir):
        os.startfile(Save_Games_dir)

def check_real_difficulty(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        for segment_id, hex_pattern in segments.items():
            pattern_bytes = binascii.unhexlify(hex_pattern)
            if pattern_bytes in content:
                return segment_id
    return None

def local_time(difficulty):
    if difficulty.isdigit():
        timestamp = int(difficulty)
        utc_dt = datetime.fromtimestamp(timestamp)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Etc/GMT+8'))
        formatted_local_dt = local_dt.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_local_dt
    else:
         return "普通难度"
    
def check_update():
    webbrowser.open_new("https://docs.qq.com/doc/DTHNKSEx1d3lFemlC")

def author():
    webbrowser.open_new("https://space.bilibili.com/2019959464")

def get_time_stamp():
    # 获取当前时间的 datetime 对象
    now = datetime.now()
    # 获取当前时区
    local_timezone = pytz.timezone('Africa/Abidjan')
    now_local = local_timezone.localize(now)
    # 转换为 UTC 时间
    now_utc = now_local.astimezone(pytz.utc)
    # 获取时间戳
    timestamp = int(now_utc.timestamp())
    return timestamp

def find_and_replace_in_hex(file_path, search_hex, replace_hex):
    # 打开文件并读取原始数据
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # 转换为十六进制字符串
    hex_data = binascii.hexlify(binary_data).decode('ascii')

    # 将查找和替换的十六进制字符串转换为小写，确保大小写不敏感
    search_hex = search_hex.lower()
    replace_hex = replace_hex.lower()

    # 替换十六进制数据中的指定内容
    modified_hex_data = hex_data.replace(search_hex, replace_hex)

    # 将修改后的十六进制数据转换回二进制数据
    modified_binary_data = binascii.unhexlify(modified_hex_data.encode('ascii'))

    # 保存修改后的内容到原文件
    with open(file_path, 'wb') as file:
        file.write(modified_binary_data)

def new_edit_difficulty(name, mapped_value, difficulty):
    global new_filename
    if difficulty == "Easy":
        old_filename = get_resource_path(f"Resources/SaveGames/E1/{mapped_value}.sav")
        new_filename = f"MULTIPLAYER_{name}_Easy.sav"
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7230"

    elif difficulty == "Normal":
        old_filename = get_resource_path(f"Resources/SaveGames/E1/{mapped_value}.sav")
        new_filename = f"MULTIPLAYER_{name}_Normal.sav"
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43"

    elif difficulty == "Hard":
        old_filename = get_resource_path(f"Resources/SaveGames/E1/{mapped_value}.sav")
        new_filename = f"MULTIPLAYER_{name}_Hard.sav"
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7231"

    elif difficulty == "Nightmare":
        old_filename = get_resource_path(f"Resources/SaveGames/E1/{mapped_value}.sav")
        new_filename = f"MULTIPLAYER_{name}_Hard.sav"
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7232"

    new_filepath = os.path.join(Save_Games_dir, new_filename)
    file_path = os.path.join(Save_Games_dir, new_filename)
    search_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43"

    return old_filename, new_filepath, file_path, search_hex, replace_hex

def open_logger_path():
    if os.path.exists(logger_path):
        os.startfile(logger_path)

def edit_edit_difficulty(new_difficulty, real_difficulty):
    if new_difficulty == "Easy":
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7230"
    elif new_difficulty == "Normal":
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43"
    elif new_difficulty == "Hard":
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7231"
    elif new_difficulty == "Nightmare":
        replace_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7232"
                
    if real_difficulty == "Easy":
        search_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7230"
    elif real_difficulty == "Normal":
        search_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43"
    elif real_difficulty == "Hard":
        search_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7231"
    elif real_difficulty == "Nightmare":
        search_hex = "2F47616D652F5361766553797374656D2F42505F4E65775F5361766547616D652E42505F4E65775F5361766547616D655F43000B000000446966666963756C7479000D0000004279746550726F70657274790021000000000000000D000000455F446966666963756C747900001D000000455F446966666963756C74793A3A4E6577456E756D657261746F7232"
                
    return search_hex, replace_hex