import cv2
import numpy as np
import pyautogui
import keyboard
import os
import time

def find_and_move(target_path, threshold=0.8):
    # 截图当前屏幕
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 读取模板图片
    template = cv2.imread(target_path, cv2.IMREAD_COLOR)
    if template is None:
        print("❌ 无法读取模板图片:", target_path)
        return

    # 获取模板尺寸
    h, w = template.shape[:2]

    # 多尺度匹配（应对不同分辨率）
    found = None
    for scale in np.linspace(0.5, 1.5, 15):  # 尝试不同缩放比例
        resized = cv2.resize(template, (int(w * scale), int(h * scale)))
        result = cv2.matchTemplate(screenshot, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if found is None or max_val > found[0]:
            found = (max_val, max_loc, scale)

    max_val, max_loc, scale = found
    print(f"匹配置信度: {max_val:.3f}, 缩放比例: {scale:.2f}")

    if max_val >= threshold:
        # 计算中心坐标
        th, tw = int(h * scale), int(w * scale)
        center_x = max_loc[0] + tw // 2
        center_y = max_loc[1] + th // 2

        # 移动鼠标
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        print(f"✅ 找到并移动到坐标: ({center_x}, {center_y})")
    else:
        print("❌ 未找到匹配图像")

def main():
    img_path = os.path.join(os.getcwd(), "Images", "Reportpng.png")
    print("按 F5 开始匹配，按 ESC 退出。")

    while True:
        if keyboard.is_pressed("f5"):
            print("开始匹配...")
            find_and_move(img_path)
            time.sleep(1)  # 防止连续触发
        elif keyboard.is_pressed("esc"):
            print("退出程序。")
            break

if __name__ == "__main__":
    main()
