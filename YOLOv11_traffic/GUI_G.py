import streamlit as st
import cv2
import time
import os
import glob
from pathlib import Path
import numpy as np
import tempfile
import shutil

# 请根据你的项目结构调整下面的导入
from main import crop_and_pad  # 裁剪并填充函数
from main import inference  # inference.inference(image) -> (detections, results)


def save_results(image, image_name, detections, results, save_dir):
    # 创建输出文件夹（如果不存在）
    os.makedirs(save_dir, exist_ok=True)

    for bbox, label in detections:
        x1 = bbox[0]
        y1 = bbox[1]
        x2 = bbox[2]
        y2 = bbox[3]

        image = cv2.putText(image, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255))

    for index, x in enumerate((20, 50, 80)):
        image = cv2.circle(image, (x, 20), 12, (0, 255, 0) if results[index] else (0, 0, 255), -1)

    # 构造输出路径
    save_path = os.path.join(save_dir, f'result_{image_name}')
    cv2.imwrite(save_path, image)
    return save_path


def main():
    # 设置页面配置
    st.set_page_config(
        page_title="YOLOv11 交通信号灯检测",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 添加自定义CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #f5f5f5;
        border-radius: 5px;
    }
    .results-container {
        margin-top: 1.5rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 标题和介绍
    st.markdown('<h1 class="main-header">🚦 YOLOv11 交通信号检测</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
        st.markdown("### 👨‍💻 开发者信息")
        st.markdown("[访问我的 GitHub 主页](https://github.com/xy-lo)")

        st.divider()
        mode = st.selectbox("选择模式", ["图片检测", "批量图片检测", "实时摄像头检测"])
        st.divider()

    # 创建临时目录用于保存结果
    default_result_dir = os.path.join(os.getcwd(), "results")
    os.makedirs(default_result_dir, exist_ok=True)

    # 设置会话状态以保存结果路径
    if 'result_dir' not in st.session_state:
        st.session_state.result_dir = default_result_dir

    if mode == "图片检测":
        with st.sidebar:
            st.markdown("### 📸 上传单张图片")
            uploaded_file = st.file_uploader("选择一张图片", type=['jpg', 'jpeg', 'png'])

            # 结果保存路径选择器
            st.markdown("### 💾 选择结果保存位置")
            save_path_option = st.radio("保存位置选项", ["默认路径", "自定义路径"])

            if save_path_option == "默认路径":
                st.session_state.result_dir = default_result_dir
                st.info(f"结果将保存至: {default_result_dir}")
            else:
                custom_path = st.text_input("自定义保存路径", st.session_state.result_dir)
                if custom_path and custom_path != st.session_state.result_dir:
                    if os.path.isdir(custom_path) or not os.path.exists(custom_path):
                        os.makedirs(custom_path, exist_ok=True)
                        st.session_state.result_dir = custom_path
                        st.success(f"已设置保存路径: {custom_path}")
                    else:
                        st.error("无效的目录路径")

        col1, col2 = st.columns(2)

        if uploaded_file is not None:
            # 读取图像
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            with col1:
                st.markdown('<div class="highlight"><h3>📥 输入图像</h3></div>', unsafe_allow_html=True)
                st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="原始图像", use_column_width=True)

            # 预处理
            processed_img = crop_and_pad(img, 480, 640)

            if st.button("开始检测", use_container_width=True):
                with st.spinner('正在检测中...'):
                    # 推理
                    t1 = time.perf_counter()
                    dets, results = inference.inference(processed_img)
                    t2 = time.perf_counter()

                    # 保存结果
                    result_img = processed_img.copy()
                    save_path = save_results(result_img, uploaded_file.name, dets, results,
                                             save_dir=st.session_state.result_dir)

                    with col2:
                        st.markdown('<div class="highlight"><h3>📤 检测结果</h3></div>', unsafe_allow_html=True)
                        st.image(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB),
                                 caption=f"检测完成 — 耗时: {t2 - t1:.3f}秒", use_column_width=True)
                        st.success(f"结果已保存至: {save_path}")



    elif mode == "批量图片检测":
        with st.sidebar:
            st.markdown("### 📁 批量上传图片")
            uploaded_files = st.file_uploader("选择多张图片", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

            # 结果保存路径选择器
            st.markdown("### 💾 选择结果保存位置")
            save_path_option = st.radio("保存位置选项", ["默认路径", "自定义路径"])

            if save_path_option == "默认路径":
                st.session_state.result_dir = default_result_dir
                st.info(f"结果将保存至: {default_result_dir}")
            else:
                custom_path = st.text_input("自定义保存路径", st.session_state.result_dir)
                if custom_path and custom_path != st.session_state.result_dir:
                    if os.path.isdir(custom_path) or not os.path.exists(custom_path):
                        os.makedirs(custom_path, exist_ok=True)
                        st.session_state.result_dir = custom_path
                        st.success(f"已设置保存路径: {custom_path}")
                    else:
                        st.error("无效的目录路径")

        if uploaded_files:
            st.success(f"已上传 {len(uploaded_files)} 张图片")

            if st.button("开始批量检测", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()

                # 创建临时目录来保存上传的图片
                with tempfile.TemporaryDirectory() as temp_dir:
                    # 保存上传的图片到临时目录
                    temp_image_paths = []
                    for uploaded_file in uploaded_files:
                        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        temp_image_paths.append(temp_file_path)

                    # 创建结果展示容器
                    results_container = st.container()
                    with results_container:
                        st.markdown('<div class="results-container"><h3>📊 检测结果</h3></div>', unsafe_allow_html=True)
                        result_gallery = st.empty()

                        # 保存所有结果图像路径，用于最后展示
                        all_results = []

                        # 处理每张图片
                        for idx, img_path in enumerate(temp_image_paths):
                            img = cv2.imread(img_path)
                            if img is None:
                                status_text.warning(f"⚠️ 读取失败，跳过：{os.path.basename(img_path)}")
                                continue

                            # 预处理
                            img = crop_and_pad(img, 480, 640)

                            # 推理
                            t1 = time.perf_counter()
                            dets, results = inference.inference(img)
                            t2 = time.perf_counter()

                            # 保存处理结果
                            img_name = os.path.basename(img_path)
                            save_path = save_results(img, img_name, dets, results, save_dir=st.session_state.result_dir)
                            all_results.append((img_path, save_path, t2 - t1, results))

                            # 更新进度
                            progress = (idx + 1) / len(temp_image_paths)
                            progress_bar.progress(progress)
                            status_text.text(f"处理进度: {idx + 1}/{len(temp_image_paths)} ({progress:.1%})")

                    # 生成结果展示
                    with results_container:
                        st.success(f"批量检测完成！所有结果已保存至: {st.session_state.result_dir}")

                        # 显示结果统计
                        total_passed = sum(1 for _, _, _, res in all_results if all(res))
                        st.markdown(f"### 总结果: {len(all_results)}/{len(all_results)} 通过检测")

                        # 显示每个结果
                        for i, (orig_path, result_path, process_time, detect_results) in enumerate(all_results):
                            st.markdown(f"#### 图片 {i + 1}: {os.path.basename(orig_path)}")

                            col1, col2 = st.columns(2)
                            with col1:
                                st.image(cv2.cvtColor(cv2.imread(orig_path), cv2.COLOR_BGR2RGB),
                                         caption=f"原始图像",
                                         use_column_width=True)
                            with col2:
                                st.image(cv2.cvtColor(cv2.imread(result_path), cv2.COLOR_BGR2RGB),
                                         caption=f"检测结果 — 耗时: {process_time:.3f}秒",
                                         use_column_width=True)



    elif mode == "实时摄像头检测":
        with st.sidebar:
            st.markdown("### 📹 摄像头设置")
            camera_id = st.selectbox("选择摄像头", options=list(range(3)), format_func=lambda x: f"摄像头 {x}")
            st.info("请确保已连接摄像头")

            # 结果保存路径选择器
            st.markdown("### 💾 选择结果保存位置")
            save_path_option = st.radio("保存位置选项", ["默认路径", "自定义路径"])

            if save_path_option == "默认路径":
                camera_result_dir = os.path.join(os.getcwd(), "camera_results")
                os.makedirs(camera_result_dir, exist_ok=True)
                st.info(f"结果将保存至: {camera_result_dir}")
            else:
                custom_path = st.text_input("自定义保存路径", os.path.join(os.getcwd(), "camera_results"))
                if custom_path:
                    if os.path.isdir(custom_path) or not os.path.exists(custom_path):
                        os.makedirs(custom_path, exist_ok=True)
                        camera_result_dir = custom_path
                        st.success(f"已设置保存路径: {custom_path}")
                    else:
                        st.error("无效的目录路径")
                        camera_result_dir = os.path.join(os.getcwd(), "camera_results")

            save_frames = st.checkbox("保存检测帧", value=False)

        run = st.checkbox("开启摄像头", value=False)

        if run:
            cap = cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                st.error("无法打开摄像头，请检查连接或选择其他摄像头")
            else:
                frame_placeholder = st.empty()
                status_placeholder = st.empty()

                frame_count = 0

                while run:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("无法读取摄像头帧")
                        break

                    # 预处理
                    frame = crop_and_pad(frame, 480, 640)

                    # 推理
                    t1 = time.perf_counter()
                    dets, results = inference.inference(frame)
                    t2 = time.perf_counter()

                    # 处理检测结果
                    result_frame = frame.copy()
                    for bbox, label in dets:
                        x1, y1, x2, y2 = map(int, bbox)
                        cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(result_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

                    for index, x in enumerate((20, 50, 80)):
                        cv2.circle(result_frame, (x, 20), 12, (0, 255, 0) if results[index] else (0, 0, 255), -1)

                    # 保存帧
                    if save_frames and frame_count % 30 == 0:  # 每隔30帧保存一次
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        save_path = os.path.join(camera_result_dir, f'camera_{timestamp}.jpg')
                        cv2.imwrite(save_path, result_frame)

                    # 显示结果
                    frame_placeholder.image(cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB),
                                            caption="实时检测", use_column_width=True)

                    status_text = f"FPS: {1 / (t2 - t1):.1f} | "
                    status_text += "状态: " + ("通过" if all(results) else "不通过")
                    status_placeholder.markdown(
                        f"<div style='text-align:center;padding:10px;background-color:{'green' if all(results) else 'red'};color:white;font-weight:bold;border-radius:5px;'>{status_text}</div>",
                        unsafe_allow_html=True)

                    frame_count += 1
                    time.sleep(0.01)  # 小延迟避免占用过多资源

                    # 检查运行状态
                    run = st.checkbox("开启摄像头", value=True)

                cap.release()
                st.info("摄像头已关闭")

    # 添加页脚
    st.markdown("""
    <div class="footer">
        <p>基于YOLOv11的交通信号检测系统 © 2025</p>
        <p>Powered by OpenCV and Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()