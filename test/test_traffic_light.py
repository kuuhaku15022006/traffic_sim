# tests/test_traffic_light.py

import csv
import pytest
from collections import deque
from traffic_sim.traffic_light import TrafficLight, Intersection
from traffic_sim.loaders import load_lights_csv


# =========================================================
# 🧩 TEST TRAFFICLIGHT
# =========================================================

def test_is_green_cycle_basic(): #passed
    light = TrafficLight(green_time=3, red_time=2)

    # Tick 0–2: xanh
    for t in range(3):
        assert light.is_green(t), f"Tick {t} phải là xanh"

    # Tick 3–4: đỏ
    for t in range(3, 5):
        assert not light.is_green(t), f"Tick {t} phải là đỏ"


def test_is_green_with_offset(): #passed
    light = TrafficLight(green_time=2, red_time=2, offset=1)

    # Tick 0: đèn lệch offset => đỏ
    assert not light.is_green(0)

    # Tick 1–2: xanh
    for t in range(1,3):
        assert light.is_green(t), f"Tick {t} phải là xanh"

    # Tick 3–4: đỏ
    for t in range(3, 5):
        assert not light.is_green(t), f"Tick {t} phải là đỏ"


def test_tick_changes_state(): #passed
    light = TrafficLight(green_time=2, red_time=2)
    results = []
    for _ in range(6):
        results.append(light.is_green(light.timer))
        light.tick(1)
    # Chu kỳ: 2 xanh, 2 đỏ, 2 xanh
    assert results == [True, True, False, False, True, True]


# =========================================================
# 🧩 TEST INTERSECTION QUEUE
# =========================================================

def test_step_dispatch_when_green(): #passed
    light = TrafficLight(green_time=3, red_time=2)
    inter = Intersection("A", light)
    inter.queue.extend(["v1", "v2", "v3", "v4", "v5"])

    # Đèn xanh, nhả tối đa 2 xe
    dispatched = inter.step(dispatch_limit=3)
    assert dispatched == ["v1", "v2", "v3"]
    assert list(inter.queue) == ["v4", "v5"]


def test_no_dispatch_when_red(): #passed
    light = TrafficLight(green_time=2, red_time=2)
    inter = Intersection("B", light)
    inter.queue.extend(["x1", "x2"])

    # Chạy 2 tick để vào pha đỏ
    
    light.tick(2)

    dispatched = inter.step(dispatch_limit=5)
    assert dispatched == []  # Không nhả khi đèn đỏ
    assert len(inter.queue) == 2


def test_queue_persists_across_ticks():
    light = TrafficLight(green_time=2, red_time=1)
    inter = Intersection("C", light)
    inter.queue.extend(["a", "b", "c"])

    inter.step(1)
    inter.step(1)
    assert len(inter.queue) == 1  # Còn 1 xe

    light.tick()  # sang pha đỏ
    dispatched = inter.step(2)
    assert dispatched == []


# =========================================================
# 🧩 TEST LOADERS LIGHTS
# =========================================================

def test_load_lights_csv(tmp_path):
    """Kiểm thử load_lights_csv() có tạo đúng dict TrafficLight không."""
    csv_path = tmp_path / "lights.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "green_time", "red_time", "offset"])
        writer.writerow(["A", 3, 2, 0])
        writer.writerow(["B", 4, 1, 1])

    lights = load_lights_csv(csv_path)
    assert isinstance(lights, dict)
    assert "A" in lights and "B" in lights
    assert isinstance(lights["A"], TrafficLight)
    assert lights["A"].green_time == 3
    assert lights["B"].offset == 1
