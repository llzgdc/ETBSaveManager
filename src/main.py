import tkinter as tk
import locale
import ETBSM_V2_Function_Rust as f2
import sys
import os
from tkinter import ttk
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
        pass

    def function_edit(self):
        pass

    def function_refresh(self):
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
        
if __name__ == "__main__":
    app = ETBSM()
    app.mainloop()