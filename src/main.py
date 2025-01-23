from StreamDock.DeviceManager import DeviceManager
from StreamDock.ImageHelpers import PILHelper
import threading
import time

if __name__ == "__main__":
    manner = DeviceManager()
    streamdocks= manner.enumerate()
    # 监听设备插拔
    t = threading.Thread(target=manner.listen)
    t.start()
    print("Found {} Stream Dock(s).\n".format(len(streamdocks)))
    arr = []
    for device in streamdocks:
        # 打开设备
        device.open()
        device.wakeScreen()
        # 开线程获取设备反馈
        t = threading.Thread(target=device.whileread)
        t.daemon = True # detach
        t.start()
        # 设置设备亮度0-100
        device.set_brightness(50)
        # # 设置背景图片（传图片的地址）
        # device.clearAllIcon()
        for i in range(1000):
            res = device.set_touchscreen_image("../img/YiFei320.png")
            device.refresh()
            time.sleep(2)
            device.clearAllIcon()
            for i in range(10):
                device.set_key_image(i + 1, "../img/tiga64.png")
            device.refresh()
            time.sleep(2)
        # 清空某个按键的图标
        device.cleaerIcon(3)
        time.sleep(1)
        # 清空所有按键的图标
        # device.clearAllIcon()
        device.refresh()
        # time.sleep(1)
        # 关闭设备
        # device.close()
    t.join()
    time.sleep(10000)
    
    
