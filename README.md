# Image-Video-Converter
  多媒体格式转换工具集：一个基于 FFmpeg 的图形界面工具集，支持视频和图片格式的快速转换，操作简单且功能丰富。
  
## 功能特点
  （1）视频格式转换：支持 MP4、AVI、MOV、FLV、MKV 等常见视频格式互转
  
  （2）图片格式转换：支持 PNG、JPG、WebP、BMP、TIFF 等图片格式转换
  
  （3）批量处理：图片转换器支持多文件批量转换
  
  （4）进度显示：实时展示转换进度和详细日志
  
  （5）中文支持：支持中文路径和文件名，解决编码问题

## 运行截图

<img width="815" height="603" alt="image" src="https://github.com/user-attachments/assets/84d90165-38d9-4807-bbf7-bc1cabce0c9d" />


<img width="302" height="191" alt="image" src="https://github.com/user-attachments/assets/d2d548fa-9dfe-4098-a857-794c0dbf1110" />


<img width="753" height="540" alt="image" src="https://github.com/user-attachments/assets/9fb56b03-ddaa-4582-bef7-4afe18c03029" />


<img width="316" height="146" alt="image" src="https://github.com/user-attachments/assets/37e9596c-0127-4857-a133-10f655a7e298" />



## 安装与使用
### 前置条件
  #### 运行可执行文件（推荐）：无需安装 Python，直接运行main.exe
  #### 运行源代码：需安装 Python 3.6 + 环境
          下载地址：https://www.python.org/downloads/
  #### 必须安装 FFmpeg（两种运行方式都需要）：
          Windows：从FFmpeg 官网下载，解压后将bin目录添加到系统环境变量
          macOS：brew install ffmpeg
          Linux：sudo apt install ffmpeg
### 快速启动
  #### 视频转换器：
        直接双击 VideoConverter/main.exe
        或运行源代码：python VideoConverter/main.py
  #### 图片转换器：
        直接双击 ImageConverter/main.exe
        或运行源代码：python ImageConverter/main.py

## 使用教程
  ### 视频转换步骤
    1、点击 "浏览" 按钮选择需要转换的视频文件
    2、从下拉菜单选择目标输出格式（如 MP4、AVI 等）
    3、（可选）点击 "设置输出路径" 自定义保存位置（默认与输入文件同目录）
    4、点击 "开始转换"，等待进度条完成（可在状态框查看详细过程）
  ### 图片转换步骤
    1、单文件转换：点击 "浏览" 选择图片；批量转换：直接点击 "批量转换"
    2、选择目标输出格式（如 PNG、WebP 等）
    3、（可选）设置输出路径
    4、点击 "开始转换" 或 "批量转换"，等待完成

## 常见问题
    1、提示 "未找到 FFmpeg"：
        检查 FFmpeg 是否已安装并添加到系统环境变量；重启电脑使环境变量生效
        验证方法：命令行输入ffmpeg -version，若显示版本信息则安装成功
    2、中文路径导致转换失败：
        程序已处理编码问题，确保使用最新版本
        避免使用特殊符号（如 emoji、空格除外）作为文件名
    3、转换后文件无法打开：
        检查输出格式是否正确（如视频格式不能转为图片格式）
    4、exe 文件无法运行
        确保已安装 FFmpeg（exe 依赖 FFmpeg 运行）
        尝试运行源代码版本排查问题
