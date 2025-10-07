import csv
from traffic_sim.traffic_light import TrafficLight


def load_lights_csv(path) -> dict[str, TrafficLight]:
    lights = {}
    with open(path, newline= '') as f:
            reader = csv.DictReader(f)
            for row in reader:
                  node = row['node']
                  lights[node] = TrafficLight(
                green_time=int(row['green_time']),
                red_time=int(row['red_time']),
                offset=int(row.get('offset', 0))
            )
    return lights
