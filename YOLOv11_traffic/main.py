import cv2
import os
import time
from inferences.images import inference as inference

def crop_and_pad(image, target_height=480, target_width=640):
    """裁剪并填充白色"""
    if image is None:
        raise ValueError("读取图像失败，请检查路径是否正确！")

    h, w, _ = image.shape

    # 计算裁剪区域（居中裁剪）
    start_x = max((w - target_width) // 2, 0)
    start_y = max((h - target_height) // 2, 0)

    cropped_image = image[start_y:start_y + min(target_height, h), start_x:start_x + min(target_width, w)]

    # 计算填充尺寸
    top_pad = max((target_height - cropped_image.shape[0]) // 2, 0)
    bottom_pad = target_height - cropped_image.shape[0] - top_pad
    left_pad = max((target_width - cropped_image.shape[1]) // 2, 0)
    right_pad = target_width - cropped_image.shape[1] - left_pad

    # 填充白色
    padded_image = cv2.copyMakeBorder(cropped_image, top_pad, bottom_pad, left_pad, right_pad,
                                      cv2.BORDER_CONSTANT, value=(255, 255, 255))
    return padded_image

def save_results(image, image_name, detections, results):
    for bbox, label in detections:
        x1 = bbox[0]
        y1 = bbox[1]
        x2 = bbox[2]
        y2 = bbox[3]

        image = cv2.putText(image, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255))
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255))

    for index, x in enumerate((20, 50, 80)):
        image = cv2.circle(image, (x, 20), 12, (0, 255, 0) if results[index] else (0, 0, 255), -1)

    cv2.imwrite(f'inferences/results/result_{image_name}', image)


def main():
    for image_name in os.listdir('inferences/images'):
        image = cv2.imread(f'inferences/images/{image_name}')
        if image is None:
            print(f"警告：无法读取图像 {image}，跳过该文件！")
            continue  # 跳过该图像

        # 裁剪并填充
        image = crop_and_pad(image, 480, 640)
        time1 = time.perf_counter()
        detections, results = inference.inference(image)
        time2 = time.perf_counter()

        save_results(image, image_name, detections, results)

        cv2.imshow('Inference Result', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(f'Image: {image_name:<8} Time: {time2 - time1:.3f}s')


if __name__ == '__main__':
    main()
