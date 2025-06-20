from functions import set_level_lists, set_level_mapping, get_resource_path, show_folder, check_real_difficulty, local_time, check_update, author, get_time_stamp, find_and_replace_in_hex, new_edit_difficulty, open_logger_path, edit_edit_difficulty
from logger_setup import LoggerSingleton
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import shutil
import os
import re


VERSION = "V2.7.2"

Save_Games_dir = os.path.join(os.getenv("LOCALAPPDATA"), "EscapeTheBackrooms", "Saved", "SaveGames")

logger = LoggerSingleton.get_instance(log_to_file=True, log_to_console=True)

def set_lists_dicts():
    global Ending1_levels, Ending2_levels, Ending3_levels, Ending4_levels, Ending5_levels, mode_list, name_list, difficulty_list, opened, Ending1_mapping, Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping

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

    Ending1_levels, Ending2_levels, Ending3_levels, Ending4_levels, Ending5_levels = set_level_lists()

    Ending1_mapping, Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping = set_level_mapping(Ending2_mapping, Ending3_mapping, Ending4_mapping, Ending5_mapping, [21, 32, 5, 17])

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        set_lists_dicts()

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        logger.debug(f"Screen size obtained: {screenwidth}x{screenheight}")

        self.title(f"E.T.B. Save Manager{VERSION}")
        self.iconbitmap(get_resource_path("Resources/Other/Icons/icon.ico"))
        logger.debug("The title and icon have been set")

        # 确保窗口位置为整数
        size = f'{834}x{485}+{int((screenwidth - 834) / 2)}+{int((screenheight - 515) / 2)}'
        self.geometry(size)
        logger.debug("The window size has been set")

        self.resizable(False, False)
        logger.debug("Window zooming is disabled")
        logger.info("A main window has been created")

        try:
            self.background_image = Image.open(get_resource_path("Resources/Other/Images/main.jpg"))
            logger.debug("The background image has been loaded")
        except Exception as e:
            logger.error(f"Failed to load background image: {e}")
            self.background_image = None

        if self.background_image:
            self.background_photo = ImageTk.PhotoImage(self.background_image)
            self.background_label = tk.Label(self, image=self.background_photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            logger.info("The background label has been created")
        
        self.create_main_widgets()
        self.populate_treeview()
    
    def create_main_widgets(self):
        # 创建样式对象
        style = ttk.Style()
        
        # 定义一个样式，并设置字体大小
        style.configure('TButton', font=('SimHei', 12))

        # 定义按钮创建函数
        def create_button(text, x, y, command):
            btn = ttk.Button(text=text, style='TButton', command=command)
            btn.place(x=x, y=y, width=100, height=45)
            logger.debug(f"The {text} button has been created at ({x}, {y})")
            return btn
    
        # 创建按钮
        self.new_btn = create_button("New", 17, 10, self.new)
        self.delete_btn = create_button("Delete", 133, 10, self.delete)
        self.edit_btn = create_button("Edit", 249, 10, self.edit)
        self.refresh_btn = create_button("Refresh", 365, 10, self.refresh)
        self.show_folder_btn = create_button("Show Folder", 481, 10, show_folder)
        self.more_btn = create_button("More", 597, 10, self.more)
        self.settings_btn = create_button("Settings", 713, 10, self.settings)

        # 创建 Treeview
        self.treeview = ttk.Treeview(show="headings")
        self.treeview.place(x=10, y=80, width=814, height=390)
        logger.debug("The treeview has been created")

        # 创建返回按钮
        self.create_back_btn()
        self.back_btn.place_forget()

        # 设置 Treeview 列标题
        self.treeview["columns"] = ("mode", "name", "difficulty")
        self.treeview.heading("mode", text="MP/SP", anchor=tk.CENTER)
        self.treeview.heading("name", text="Save Name", anchor=tk.CENTER)
        self.treeview.heading("difficulty", text="Save Difficulty", anchor=tk.CENTER)
        logger.info("The main widgets have been created")

        # 设置列宽
        self.set_column_widths([5/22, 11/22, 5/22])
        logger.info("The column widths have been set")
    
    def show_main_widgets(self):
        # 确保所有按钮已正确初始化
        buttons = [
            (self.new_btn, 17),
            (self.delete_btn, 133),
            (self.edit_btn, 249),
            (self.refresh_btn, 365),
            (self.show_folder_btn, 481),
            (self.more_btn, 597),
            (self.settings_btn, 713)
            ]
    
        for btn, x in buttons:
            if btn is not None:  # 确保按钮已正确初始化
                btn.place(x=x, y=10, width=100, height=45)
    
        # 设置树视图的位置和尺寸
        if self.treeview is not None:
            self.treeview.place(x=10, y=80, width=814, height=390)

    def set_column_widths(self, widths, total_width=814):
        column_widths = [int(total_width * width) for width in widths]
        for i, width in enumerate(column_widths):
            self.treeview.column(i, width=width)
    
    def set_treeview_column_center(self, treeview, column):
        treeview.heading(column, anchor="center")
        treeview.column(column, anchor="center")

    def populate_treeview(self):
        mode_list.clear()
        name_list.clear()
        difficulty_list.clear()
        logger.debug("Cleared lists")

        try:
            if not os.path.exists(Save_Games_dir):
                return

            old_saves = os.listdir(Save_Games_dir)
        except Exception as e:
            logger.error(f"Error accessing directory: {e}")
            return

        valid_saves = [file_name for file_name in old_saves if file_name.startswith("MULTIPLAYER") or file_name.startswith("SINGLEPLAYER")]

        for i, file_name in enumerate(valid_saves, start=1):
            mode, name, difficulty = self.parse_file_name(file_name)
            if mode == "未知模式" and name == "未知名称" and difficulty == "未知难度":
                continue
            if mode and name and difficulty:
                self.treeview.insert("", "end", text=str(i), values=(mode, name, difficulty))

        for col in self.treeview["columns"]:
            self.set_treeview_column_center(self.treeview, col)
    
    def replace_difficulty(self, difficulty):
        return difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")

    def contains_digit(self, s):
        return any(c.isdigit() for c in s)

    def parse_file_name(self, file_name):
        try:
            logger.debug(f"Start parsing file names: {file_name}")
            parts = file_name.split("_")
            if len(parts) < 3:
                logger.error(f"The file name format is incorrect: {file_name}")
                raise ValueError("The file name format is incorrect")

            mode = parts[0]
            name = parts[1]
            difficulty = parts[2].split(".")[0] if len(parts) > 2 else "Normal"

            safe_file_path = os.path.join(Save_Games_dir, os.path.basename(file_name))
            real_difficulty = self.replace_difficulty(check_real_difficulty(safe_file_path))

            if real_difficulty == "未知":
                return "未知模式", "未知名称", "未知难度"
            
            mode_list.append(mode)
            name_list.append(name)
            difficulty_list.append(difficulty)

            # 安全性检查
            if not all(part.isalnum() or part in ["MULTIPLAYER", "SINGLEPLAYER", "Normal", "Easy", "Hard", "Nightmare"] for part in [mode, name, difficulty]):
                logger.error(f"The file name contains illegal characters: {file_name}")
                raise ValueError("The file name contains illegal characters")

            mode = mode.replace("MULTIPLAYER", "Multiplayer").replace("SINGLEPLAYER", "Singleplayer")
            name = name
            if self.contains_digit(difficulty):
                difficulty = self.replace_difficulty("Normal")
            else:
                difficulty = self.replace_difficulty(difficulty)

            if difficulty == real_difficulty:
                difficulty = f"{difficulty}"
            else:
                difficulty = f"{difficulty} / {real_difficulty}"

            logger.debug(f"Parsing the file name completion: mode={mode}, name={name}, difficulty={difficulty}")
            return mode, name, difficulty

        except (ValueError, IndexError) as e:
            logger.error(f"An error occurred while parsing the file name: {e}")
            return "未知模式", "未知名称", "未知难度"  # 返回默认值
    
    def create_back_btn(self):
        try:
            # 确保 get_resource_path 函数已定义
            resource_path = get_resource_path("Resources/Other/Icons/back.ico")
            back_btn_icon = Image.open(resource_path)
            back_btn_icon.thumbnail((40, 40))
            self.back_btn_photo = ImageTk.PhotoImage(back_btn_icon)

            # 参数化按钮的位置和大小
            button_x = 774
            button_y = 425
            button_width = 50
            button_height = 50

            self.back_btn = ttk.Button(image=self.back_btn_photo, command=self.back)
            self.back_btn.place(x=button_x, y=button_y, width=button_width, height=button_height)
        except Exception as e:
            logger.error(f"Error creating back button: {e}")
    
    def show_back_btn(self):
        self.back_btn.place(x=774, y=425, width=50, height=50)

    def hide_all_widgets(self):
        # 定义需要隐藏的控件类型
        widgets_to_hide = (ttk.Button, ttk.Treeview, tk.Text, tk.Label, tk.Entry, ttk.Combobox, tk.Canvas)
    
        # 遍历所有子控件
        for widget in self.winfo_children():
            if isinstance(widget, widgets_to_hide):
                try:
                    widget.place_forget()
                except Exception as e:
                    logger.error(f"Error hiding widget: {e}")
    
        # 设置背景标签的位置
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def back(self):
        self.hide_all_widgets()
        self.show_main_widgets()

    def create_new_widgets(self):
        self.name_label = tk.Label(text="Please Enter Save Name:", font=("SimHei", 10))
        self.name_label.place(x=10, y=10, height=30, width=170)

        self.name_entry = tk.Entry(font=("SimHei", 14))
        self.name_entry.place(x=10, y=40, height=30, width=170)

        self.ending_label = tk.Label(text="Please Select Ending:", font=("SimHei", 12))
        self.ending_label.place(x=10, y=90, height=30, width=170)

        self.ending_box = ttk.Combobox(values=["Main Ending", "Ending 2", "Ending 3", "Ending 4", "Ending 5"], font=("SimHei", 12), state="readonly")
        self.ending_box.place(x=10, y=120, height=30, width=170)
        self.ending_box.set("Main Ending")

        self.level_label = tk.Label(text="Please Select Level:", font=("SimHei", 12))
        self.level_label.place(x=10, y=170, height=30, width=170)
        self.level_box_value = Ending1_levels
        self.level_box = ttk.Combobox(values=self.level_box_value, font=("SimHei", 12), state="readonly")
        self.level_box.place(x=10, y=200, height=30, width=170)
        self.level_box.set(self.level_box_value[0])
        self.ending_box.bind("<<ComboboxSelected>>", self.switch_ending)

        self.difficulty_label = tk.Label(text="Please Select Difficulty:", font=("SimHei", 9))
        self.difficulty_label.place(x=10, y=250, height=30, width=170)

        self.difficulty_box = ttk.Combobox(values=["Easy", "Normal", "Hard", "Nightmare"], font=("SimHei", 12), state="disabled")
        self.difficulty_box.place(x=10, y=280, height=30, width=170)
        self.difficulty_box.set("Normal")

        self.mode_label = tk.Label(text="Please Select Mode:", font=("SimHei", 12))
        self.mode_label.place(x=10, y=330, height=30, width=170)

        self.mode_box = ttk.Combobox(values=["Singleplayer", "Multiplayer"], font=("SimHei", 12), state="readonly")
        self.mode_box.place(x=10, y=360, height=30, width=170)
        self.mode_box.set("Singleplayer")

        self.mode_box.bind("<<ComboboxSelected>>", self.disable_difficulty)

        self.confirm_new_btn = ttk.Button(text="Confirm", command=self.confirm_new) 
        self.confirm_new_btn.place(x=10, y=410, height=50, width=75)

        new_back_btn_icon = Image.open(get_resource_path("Resources/Other/Icons/back.ico"))
        new_back_btn_icon.thumbnail((40, 40))
        self.new_back_btn_photo = ImageTk.PhotoImage(new_back_btn_icon)

        self.new_back_btn = ttk.Button(image=self.new_back_btn_photo, command=self.back)
        self.new_back_btn.place(x=105, y=410, width=75, height=50)

        self.white_canvas = tk.Canvas(bg="white", width=814, height=315)

        default_image_path = get_resource_path("Resources/Other/Images/Ending1/0.jpg")
        self.default_image = Image.open(default_image_path) 
        self.default_photo = ImageTk.PhotoImage(self.default_image) #

        self.image_label = tk.Label(image=self.default_photo)
        self.image_label.place(x=200, y=65)

        self.show_image()

        self.level_box.bind("<<ComboboxSelected>>", self.show_image)
    
    def show_image(self, event=None):
        selected_index = self.level_box.get()
        selected_ending_1 = self.ending_box.current()

        if selected_index == "None(DO NOT SELECT)":
            image_path = get_resource_path(f"Resources/Other/Images/None.jpg")
        else:
            selected_index = self.level_box.current()
            image_path = get_resource_path(f"Resources/Other/Images/Ending1/{selected_index}.jpg")

        self.show_image_on_canvas(image_path)

    def show_image_on_canvas(self, image_path):
        # 清空画布
        self.white_canvas.delete("all")
        
        # 加载并缩放图片
        image = Image.open(image_path)
        image.thumbnail((680, 350))  # 缩放图片以适应画布
        self.image_on_canvas = ImageTk.PhotoImage(image)

        # 计算图片在画布上的位置使其居中显示
        canvas_width = 680
        canvas_height = 350
        image_width = image.width
        image_height = image.height

        x_offset = (canvas_width - image_width) / 2
        y_offset = (canvas_height - image_height) / 2


        self.white_canvas.create_image(x_offset, y_offset, anchor="nw", image=self.image_on_canvas)

        # 更新图片标签的配置
        self.image_label.configure(image=self.image_on_canvas)

    def disable_difficulty(self, event):
        selected_mode = self.mode_box.get()
        if selected_mode == "Multiplayer":
            self.difficulty_box.config(state="readonly")
        elif selected_mode == "Singleplayer":
            self.difficulty_box.config(state="disabled")
            self.difficulty_box.set("Normal")

    def switch_ending(self, event):
        selected_ending = self.ending_box.get()
        if selected_ending == "Main Ending":
            self.level_box_value = Ending1_levels
        elif selected_ending == "Ending 2":
            self.level_box_value = Ending2_levels
        elif selected_ending == "Ending 3":
            self.level_box_value = Ending3_levels
        elif selected_ending == "Ending 4":
            self.level_box_value = Ending4_levels
        elif selected_ending == "Ending 5":
            self.level_box_value = Ending5_levels
        self.level_box.config(values=self.level_box_value)
        self.level_box.set(self.level_box_value[0])
        self.show_image()

    def new(self):
        target_item = "new"
        if target_item in opened:
            self.hide_all_widgets()
            self.show_new_widgets()
        else:
            self.hide_all_widgets()
            self.create_new_widgets()
            opened.append(target_item)
    
    def show_new_widgets(self):
        self.name_label.place(x=10, y=10, height=30, width=170)
        self.name_entry.place(x=10, y=40, height=30, width=170)
        self.name_entry.delete(0, "end")

        self.ending_label.place(x=10, y=90, height=30, width=170)
        self.ending_box.place(x=10, y=120, height=30, width=170)
        self.ending_box.set("Main Ending")

        self.level_label.place(x=10, y=170, height=30, width=170)
        self.level_box.place(x=10, y=200, height=30, width=170)
        self.level_box.set("Level 0")

        self.difficulty_label.place(x=10, y=250, height=30, width=170)
        self.difficulty_box.place(x=10, y=280, height=30, width=170)
        self.difficulty_box.set("Normal")
        self.difficulty_box.config(state="disabled")

        self.mode_label.place(x=10, y=330, height=30, width=170)
        self.mode_box.place(x=10, y=360, height=30, width=170)
        self.mode_box.set("Singleplayer")

        self.confirm_new_btn.place(x=10, y=410, height=50, width=75)
        self.new_back_btn.place(x=105, y=410, width=75, height=50)

        self.image_label.place(x=200, y=65)

        self.show_image()

    def confirm_new(self):
        global mapped_value, new_filepath, new_filename
        new_name = self.name_entry.get().strip()
        if not new_name:
            messagebox.showinfo("Tip", "Save name cannot be empty!")
            return

        if not re.match("^[A-Za-z0-9]+$", new_name):
            messagebox.showerror("Error", "Only English letters and numbers are allowed!")
            return
        
        mode = self.mode_box.get()
        mode = mode.replace("Multiplayer", "MULTIPLAYER").replace("Singleplayer", "SINGLEPLAYER")
        difficulty = self.difficulty_box.get()
        name = self.name_entry.get()
        level = self.level_box.get()
        ending = self.ending_box.current()

        if level == "None(DO NOT SELECT)":
            messagebox.showerror("Error", "Do not select this option!")
        else:
            level = str(self.level_box.current())
            ending = "ending"+str(ending+1)+"_mapping"
            ending_a = []

            if ending == "ending1_mapping":
                mapped_value = Ending1_mapping[level]
                ending_a = Ending1_mapping
            elif ending == "ending2_mapping":
                mapped_value = Ending2_mapping[level]
                ending_a = Ending2_mapping
            elif ending == "ending3_mapping":
                mapped_value = Ending3_mapping[level]
                ending_a = Ending3_mapping
            elif ending == "ending4_mapping":
                mapped_value = Ending4_mapping[level]
                ending_a = Ending4_mapping
            elif ending == "ending5_mapping":
                mapped_value = Ending5_mapping[level]
                ending_a = Ending5_mapping

            if mode == "SINGLEPLAYER":
                if level in ending_a:
                    global old_filename
                    timestamp = get_time_stamp()
                    old_filename = get_resource_path(f"Resources/SaveGames/E1/{mapped_value}.sav")
                    new_filename = f"SINGLEPLAYER_{name}_{timestamp}.sav"
                    new_filepath = os.path.join(Save_Games_dir, new_filename)
            elif mode == "MULTIPLAYER":
                if level in ending_a:
                    difficulty = difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")
                    old_filename, new_filepath, file_path, search_hex, replace_hex = new_edit_difficulty(name, mapped_value, difficulty)
            
            try:
                difficulty = difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")
                shutil.copy(old_filename, new_filepath)
                if mode == "MULTIPLAYER":
                    find_and_replace_in_hex(file_path, search_hex, replace_hex)
                if mode == "SINGLEPLAYER":
                    now = local_time(str(timestamp))
                    messagebox.showinfo("Tip", "Save created successfully!"+"\n"+"Save Type:"+"Singleplayer"+"\n"+"Save Name"+f": {name}"+"\n"+"Timestamp: "+f"{timestamp}"+"\n"+"Time: "+f"{now}")
                elif mode == "MULTIPLAYER":
                    if difficulty == "Nightmare":
                        messagebox.showinfo("Tip", "Save created successfully!\n" +"Save Type: Multiplayer\n" +f"Save Name: {name}\n" +f"Save Difficulty: {difficulty}\n" +"(Need to find a save with display difficulty)")
                    else:
                        messagebox.showinfo("Tip", "Save created successfully!\n" +"Save Type: Multiplayer\n" +f"Save Name: {name}\n" +f"Save Difficulty: {difficulty}")
            except Exception as e:
                messagebox.showerror("Error", "Save creation error: " + f"{str(e)}")
            
            self.back()
            self.refresh()

    def delete(self):
        selected_items = self.treeview.selection()

        if not selected_items:
            messagebox.showinfo("Tip", "Please select a save to delete!")
            return
        else:
            delete_items = []

            for selected_item in selected_items:
                item_index = self.treeview.index(selected_item)

                name = name_list[item_index]
                mode = mode_list[item_index]
                difficulty = difficulty_list[item_index]

                save_game_name = f"{mode}_{name}_{difficulty}.sav"
                delete_items.append(save_game_name)

            for selected_item in delete_items:
                file_path = os.path.join(Save_Games_dir, selected_item)

                logger.debug(f"Start parsing file names: {selected_item}")
                parts = selected_item.split("_")
                if len(parts) < 3:
                    logger.error(f"The file name format is incorrect: {selected_item}")
                    raise ValueError("The file name format is incorrect")
                
                mode = parts[0]
                name = parts[1]
                difficulty = parts[2].split(".")[0]

                real_difficulty = check_real_difficulty(file_path)
                real_difficulty = real_difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")

                if os.path.exists(file_path):
                    mode = mode.replace("SINGLEPLAYER", "Singleplayer").replace("MULTIPLAYER", "Multiplayer")
                    if mode == "Multiplayer":
                        difficulty = difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")
                        question = (f"Please confirm the following details:\n"f"Save Mode: {mode}\n"f"Save Name: {name}\n"f"Save Difficulty: {difficulty}\n"f"Actual Difficulty: {real_difficulty}")
                    if mode == "Singleplayer":
                        time = local_time(difficulty)
                        difficulty = "Normal"
                        question = (f"Please confirm the following details:\n"f"Save Mode: {mode}\n"f"Save Name: {name}\n"f"Save Difficulty: {difficulty}\n"f"Actual Difficulty: {real_difficulty}")
                        if time != "Normal":
                            question = question + f"\nCreated Time:{time}"
            
                ask = messagebox.askquestion("Tip", question)
                if ask == "yes":
                    os.remove(file_path)
                    messagebox.showinfo("Tip", "Deleted Successfully!")
                    self.refresh()
                else:
                    continue
            
    def edit(self):
        target_item = "edit"
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showinfo("Tip", "Please select a save to edit!")
            return
        if target_item in opened:
            self.hide_all_widgets()
            self.show_edit_widgets()
        else:
            self.create_edit_widgets()
            self.hide_all_widgets()
            self.show_edit_widgets()
            opened.append(target_item)

    def create_edit_widgets(self):
        self.edit_name_label = tk.Label(text="Enter a new save name\nEnglish letters and\n numbers only\nIf you can't change,\nit means the name is \nalready taken", font=("SimHei", 10))
        self.edit_name_label.place(x=200, y=130, width=200, height=75)

        self.edit_mode_label = tk.Label(text="Select a New Mode", font=("SimHei", 12))
        self.edit_mode_label.place(x=430, y=130, width=200, height=30)

        self.edit_input = tk.Entry(font=("SimHei", 12))
        self.edit_input.place(x=200, y=230, width=200, height=30)

        self.edit_new_mode = ttk.Combobox(values=["Multiplayer", "Singleplayer"], font=("SimHei", 12), state="readonly")
        self.edit_new_mode.place(x=430, y=160, width=200, height=30)
        self.edit_new_mode.bind("<<ComboboxSelected>>", self.switch_edit_difficulty)

        self.edit_difficult_label = tk.Label(text="Select a New Difficulty", font=("SimHei", 12))
        self.edit_difficult_label.place(x=430, y=200, width=200, height=30)

        self.edit_difficult_mode = ttk.Combobox(values=["Easy", "Normal", "Hard", "Nightmare"], font=("SimHei", 12), state="readonly")
        self.edit_difficult_mode.place(x=430, y=230, width=200, height=30)

        self.confirm_edit_btn = ttk.Button(text="Confirm", command=self.edit_save_game)
        self.confirm_edit_btn.place(x=317, y=280, width=200, height=30)
    
    def switch_edit_difficulty(self, event):
        new_mode = self.edit_new_mode.get()
        new_mode = new_mode.replace("Singleplayer", "SINGLEPLAYER").replace("Multiplayer", "MULTIPLAYER")
        if new_mode == "SINGLEPLAYER":
            self.edit_difficult_mode.set("Normal")
            self.edit_difficult_mode.config(state="disabled")
        elif new_mode == "MULTIPLAYER":
            self.edit_difficult_mode.config(state="readonly")
    
    def edit_save_game(self):
        selected_item = self.treeview.selection()

        if not selected_item:
            messagebox.showinfo("Tip", "Please select a save to edit!")
            return
        else:
            item_index = self.treeview.index(selected_item[0])

            name = name_list[item_index]
            mode = mode_list[item_index]
            difficulty = difficulty_list[item_index]

            new_name =  self.edit_input.get().strip()
            new_mode = self.edit_new_mode.get().replace("Singleplayer", "SINGLEPLAYER").replace("Multiplayer", "MULTIPLAYER")
            new_difficulty = self.edit_difficult_mode.get().replace("Easy", "Easy").replace("Normal", "Normal").replace("Hard", "Hard").replace("Nightmare", "Nightmare")

            save_game_name = f"{mode}_{name}_{difficulty}.sav"
            file_path = os.path.join(Save_Games_dir, save_game_name)
            new_save_game_name = f"{new_mode}_{new_name}_{new_difficulty}.sav"
            new_file_path = os.path.join(Save_Games_dir, new_save_game_name)

            if not new_name:
                messagebox.showinfo("Tip", "Save name cannot be empty!")
                return

            if not re.match("^[A-Za-z0-9]+$", new_name):
                messagebox.showerror("Error", "English letters and numbers only")
                return
            
            if mode == "SINGLEPLAYER":
                if new_mode == "SINGLEPLAYER":
                    new_difficulty = difficulty
                    new_name = f"{new_mode}_{new_name}_{new_difficulty}.sav"
                    old_name_path = os.path.join(Save_Games_dir, save_game_name)
                    new_file_path = os.path.join(Save_Games_dir, new_save_game_name)
                elif new_mode == "MULTIPLAYER":
                    file_path = os.path.join(Save_Games_dir, save_game_name)
                    real_difficulty = check_real_difficulty(file_path)
                    search_hex, replace_hex = edit_edit_difficulty(new_difficulty, real_difficulty)
                    new_name = f"{new_mode}_{new_name}_{new_difficulty}.sav"
                    old_name_path = os.path.join(Save_Games_dir, save_game_name)
                
                    find_and_replace_in_hex(old_name_path, search_hex, replace_hex)

                    new_file_path = os.path.join(Save_Games_dir, new_save_game_name)
            elif mode == "MULTIPLAYER":
                old_name = f"{mode}_{name}_{difficulty}.sav"

                if new_mode == "SINGLEPLAYER":
                    new_difficulty = get_time_stamp()
                    new_name = f"{new_mode}_{new_name}_{new_difficulty}.sav"
                    old_name_path = os.path.join(Save_Games_dir, save_game_name)
                    new_file_path = os.path.join(Save_Games_dir, new_save_game_name)
                elif new_mode == "MULTIPLAYER":
                    file_path = os.path.join(Save_Games_dir, save_game_name)
                    real_difficulty = check_real_difficulty(file_path)
                    search_hex, replace_hex = edit_edit_difficulty(new_difficulty, real_difficulty)
                    new_name = f"{new_mode}_{new_name}_{new_difficulty}.sav"
                    old_name_path = os.path.join(Save_Games_dir, save_game_name)

                    find_and_replace_in_hex(old_name_path, search_hex, replace_hex)

                    new_file_path = os.path.join(Save_Games_dir, new_save_game_name)
            
            new_mode = self.edit_new_mode.get().replace("SINGLEPLAYER", "Singleplayer").replace("MULTIPLAYER", "Multiplayer")
            new_difficulty = self.edit_difficult_mode.get().replace("Easy", "Easy").replace("Normal", "Normal").replace("Hard", "Hard").replace("Nightmare", "Nightmare")
            mode = mode.replace("SINGLEPLAYER", "Singleplayer").replace("MULTIPLAYER", "Multiplayer")
            difficulty = difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")

            if os.path.exists(file_path):
                os.rename(file_path, new_file_path)
                self.refresh()
                messagebox.showinfo("Tip", f"Save details have been updated successfully:\n"f"Mode: {new_mode}\n"f"Name: {new_name}\n"f"Difficulty: {new_difficulty}")
                self.hide_all_widgets()
                self.show_main_widgets()
            else:
                messagebox.showerror("Error", f"Update failed:\n"f"Mode: {mode}\n"f"Name: {name}\n"f"Difficulty: {difficulty}")
                self.hide_all_widgets()
                self.show_main_widgets()

    def show_edit_widgets(self):
        selected_item = self.treeview.selection()
        item_index = self.treeview.index(selected_item[0])
        name = name_list[item_index]
        mode = mode_list[item_index]
        mode = mode.replace("MULTIPLAYER", "Multiplayer").replace("SINGLEPLAYER", "Singleplayer")
        difficulty = difficulty_list[item_index]
        if mode == "Singleplayer":
            difficulty = "Normal"
        elif mode == "Multiplayer":
            difficulty = difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")
        self.show_back_btn()
        self.edit_name_label.place(x=200, y=130, width=200, height=80)
        self.edit_input.place(x=200, y=230, width=200, height=30)
        self.confirm_edit_btn.place(x=317, y=280, width=200, height=30)
        self.edit_mode_label.place(x=430, y=130, width=200, height=30)
        self.edit_new_mode.place(x=430, y=160, width=200, height=30)
        self.edit_difficult_label.place(x=430, y=200, width=200, height=30)
        self.edit_difficult_mode.place(x=430, y=230, width=200, height=30)
        self.edit_new_mode.set(mode)
        self.edit_difficult_mode.set(difficulty)
        self.edit_input.delete(0, tk.END)
        self.edit_input.insert(0, name)

    def refresh(self):
        self.treeview.delete(*self.treeview.get_children())
        self.populate_treeview()

    def create_more_widgets(self):
        self.hide_btn = ttk.Button(text="Hide Save", command=self.hide) 
        self.hide_btn.place(x=10, y=10, height=44, width=98)

        self.detail_btn = ttk.Button(text="Details", command=self.detail_1) 
        self.detail_btn.place(x=80, y=10, height=44, width=98)
    
    def show_more_widgets(self):
        self.hide_all_widgets()
        self.hide_btn.place(x=10, y=10, height=44, width=98)
        self.show_back_btn()
        self.back_btn.config(command=self.back)
        self.detail_btn.place(x=120, y=10, height=44, width=98)

    def more(self):
        target_item = "more"
        if target_item in opened:
            self.hide_all_widgets()
            self.show_more_widgets()
        else:
            self.create_more_widgets()
            self.hide_all_widgets()
            self.show_more_widgets()
            opened.append(target_item)
        
    def create_hide_widgets(self):
        self.hide_ok_btn = ttk.Button(text="Confirm", command=self.hide_file) 
        self.hide_ok_btn.place(x=10, y=10, height=44, width=98)

    def show_hide_widgets(self):
        self.hide_all_widgets()
        self.treeview.place(x=10, y=80, width=814, height=390)
        self.back_btn.place(x=774, y=10, width=50, height=50)
        self.back_btn.config(command=self.show_more_widgets)
        self.hide_ok_btn.place(x=10, y=10, height=44, width=98)

    def hide_file(self):
        # 创建隐藏目录
        hidden_dir = os.path.join(os.getenv('LOCALAPPDATA'), "EscapeTheBackrooms", "Saved", "SaveGames", "HiddenFiles")
        logger.debug("Hidden directory path: %s", hidden_dir)

        if not os.path.exists(hidden_dir):
            try:
                os.makedirs(hidden_dir)
                logger.info("Hidden directory created successfully")
            except OSError as e:
                logger.error(f"Went wrong: {e}")
                messagebox.showerror("Error", "An error occurred" + f": {e}")
                return

        # 获取选中的存档项
        selected_items = self.treeview.selection()
        logger.debug("Selected items: %s", selected_items)

        if not selected_items:
            messagebox.showinfo("Tip", "Please select a save to hide!")
            logger.warning("No items selected to hide")
            return
        else:
            hide_items = []

            for selected_item in selected_items:
                item_index = self.treeview.index(selected_item)
                logger.debug("Selected item index: %s", item_index)

                name = name_list[item_index]
                mode = mode_list[item_index]
                difficulty = difficulty_list[item_index]

                save_game_name = f"{mode}_{name}_{difficulty}.sav"
                hide_items.append(save_game_name)
                logger.debug("Added save game to hide list: %s", save_game_name)

            for selected_item in hide_items:
                file_path = os.path.join(Save_Games_dir, selected_item)
                logger.debug("File path to move: %s", file_path)

                logger.debug("Start parsing file names: %s", selected_item)
                parts = selected_item.split("_")
                if len(parts) < 3:
                    logger.error(f"The file name format is incorrect: {selected_item}")
                    raise ValueError("The file name format is incorrect")

                mode = parts[0]
                name = parts[1]
                difficulty = parts[2].split(".")[0]

                save_game_name = f"{mode}_{name}_{difficulty}.sav"
                logger.debug("Parsed save game name: %s", save_game_name)

                try:
                    shutil.move(file_path, hidden_dir)
                    logger.info(f"Moved file {file_path} to {hidden_dir}")
                    messagebox.showinfo("Tip", f"Save \"{save_game_name}\" has been hidden\n"f"Please check the HiddenFiles folder in the save directory")
                except Exception as e:
                    logger.error(f"Failed to move file {file_path}: {e}")
                    messagebox.showerror("Error", f"An error occurred: {e}")

            self.refresh()
            logger.info("Refreshed the window after hiding files")

    def hide(self):
        target_item = "hide"
        if target_item in opened:
            self.hide_all_widgets()
            self.show_hide_widgets()
        else:
            self.create_hide_widgets()
            self.hide_all_widgets()
            self.show_hide_widgets()
            opened.append(target_item)

    def create_detail_1_widgets(self):
        self.detail_ok_btn = ttk.Button(text="Confirm", command=self.detail_2) 
        self.detail_ok_btn.place(x=10, y=10, height=44, width=98)

    def show_detail_1_widgets(self):
        self.hide_all_widgets()
        self.treeview.place(x=10, y=80, width=814, height=390)
        self.back_btn.place(x=774, y=10, width=50, height=50)
        self.back_btn.config(command=self.show_more_widgets)
        self.detail_ok_btn.place(x=10, y=10, height=44, width=98)
    
    def create_detail_2_widgets(self):
        detail_text = "a"
        self.detail_label = tk.Label(text=f"{detail_text}", font=("SimHei", 12))
        self.detail_label.place(x=317, y=192, height=100, width=200)
    
    def show_detail_2_widgets(self, text):
        self.hide_all_widgets()
        self.show_back_btn()
        self.back_btn.config(command=self.show_detail_1_widgets)
        self.detail_label.place(x=317, y=192, height=100, width=200)
        detail_text = text
        self.detail_label.config(text=f"{detail_text}")
    
    def detail(self):
        self.show_back_btn()

        selected_item = self.treeview.selection()

        if not selected_item:
            messagebox.showinfo("Tip", "Please select a save to view its details!")
            return
        else:
            item_index = self.treeview.index(selected_item[0])

            name = name_list[item_index]
            mode = mode_list[item_index]
            difficulty = difficulty_list[item_index]

            save_game_name = f"{mode}_{name}_{difficulty}.sav"
            file_path = os.path.join(Save_Games_dir, save_game_name)
            found_segment = check_real_difficulty(file_path)
            found_segment = found_segment.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")
            mode = mode.replace("MULTIPLAYER", "Multiplayer").replace("SINGLEPLAYER", "Singleplayer")
            if mode == "Singleplayer" or mode == "SINGLEPLAYER":
                difficulty == "Normal"
            elif mode == "Multiplayer":
                difficulty = difficulty.replace("Normal", "Normal").replace("Easy", "Easy").replace("Hard", "Hard").replace("Nightmare", "Nightmare")

            text = f"Save Type: {mode}\n"f"Save Name: {name}\n"f"Save Difficulty: {difficulty}\n"f"Actual Difficulty: {found_segment}"
            self.show_detail_2_widgets(text)

    def create_detail_widgets(self):
        self.create_detail_1_widgets()
        self.create_detail_2_widgets()
    
    def detail_1(self):
        target_item = "detail"
        if target_item in opened:
            self.hide_all_widgets()
            self.show_detail_1_widgets()
        else:
            self.create_detail_widgets()
            self.hide_all_widgets()
            self.show_detail_1_widgets()
            opened.append(target_item)

    def detail_2(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showinfo("Tip", "Please select a save to view its details!")
            return
        
        self.hide_all_widgets()
        self.detail()

    def create_settings_widgets(self):
        self.settings_entry = tk.Text(font=("SimHei", 12), wrap=tk.WORD)
        self.settings_entry.place(x=10, y=10, width=500, height=450)

        self.update_button = ttk.Button(text="Check for Updates", command=check_update)
        self.update_button.place(x=520, y=10, width=170, height=30)

        self.author_btn = ttk.Button(text="Created by llzgdc", command=author)
        self.author_btn.place(x=520, y=50, width=170, height=30)

        self.logger_btn = ttk.Button(text="Open Log Folder", command=open_logger_path)
        self.logger_btn.place(x=520, y=90, width=170, height=30)

        txt_path = get_resource_path("Resources/Other/ann.txt")

        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.settings_entry.delete(1.0, tk.END)
                self.settings_entry.insert(1.0, content)

        self.settings_entry.config(state='disabled')
    
    def show_settings_widgets(self):
        self.settings_entry.place(x=10, y=10, width=500, height=450)
        self.update_button.place(x=520, y=10, width=170, height=30)
        self.author_btn.place(x=520, y=50, width=170, height=30)
        self.logger_btn.place(x=520, y=90, width=170, height=30)
    
    def settings(self):
        target_item = "settings"
        if target_item in opened:
            self.hide_all_widgets()
            self.show_settings_widgets()
            self.show_back_btn()
        else:
            self.hide_all_widgets()
            self.create_settings_widgets()
            opened.append(target_item)
            self.show_back_btn()

if __name__ == "__main__":
    app = Window()
    app.mainloop()