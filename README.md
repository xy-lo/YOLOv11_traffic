
# 🚦 YOLOv11 交通信号识别系统

本项目基于 YOLOv11 实现交通信号灯图像的检测与识别，提供 Streamlit Web 界面支持，可用于批量图像检测与实时摄像头检测。

---

## 📦 功能简介

- **图片批量检测**：上传图片文件夹，系统将逐张检测交通信号灯并保存带有检测结果的图像。
- **实时摄像头检测**：自动开启电脑摄像头，实时检测画面中的交通信号灯。
- **结果可视化**：检测结果在页面中实时展示，支持彩色标注与响应时间显示。
- **本地保存检测结果**：检测图像将保存至指定文件夹，方便后续查看与分析。

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

> ⚠️ 若缺少 OpenCV、Streamlit 等包，请手动安装：
```bash
pip install opencv-python streamlit
```

### 2️⃣ 启动服务

在终端中运行以下命令启动 GUI：

```bash
streamlit run D:\python\TrafficRules-main\GUI_G.py --server.address 0.0.0.0 --server.port 8501
```

### 3️⃣ 打开浏览器访问

浏览器地址栏输入：

```
http://localhost:8501/
```

即可打开网页界面。

---

## 🧾 数据说明

- 默认读取文件夹路径：`inferences/images/`
- 图像格式支持 `.jpg` `.png` 等常见格式。
- 检测结果输出到：`inferences/results/`

---

## 🧠 模型简介

- 使用自定义训练的 YOLOv11 模型，支持以下交通信号类别：
  - 红灯（Red Light）
  - 黄灯（Yellow Light）
  - 绿灯（Green Light）

模型输出为目标框和分类标签，检测结果通过红色框标注于图像中。

---

## 🌐 项目结构

```
TrafficRules-main/
├── GUI_G.py                 # Streamlit 主界面
├── main.py                  # 核心推理与预处理函数
├── inferences/
│   ├── images/              # 输入图像
│   └── results/             # 检测结果保存路径
├── utils/                   # 工具函数（如有）
├── models/                  # YOLOv11 模型（如有）
└── README.md                # 使用说明文档
```

---

## 📎 联系作者

如有疑问或建议，欢迎访问我的 GitHub 主页 👇  
🔗 [https://github.com/xy-lo](https://github.com/你的GitHub用户名)

---

## 🏁 致谢

感谢 YOLO 系列开源项目提供的技术支持。  
本项目仅用于学习与研究用途，禁止用于任何商业化用途。


# YOLOv11 交通信号检测系统

该项目基于 YOLOv11 模型，实现了对交通信号灯的图像检测和分类。支持图片批量检测和实时摄像头检测模式，应用 PyTorch 和 Streamlit 实现人性化界面。

---

## 功能特性
- 🚦 支持交通信号灯检测，包括红绿灯分类
- 📺 支持图片批量检测
- 📹 支持实时摄像头检测
- 展示检测结果并保存
- 🔄 简单易用的 Streamlit UI

---

## 启动方式

1. 确保已安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行 Streamlit 界面：
```bash
streamlit run GUI_G.py --server.address 0.0.0.0 --server.port 8501
```

3. 手机连同一网络后访问宿主机IP。
例如：`http://192.168.1.101:8501`

---

## 代码结构
```
TrafficRules-main/
├── GUI_G.py                 # Streamlit UI 主程序
├── main.py                  # 包含 inference 与预处理逻辑
├── inferences/
│   ├── images/              # 待检测图片文件夹
│   └── results/             # 检测结果保存文件夹
├── models/                  # YOLOv11 训练模型
└── README.md
```

---

## 界面演示

### 1. 主界面显示
![主界面](https://example.com/main_interface.png)

### 2. 单张图片检测
![单张图检测](https://example.com/single_image_detection.png)

### 3. 批量检测
![批量检测](https://example.com/batch_image_detection.png)

---

## 连接
- 💻 作者 GitHub: [https://github.com/your-username](https://github.com/your-username)
- 🎡 模型基于: YOLOv11

---

## 本地使用注意
- 如需手机访问 Streamlit，请使用 `--server.address 0.0.0.0` 开启，并访问宿主机IP
- `st.set_page_config` 必须放在文件最开始处！

---

## 小结
此项目适合作为交通监控系统的基础框架，支持内置模型、本地开发、快速应用。
