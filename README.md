<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" crossorigin="anonymous" />

<div style="text-align: center;"><img src="https://github.com/llzgdc/ETBSaveManager/blob/development/src-tauri/icons/128x128.png" alt="icon" width="128" height="128"></div>

<div style="text-align: center;"><h1>ETB Save Manager</h1></div>

---

# Update History

## Version 2.0.0 ~ 2.8.0(development) (2024-07-23 ~ NOW)

- Complete Interface Redesign
- Fixed Legacy Bugs
- Added More Features


## Version 1.0.0 ~ 1.2.0 (2024-02-15 ~ 2024-02-16)
- Initial Version Release
- Implemented Save List Display
- Developed Save Identification, Creation, Deletion, and Editing Functions

# Installation(v2.7.3)

### Windows

1. Download Installation Package:

- [Link-Github](https://github.com/llzgdc/EscapeTheBackroomsSaveGamesTools/releases/tag/v2.3.0)

2. For `exe` file, double-click to use directly

3. For `zip` file, extract and double-click `ETBSaveManager-EN v2.7.3.exe`

# Development (v2.8.0)

## Development Environment

You need to install the Rust environment first.

1. Install Rust: [https://www.rust-lang.org/](https://www.rust-lang.org/)

Then install the PyO3 environment.

1. Install PyO3: [https://pyo3.rs/](https://pyo3.rs/)

### Steps

1. Clone the project code: `git clone https://github.com/llzgdc/ETBSaveManager.git`
2. Enter the project directory: `cd ETBSaveManager`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Run in terminal: `maturin new ETBSM_V2_Function_Rust`
6. Enter the project directory: `cd ETBSM_V2_Function_Rust`
7. Copy files from the `src-rust` folder into the `ETBSM_V2_Function_Rust` folder
8. Run `maturin develop` and wait for compilation
9. Now you can modify `lib.rs`, `main.py`, or other files

**Tips:** After each modification to `lib.rs`, you need to run `maturin develop` again to recompile.

# Feature Introduction

### Create Function  
Creation interface includes: Save Name, Route/Plot, Level, Difficulty, and Mode. You can freely fill or select. Right side shows a simple level preview image for quick level selection.

### Delete Function
First select a save in the Treeview, then click delete. Currently supports single deletion, multi-select deletion coming in future updates.

### Edit Function
Select a save in the Treeview, then click edit. In the edit interface, you can input save names. If you can't change the name, it means the name is already in use.

### Hide Function
Select a save in the Treeview, then click hide. Hidden save files can be found in the HiddenFiles folder within the save directory. "Show" function will be added in future updates.

### Refresh Function
Click the button to reload save list.

### Show Folder Function
Click the button to open save folder.

# Bilibili Video Introduction
**Link：[https://www.bilibili.com/video/BV194421Z7sj](https://www.bilibili.com/video/BV194421Z7sj)**  