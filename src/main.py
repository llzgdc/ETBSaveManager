import tkinter as tk
import locale
import ETBSM_V2_Function_Rust as f2
import sys
import os
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess

VERSION = "2.8.0"

class ETBSM(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 设置窗口默认标题
        self.title(f"ETBSaveManager{VERSION}")

        # 设置窗口大小以及居中位置
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = f'{834}x{485}+{int((screenwidth - 834) / 2)}+{int((screenheight - 515) / 2)}'
        self.geometry(size)

        # 禁止改变窗口大小
        self.resizable(False, False)

        # 设置窗口图标
        self.iconbitmap(self.get_path("./resources/icon/icon.ico"))

        # 检测系统语言并修改窗口标题
        self.detected_language = self.detect_system_language()
        self.update_title_based_on_language(self.detected_language)

        self.create_main_widgets()

        self.function_refresh()

    def detect_system_language(self):
        # 获取当前系统的语言设置
        lang_code, _ = locale.getlocale()
        if lang_code:
            language = lang_code.split('_')[0]
        else:
            language = 'unknown'

        print(f"检测到的语言为: {language}")

        return language

    def update_title_based_on_language(self, language):
        # 根据检测到的语言动态更新窗口标题
        if 'Chinese' in language:
            new_title = f"逃离后室存档工具{VERSION}"
        else:
            new_title = f"ETBSaveManager{VERSION}"

        self.title(new_title)

    def get_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def create_main_widgets(self):
        # 配置全局按钮样式
        style = ttk.Style()
        style.configure('TButton', font=('Segoe UI', 12))

        # 简化按钮创建函数
        def create_button(text, x, y, command):
            btn = ttk.Button(text=text, style='TButton', command=command)
            btn.place(x=x, y=y, width=100, height=45)
            return btn

        # 创建按钮
        self.new_btn = create_button("新建", 17, 10, self.function_new)
        self.delete_btn = create_button("删除", 133, 10, self.function_delete)
        self.edit_btn = create_button("编辑", 249, 10, self.function_edit)
        self.refresh_btn = create_button("刷新", 365, 10, self.function_refresh)
        self.show_folder_btn = create_button("显示文件夹", 481, 10, self.function_show_folder)
        self.more_btn = create_button("更多", 597, 10, self.function_more)
        self.settings_btn = create_button("设置", 713, 10, self.function_settings)

        # 创建 Treeview 和滚动条
        self.treeview = ttk.Treeview(show="headings")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # 设置 Treeview 列标题和样式
        self.treeview["columns"] = ("mode", "name", "difficulty", "current_level")
        self.treeview.heading("mode", text="存档类型", anchor=tk.CENTER)
        self.treeview.heading("name", text="存档名称", anchor=tk.CENTER)
        self.treeview.heading("difficulty", text="存档难度 / 实际难度", anchor=tk.CENTER)
        self.treeview.heading("current_level", text="当前层级", anchor=tk.CENTER)

        # 设置列内容居中显示
        self.treeview.column("mode", anchor=tk.CENTER)
        self.treeview.column("name", anchor=tk.CENTER)
        self.treeview.column("difficulty", anchor=tk.CENTER)
        self.treeview.column("current_level", anchor=tk.CENTER)

        # 设置列宽
        self.set_column_widths([4/22, 10/22, 4/22, 4/22])

        # 布局控件
        self.treeview.place(x=10, y=80, width=804, height=390)
        scrollbar.place(x=814, y=80, width=20, height=390)

        # 创建返回按钮（初始隐藏）
        self.create_back_btn()
        self.back_btn.place_forget()
    
    def function_new(self):
        pass

    def function_delete(self):
        selected_items = self.treeview.selection()

        if not selected_items:
            messagebox.showinfo("提示", "请选择要删除的存档！")
            return

        # 获取对应的存档路径
        paths_to_delete = []
        for item in selected_items:
            index = self.treeview.index(item)
            if index < len(saves):  # 确保索引有效
                paths_to_delete.append(saves[index]['path'])

        if not paths_to_delete:
            messagebox.showwarning("警告", "未找到可删除的存档路径。")
            return

        # 显示确认对话框
        confirm_msg = "是否删除这些存档？" if len(paths_to_delete) > 1 else "是否删除这个存档？"
        if messagebox.askyesno("确认删除", confirm_msg):
            try:
                for path in paths_to_delete:
                    if os.path.exists(path):
                        os.remove(path)
                messagebox.showinfo("成功", "删除成功")
                self.function_refresh()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")

    def function_edit(self):
        pass

    def function_refresh(self):
        global saves

        def map_difficulty(difficulty):
            if difficulty in ['easy', 'normal', 'hard', 'nightmare']:
                return {
                    'easy': '简单难度',
                    'normal': '普通难度',
                    'hard': '困难难度',
                    'nightmare': '噩梦难度'
                }[difficulty]
            elif difficulty.isdigit():
                return '普通难度'
            else:
                return difficulty
            
        saves = f2.scan_save_files()

        # 清空当前 Treeview 内容
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for save in saves:
            if save.get('is_private') == 'false':
                mode = save['mode'].lower()
                difficulty = save['difficulty'].lower()
                actual_difficulty = save['actual_difficulty'].lower()
                current_level = save['current_level']

                display_mode = {'multiplayer': '多人模式', 'singleplayer': '单人模式'}.get(mode, mode)

                # 转换 difficulty
                display_difficulty = map_difficulty(difficulty)
                # 转换 actual_difficulty
                display_actual_difficulty = map_difficulty(actual_difficulty)

                if display_difficulty == display_actual_difficulty:
                    combined_difficulty = display_difficulty
                else:
                    combined_difficulty = f"{display_difficulty} / {display_actual_difficulty}"

                self.treeview.insert("", tk.END, values=(display_mode, save['name'], combined_difficulty, current_level))
    
    def function_show_folder(self):
        global folder_path

        # 使用环境变量获取路径
        folder_path = os.path.join(os.path.expandvars('%LOCALAPPDATA%'), 'EscapeTheBackrooms', 'Saved', 'SaveGames')
        
        # 检查文件夹是否存在
        if os.path.exists(folder_path):
            if os.name == 'nt':  # 如果是Windows系统
                os.startfile(folder_path)
            elif os.name == 'posix':  # 如果是Linux或Mac系统
                subprocess.run(['open', folder_path])
            else:
                subprocess.run(['xdg-open', folder_path])
        else:
            print("文件夹不存在:", folder_path)

    def function_more(self):
        pass

    def function_settings(self):
        pass

    def function_back(self):
        pass

    def create_back_btn(self):
        # 获取资源路径并加载图标
        resource_path = self.get_path("./resources/icon/back.ico")
        back_btn_icon = Image.open(resource_path)
        back_btn_icon.thumbnail((40, 40))
        self.back_btn_photo = ImageTk.PhotoImage(back_btn_icon)

        # 按钮参数
        x, y, width, height = 774, 425, 50, 50

        # 创建并放置按钮
        self.back_btn = ttk.Button(image=self.back_btn_photo, command=self.function_back)
        self.back_btn.place(x=x, y=y, width=width, height=height)
    
    def set_column_widths(self, widths, total_width=814):
        column_widths = [int(total_width * width) for width in widths]
        for i, width in enumerate(column_widths):
            self.treeview.column(i, width=width)
    
    def setup_game_levels(self):
        global Ending1_levels, Ending2_levels, Ending3_levels, Ending4_levels, Ending5_levels, mode_list, name_list, difficulty_list, opened, Ending1_mapping, Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping

        Ending1_levels = [
            "Level 0教学关卡", "Level 1宜居地带(1)", "Level 1宜居地带(2)", "Level 1宜居地带(3)", "Level 1宜居地带(4)", "The Hub枢纽", "Level 2废弃公共带(1)", "Level 3发电站", "Level 4废弃办公室", "Level 5恐怖旅馆(1)", "Level 5恐怖旅馆(2)", "Level 5恐怖旅馆(3)", "Level 2废弃公共带(2)", "Level Fun享乐层", "Level 37崇高", "Level !", "The End终末", "Level 922……无尽的结局", "Level 94动画(1)", "Level 94动画(2)", "Level 6熄灯", "Level 7深海恐惧症", "Level 8岩洞系统", "Level 0.11腐烂的前厅", "Level 9郊区(1)", "Level 9郊区(2)", "Level 10丰裕", "Level 3999真正的结局", "Level 0.2重塑的混乱", "Level 6.1零食室", "Level !-!灵魂终末", "Level 188百叶庭", "Level 37.2暗池(1)", "Level 37.2暗池(2)","Level 37.2暗池(3)", "Level 37.2暗池(4)", "Level FUN+(1)",  "Level FUN+(2)", "Level FUN+(3)", "Level FUN+(4)", "Level FUN+(5)","Level 52学校大厅", "Level 55.1隧道"
        ]

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
        
        # 初始化列表和字典
        Ending1_levels = []
        Ending2_levels = []
        Ending3_levels = []
        Ending4_levels = []
        Ending5_levels = []
        mode_list = []
        name_list = []
        difficulty_list = []
        opened = []

        Ending1_mapping = {}
        Ending2_mapping = {}
        Ending3_mapping = {}
        Ending4_mapping = {}
        Ending5_mapping = {}

        # 设置等级列表
        def set_level_lists():
            if len(Ending1_levels) < 32:
                raise ValueError("Ending1_levels must have at least 32 elements")
            
            Ending2_levels.extend(Ending1_levels[0:21])
            Ending3_levels.extend(Ending1_levels[0:32])
            Ending4_levels.extend(Ending1_levels[0:5])
            Ending5_levels.extend(Ending1_levels[0:17])

        # 设置等级映射
        def set_level_mapping(indices):
            assert isinstance(Ending1_mapping, dict), "Ending1_mapping must be a dictionary"
            assert isinstance(Ending2_mapping, dict), "Ending2_mapping must be a dictionary"
            assert isinstance(Ending3_mapping, dict), "Ending3_mapping must be a dictionary"
            assert isinstance(Ending4_mapping, dict), "Ending4_mapping must be a dictionary"
            assert isinstance(Ending5_mapping, dict), "Ending5_mapping must be a dictionary"

            if not all(0 <= index <= len(Ending1_mapping) for index in indices):
                raise ValueError("Indices must be non-negative and within the range of Ending1_mapping keys")

            for i, target_ending in enumerate([Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping]):
                for key in list(Ending1_mapping.keys())[0:indices[i]]:
                    target_ending[key] = Ending1_mapping[key]

        # 设置初始等级列表
        set_level_lists()

        # 设置等级映射
        indices = [21, 32, 5, 17]
        set_level_mapping(indices)

    def show_main_widgets(self):
        # 按钮及其 x 坐标
        buttons = [
            (self.new_btn, 17),
            (self.delete_btn, 133),
            (self.edit_btn, 249),
            (self.refresh_btn, 365),
            (self.show_folder_btn, 481),
            (self.more_btn, 597),
            (self.settings_btn, 713)
        ]

        # 显示所有主按钮
        for btn, x in buttons:
            if btn is not None:
                btn.place(x=x, y=10, width=100, height=45)

        # 显示树形视图
        if self.treeview is not None:
            self.treeview.place(x=10, y=80, width=814, height=390)
    
    def hide_all_widgets(self):
        # 定义需要隐藏的控件类型
        widgets_to_hide = (ttk.Button, ttk.Treeview, tk.Text, tk.Label, tk.Entry, ttk.Combobox, tk.Canvas)

        # 遍历所有子控件并尝试隐藏它们
        for widget in self.winfo_children():
            if isinstance(widget, widgets_to_hide):
                widget.place_forget()
    
    def create_new_widgets(self):
        # 存档名称输入
        self.name_label = tk.Label(text="请输入存档名称：", font=("Segoe UI", 12))
        self.name_label.place(x=10, y=10, height=30, width=170)
        
        self.name_entry = tk.Entry(font=("Segoe UI", 14))
        self.name_entry.place(x=10, y=40, height=30, width=170)

        # 结局选择
        self.ending_label = tk.Label(text="请选择结局：", font=("Segoe UI", 12))
        self.ending_label.place(x=10, y=90, height=30, width=170)

        self.ending_box = ttk.Combobox(
            values=["主结局", "结局2", "结局3", "结局4", "结局5"],
            font=("Segoe UI", 12),
            state="readonly"
        )
        self.ending_box.place(x=10, y=120, height=30, width=170)
        self.ending_box.set("主结局")
        self.ending_box.bind("<<ComboboxSelected>>", self.switch_ending)

        # 层级选择
        self.level_label = tk.Label(text="请选择层级：", font=("Segoe UI", 12))
        self.level_label.place(x=10, y=170, height=30, width=170)

        self.level_box = ttk.Combobox(
            values=Ending1_levels,
            font=("Segoe UI", 12),
            state="readonly"
        )
        self.level_box.place(x=10, y=200, height=30, width=170)
        self.level_box.set(Ending1_levels[0])
        self.level_box.bind("<<ComboboxSelected>>", self.show_image)

        # 难度选择
        self.difficulty_label = tk.Label(text="请选择难度：", font=("Segoe UI", 12))
        self.difficulty_label.place(x=10, y=250, height=30, width=170)

        self.difficulty_box = ttk.Combobox(
            values=["简单难度", "普通难度", "困难难度", "噩梦难度"],
            font=("Segoe UI", 12),
            state="disabled"
        )
        self.difficulty_box.place(x=10, y=280, height=30, width=170)
        self.difficulty_box.set("普通难度")

        # 模式选择
        self.mode_label = tk.Label(text="请选择模式：", font=("Segoe UI", 12))
        self.mode_label.place(x=10, y=330, height=30, width=170)

        self.mode_box = ttk.Combobox(
            values=["单人模式", "多人模式"],
            font=("Segoe UI", 12),
            state="readonly"
        )
        self.mode_box.place(x=10, y=360, height=30, width=170)
        self.mode_box.set("单人模式")
        self.mode_box.bind("<<ComboboxSelected>>", self.disable_difficulty)

        # 按钮区域
        self.confirm_new_btn = ttk.Button(text="确定", command=self.confirm_new)
        self.confirm_new_btn.place(x=10, y=410, height=50, width=75)

        # 返回按钮
        back_icon = Image.open(self.get_path("Resources/Other/Icons/back.ico")).resize((40, 40))
        self.new_back_btn_photo = ImageTk.PhotoImage(back_icon)

        self.new_back_btn = ttk.Button(image=self.new_back_btn_photo, command=self.back)
        self.new_back_btn.place(x=105, y=410, width=75, height=50)

        # 图像显示区域
        self.white_canvas = tk.Canvas(bg="white", width=814, height=315)
        default_img = Image.open(self.get_path("Resources/Other/Images/Ending1/0.jpg"))
        self.default_photo = ImageTk.PhotoImage(default_img)

        self.image_label = tk.Label(image=self.default_photo)
        self.image_label.place(x=200, y=65)

        self.show_image()
    
if __name__ == "__main__":
    app = ETBSM()
    app.mainloop()