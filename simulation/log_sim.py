import json
import simulation
import datetime
import numpy as np


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class LogSim:

    def __init__(self, sim):
        self.data = {
            "date": datetime.date.today().isoformat(),
            "time":
            datetime.datetime.today().time().isoformat(timespec="seconds")
        }
        self.make_head(sim)

    def make_head(self, sim):
        self.data["map"] = {}
        self.data["map"]["size"] = [sim.map_size[0], sim.map_size[1]]
        self.data["map"]["checkpoints"] = [
            {"x": i[0], "y":i[1]} for i in sim.checkpoints]
        self.data["pods"] = {"number": sim.numb_pods,
                             "ids": [i.id for i in sim.pods]}
        self.data["run_data"] = []

    def add_turn(self, sim):
        turn_data = {"turn": sim.turns, "pods": []}
        for pod in sim.pods:
            pod_data = {"id": pod.id, "x": pod.position[0], "y": pod.position[1], "angle": pod.angle,
                        "speed_x": pod.speed[0], "speed_y": pod.speed[1], "thurst": pod.thurst, "shield": pod.shield_count == 1}
            turn_data["pods"].append(pod_data)
        self.data["run_data"].append(turn_data)

    def save(self, file_name: str):
        with open(file_name, 'w') as f:
            json.dump(self.data, f, indent=4, cls=NpEncoder)
