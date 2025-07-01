use dirs_next as dirs;
use pyo3::prelude::*;
use regex::Regex;
use serde_json::Value;
use std::collections::HashMap;
use std::fs::File;
use std::io::{Cursor, Read};
use std::path::Path;
use uesave::Save;
use walkdir::WalkDir;

// 解析 .sav 文件为 JSON
fn parse_sav_file(path: &Path) -> Result<Save, String> {
    let mut file = File::open(path).map_err(|e| format!("打开文件失败: {}", e))?;

    // 读取整个文件到内存中
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)
        .map_err(|e| format!("读取文件内容失败: {}", e))?;

    // 使用 Cursor 将内存数据包装成一个 Read 实现
    let mut reader = Cursor::new(&buffer);

    // 使用 uesave::Save::read 来解析存档文件
    let save = Save::read(&mut reader).map_err(|e| format!("解析存档失败: {:?}", e))?;

    Ok(save)
}

// 提取 CurrentLevel_0.Name 字段值
fn extract_current_level(json: &Value) -> String {
    json["root"]["properties"]["CurrentLevel_0"]["Name"]
        .as_str()
        .map(|s| s.to_string())
        .unwrap_or_else(|| "Level 0".to_string())
}

// 提取 Difficulty_0.Byte.Label 并映射难度等级
fn extract_difficulty_label(json: &Value) -> String {
    json["root"]["properties"]["Difficulty_0"]["Byte"]["Label"]
        .as_str()
        .map(|s| {
            if s.contains("NewEnumerator0") {
                "easy"
            } else if s.contains("NewEnumerator1") {
                "hard"
            } else if s.contains("NewEnumerator2") {
                "nightmare"
            } else {
                "normal"
            }
        })
        .map(|s| s.to_string())
        .unwrap_or_else(|| "normal".to_string())
}

#[pyfunction]
fn scan_save_files() -> PyResult<Vec<HashMap<&'static str, String>>> {
    let re =
        Regex::new(r"(?i)^(MULTIPLAYER|SINGLEPLAYER)_(.+?)_(Easy|Normal|Hard|Nightmare|\d+)\.sav$")
            .map_err(|e| {
                PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid regex: {}", e))
            })?;

    let base_path = dirs::data_local_dir()
        .ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyFileNotFoundError, _>(
                "Could not find local app data dir",
            )
        })?
        .join("EscapeTheBackrooms/Saved/SaveGames");

    let mut result = Vec::new();

    for entry in WalkDir::new(&base_path).into_iter().filter_map(|e| e.ok()) {
        if !entry.file_type().is_file() {
            continue;
        }

        let path = entry.path();
        let file_name = match path.file_name().and_then(|s| s.to_str()) {
            Some(name) => name,
            None => continue,
        };

        let captures = match re.captures(file_name) {
            Some(cap) => cap,
            None => continue,
        };

        let mode = captures.get(1).map(|m| m.as_str()).unwrap().to_string();
        let name = captures.get(2).map(|m| m.as_str()).unwrap().to_string();
        let difficulty = captures.get(3).map(|m| m.as_str()).unwrap().to_string();
        let full_path = path.to_string_lossy().to_string();

        let is_private = path
            .parent()
            .map(|p| p != Path::new(&base_path))
            .unwrap_or(false);

        // 解析 sav 文件内容
        let save =
            parse_sav_file(path).map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e))?;

        let json = serde_json::to_value(&save).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "序列化存档为 JSON 失败: {}",
                e
            ))
        })?;

        let current_level = extract_current_level(&json);
        let actual_difficulty = extract_difficulty_label(&json);

        let mut map = HashMap::new();
        map.insert("id", result.len().to_string());
        map.insert("name", name);
        map.insert("mode", mode.to_lowercase());
        map.insert("difficulty", difficulty);
        map.insert("is_private", is_private.to_string());
        map.insert("path", full_path);
        map.insert("current_level", current_level);
        map.insert("actual_difficulty", actual_difficulty);

        result.push(map);
    }

    Ok(result)
}

/// 定义 Python 模块
#[pymodule]
fn ETBSM_V2_Function_Rust(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(scan_save_files, m)?)?;
    Ok(())
}
