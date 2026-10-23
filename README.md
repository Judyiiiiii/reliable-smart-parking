# Reliable Smart Parking

GE1354 Group 14 SemB Micro:bit 智能停车场小组作业的一次小型升级。

原项目已经包含双 Micro:bit、HC-SR04 超声波、Radio、OLED、舵机闸机、车位 LED、NeoPixel、蜂鸣器和环境灯。本次改进最容易受噪声影响的“超声波读数 -> 车位状态”部分。

## 运行仿真测试

在项目根目录执行：

```text
python -m unittest discover -s tests -v
```

当前实现只使用 Python 标准库，不需要安装依赖。

## 核心思路

### 1. 多次采样滤波

`MedianFilter` 保存最近 5 次距离读数并取中位数。比如汽车实际还在车位中，但传感器偶尔读到 60 cm，这一次异常值不会立刻把车位误判为空。

5 是奇数，避免中位数不明确；`sample_count` 必须是正奇数。

### 2. 连续确认和滞回阈值

状态保持原项目需要的两个输出状态：

```text
EMPTY --连续两次 < 10 cm--> OCCUPIED
OCCUPIED --连续两次 > 12 cm--> EMPTY
```

10 cm 和 12 cm 使用不同的进入/离开阈值，避免车辆停在边界附近时红绿灯来回闪烁。这是一个小型、容易在 Micro:bit 上实现的状态机，而不是复杂的新系统。

### 3. Python 仿真测试

`simulate()` 接收一串原始距离读数，返回每次采样后的状态。例如：

```python
from parking_system import simulate

print(simulate([20, 20, 6, 60, 6, 6]))
```

测试覆盖了：超声波尖峰、车辆进入、车辆离开、阈值边界抖动，以及参数错误。

## 如何接到 Micro:bit

本项目把“判断逻辑”和“硬件读数”分开。Micro:bit 主程序只需要周期性完成下面几步：

1. 用原项目的 `get_distance(trig, echo)` 读取一次距离。
2. 调用 `controller.update(distance_cm)`。
3. 根据返回的 `ParkingState` 控制 LED、蜂鸣器或 NeoPixel。

示意代码：

```python
from parking_system import ParkingController, ParkingState

controller = ParkingController(sample_count=5, confirmations=2)

# distance_cm 来自原项目的 get_distance(trig, echo)
state = controller.update(distance_cm)

if state == ParkingState.OCCUPIED:
    # 点亮红灯 / 显示 X
    pass
elif state == ParkingState.EMPTY:
    # 点亮绿灯 / 显示 ✓
    pass
```

硬件版本只需要把 `distance_cm` 接到原来的超声波读取函数。这样入口/出口 Radio、OLED、舵机和灯光功能不需要重写。

## 参数怎么讲解

- `sample_count=5`：最近 5 次距离读数。更大更稳定，但响应更慢。
- `confirmations=2`：连续 2 次确认后才改变状态。更大更不容易误报，但状态显示会更晚。
- `10 cm / 12 cm`：进入和离开的两个阈值，应根据实际车位尺寸校准。
- 采样周期应根据传感器稳定时间设置，例如每 200–500 ms 采样一次，再用实验调整。

## 当前刻意不包含的内容
复杂 AI、ROS、云端部署、数据库或网页控制台。本次只做“读数 -> 滤波 -> 连续确认 -> LED 状态”这一条可靠性升级。

## 文件结构

```text
parking_system.py             # 与 Micro:bit 无关的滤波和状态逻辑
tests/test_parking_system.py   # 可重复运行的 Python 测试
README.md                      # 原项目背景、升级说明和接入方法
```

