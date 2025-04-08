
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
