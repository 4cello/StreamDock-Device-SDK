# StreamDock SDK for Linux (English & Chinese Documentation)

## English Version

### 🔧 Linux-x86_64 Platform Support for StreamDock SDK

> ✅ Recommended environment: ​**Ubuntu 20.04**​, **Python 3.8.10** or above

---

### 🐍 Python Dependencies

Install the required Python libraries:

```bash
pip install pillow pyudev
```

> `threading`, `ctypes`, `time`, and `abc` are part of the Python standard library and ​**do not require installation**​.

---

### 📦 System Dependencies

To use the SDK on Linux, install the following system packages:

```bash
sudo apt install -y libudev-dev libusb-1.0-0-dev libhidapi-libusb0
```

> ⚠️ Note: `libusb-1.0-0-dev` must be installed **before**`libhidapi-libusb0`.

If you encounter the error:

```
undefined reference to `get_input_report()`
```

Replace the file at:

```
/usr/local/lib/libhidapi-libusb.so.0
```

with the `libhidapi-libusb.so.0` file provided in the **Transport** folder.

---

### 🚀 Quick Start Example

```python
from StreamDock.DeviceManager import DeviceManager
from StreamDock.Devices.StreamDockN1 import StreamDockN1
import threading
import time

if __name__ == "__main__":
    manner = DeviceManager()
    streamdocks= manner.enumerate()
    # listen plug/unplug
    t = threading.Thread(target=manner.listen)
    t.daemon = True 
    t.start()
    print("Found {} Stream Dock(s).".format(len(streamdocks)))
    for device in streamdocks:
        # open device
        device.open()
        device.init()
        # set background image
        res = device.set_touchscreen_image("../img/YiFei320.png")
        device.refresh()
        time.sleep(2)
        for i in range(1, 19):
            device.set_key_image(i, "../img/tiga64.png")
            device.refresh()
        time.sleep(2)
        # clear specialize key
        device.clearIcon(3)
        device.refresh()
        time.sleep(1)
        # clear all key
        device.clearAllIcon()
        device.refresh()
        time.sleep(0)
        # N1 switch mode
        if isinstance(device, StreamDockN1):
            device.switch_mode(0)
        # close device
        # device.close()
    time.sleep(10000)
```

---

### ⚠️ Important Notes

#### 1. Thread Management

Use `threading.Thread(..., daemon=True)` for:

* Device plug/unplug detection
* Key press event listening

These threads are long-running. Use daemon threads or control loops with booleans if needed.

#### 2. Platform Differences

Only newer platforms support **asynchronous detection** of key press and device response events during image setting.

| Platform   | Async Key Events While Setting Images | Notes                                                             |
| ------------ | --------------------------------------- | ------------------------------------------------------------------- |
| 293V3 / N4 | ✅ Supported                          | Can detect key presses during`setKeyImg`/`setTouchScreen` |
| 293 / 293s | ❌ Not supported                      | Must wait for image setting to finish before detecting key events |

On older platforms (e.g., 293, 293s), key press events cannot be detected while `setKeyImg` or `setTouchScreen` is in progress. You must wait until the operation completes and the device is idle.

#### 3. 🔌 Hotplug & Auto-Reconnect

When a device is replugged (USB unplugged and plugged in again), the SDK will **automatically reconnect** the device using `DeviceManager.listen()`.

You can customize your reconnect logic right after the device is re-detected:

```python
# your reconnect logic like the next two line
newDevice.set_key_image(1, "../img/tiga64.png")
newDevice.refresh()
```

We recommend wrapping your reconnection configuration in a helper method such as `autoInit()`:

```python
newDevice.open()
newDevice.autoInit()  # e.g., reset icons, refresh screen, set mode
```

This ensures the reconnected device resumes its previous working state.

> On macOS, this uses internal polling (`hid.enumerate()`); on Linux, it uses pyudev to detect events in real time.
