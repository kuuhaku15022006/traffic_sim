from collections import deque

class TrafficLight:
    def __init__(self, green_time: int, red_time: int, offset: int = 0):
        self.green_time = green_time
        self.red_time = red_time
        self.cycle = green_time + red_time
        self.timer = offset
        self.offset = offset

    def is_green (self, tick: int = None) -> bool:
        if tick == None:
            tick = self.timer
        pos_in_cycle = (tick - self.offset) % self.cycle
        return pos_in_cycle < self.green_time

     
    def tick(self, sec = None):
        if sec == None:
            if self.is_green():
                self.timer = (self.offset + self.green_time) % self.cycle
            else:
                self.timer = self.offset % self.cycle
        else:
            self.timer = (self.timer + sec) % self.cycle

class Intersection:
    def __init__(self, node_id: str, traffic_light: TrafficLight):
        self.node_id = node_id
        self.traffic_light =traffic_light
        self.queue = deque()
    
    def step(self, dispatch_limit: int) -> list[str]:
        dispatched = []
        if self.traffic_light.is_green():
            for t in range (min(dispatch_limit,len(self.queue))):
                dispatched.append(self.queue.popleft())
        return dispatched   
