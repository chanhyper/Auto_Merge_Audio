# Auto_Merge_Audio
# 音频合成转换程序

## 功能说明
该程序自动合并`cn`和`en`文件夹中的同名音频文件（如01.mp3），播放顺序为：
1. 先播放中文音频（cn目录）
2. 再播放英文音频（en目录）

## 使用步骤

### 1. 安装依赖
```bash
# 安装Python依赖
pip install pydub

# 安装ffmpeg（音频处理核心依赖）
# MacOS系统
brew install ffmpeg

# Windows系统
# 1. 访问 https://ffmpeg.org/download.html#build-windows 下载ffmpeg
# 2. 解压下载的zip文件
# 3. 将解压后的文件夹中的bin目录添加到系统环境变量PATH中
```

### 2. 准备音频文件
- 中文音频放入 `cn/` 文件夹
- 英文音频放入 `en/` 文件夹
- 文件命名格式：`01.mp3`, `02.mp3`...

### 3. 运行程序
```bash
python merge_audio.py
```

### 4. 获取结果
合并后的音频将保存在 `output/` 文件夹，命名格式为 `merged_01.mp3`

## 注意事项
- 确保中英文音频文件数量相同
- 文件命名需严格按数字序号排列
- 首次运行前必须安装ffmpeg
