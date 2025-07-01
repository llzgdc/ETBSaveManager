<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" crossorigin="anonymous" />

<div style="text-align: center;"><img src="https://github.com/llzgdc/ETBSaveManager/blob/development/src-tauri/icons/128x128.png" alt="icon" width="128" height="128"></div>

<div style="text-align: center;"><h1>逃离后室存档工具</h1></div>

---

# 更新历史

## 版本 2.0.0 ~ 2.8.0(development) (2024-07-23 ~ 现在)

- 界面大换新
- 修复了遗留的 bug
- 添加了更多功能

## 版本 1.0.0 ~ 1.2.0 (2024-02-15 ~ 2024-02-16)

- 初始版本发布
- 实现了存档列表的展示
- 实现了存档识别、新建、删除、编辑功能

# 安装（v2.7.3）

### Windows

1. 下载安装包：

- [下载链接-Github](https://github.com/llzgdc/EscapeTheBackroomsSaveGamesTools/releases/tag/v2.7.3)
- [下载链接-Gitee](https://gitee.com/llzgd/EscapeTheBackroomsSaveGamesTools/releases/tag/v2.7.3)
- [下载链接-蓝奏云](https://llzgd.lanzouu.com/b009h9fqxg) 密码:`aq4u`

2. 若下载`exe`文件，直接双击即可使用
3. 若下载`zip`文件，解压后双击`逃离后室存档工具V2.7.3.exe`即可使用

# 开发（v2.8.0）

## 开发环境
你需要先安装rust环境
1. 安装rust环境：[https://www.rust-lang.org/zh-CN/](https://www.rust-lang.org/zh-CN/)

再安装PyO3环境
1. 安装PyO3环境：[https://pyo3.rs/](https://pyo3.rs/)

### 步骤
1. 克隆项目代码`git clone https://github.com/llzgdc/ETBSaveManager.git`
2. 进入项目目录`cd ETBSaveManager`
3. 安装虚拟环境`python -m venv venv`
4. 激活虚拟环境`source venv/bin/activate`
5. 终端中运行`maturin new ETBSM_V2_Function_Rust`
6. 进入项目目录`cd ETBSM_V2_Function_Rust`
7. 将`src-rust`文件夹中的文件复制到`ETBSM_V2_Function_Rust`文件夹中
8. 运行`maturin develop`并等待编译
9. 现在可以修改`lib.rs`或`main.py`及其他文件

**tips:** 每次修改完`lib.rs`后，需要运行`maturin develop`重新编译


# 功能介绍

### 新建功能  
新建界面中包含：存档名称、线路剧情、层级、难度与模式。  
可以自由填写或选择。  
右边有简易的层级图片预览，快速找到想要的层级。

### 删除功能
你需要先在Treeview中选择一个存档，再点击删除。   
目前只能一个一个的删除，未来会加入多选删除。  

### 编辑功能
同样，你需要先在Treeview中选择一个存档，再点击编辑。  
在编辑界面中，你可以输入存档名称。  
如果你发现改不了名的时候，就代表名称重复了。

### 隐藏功能
同样，你需要先在Treeview中选择一个存档，再点击隐藏。  
隐藏的存档文件你可以在存档文件夹下的HiddenFiles文件夹中查看。  
未来会加入“显示”功能

### 刷新功能
点击按钮后可以重新获取存档

### 显示文件夹功能
点击按钮后可以打开存档文件夹  

# Bilibili视频介绍
**链接：[https://www.bilibili.com/video/BV194421Z7sj](https://www.bilibili.com/video/BV194421Z7sj)**  