from asyncio import shield
from random import randint
import numpy as np
from math import atan2, pi, cos, sin
import itertools

# constants
checkpoint_radius = 600


def print_input(func):
    def wrapper(*arg):
        print(*arg[1:])
        return func(*arg)
    return wrapper


def print_output(func):
    def wrapper(*arg):
        res = func(*arg)
        print(res)
        return res
    return wrapper


def points_angle(point1, point2):
    y =point2[1]-point1[1]
    x = point2[0]-point1[0]
    t = atan2(y,x)
    mt =  (t + 2*pi)%(2*pi)
    return mt
    # return (atan2(point2[1]-point1[1], point2[0]-point1[0])+2*pi) % (2*pi)


def distance(point1, point2=[0, 0]):
    return ((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)**0.5


class Pod:
    id_iter = itertools.count()

    def __init__(self,position, checkpoints, angle=None):
        self.boost_val = 650
        self.turns_limit = 45
        self.id = next(self.id_iter)

        self.thurst = 0
        self.angle = angle
        self.position = np.array(position, np.float64)
        self.speed = np.array([0.0, 0.0])
        self.boost = False
        self.shield_count = 0
        self.dt = 1
        self.checkpoints = checkpoints
        self.checkpoint_counter = 0
        self.laps = 0
        self.turn = 0

    def diff_angle(self, point):
        a = points_angle(self.position, point)
        r, l = .0, .0
        if self.angle <= a:
            r = a - self.angle
        else:
            r = 2*pi-self.angle+a
        if self.angle >= a:
            l = self.angle - a
        else:
            l = 2*pi+self.angle-a
        if r < l:
            return r
        return -l

    def rotate(self, point):
        a = self.diff_angle(point)
        a = max(min(a, pi/10), -pi/10)
        self.angle += a
        self.angle = (2*pi + self.angle) % (pi*2)

    def move_pod(self, dest, command, t=1):
        dest = np.array(dest)
        if self.shield_count:
            self.shield_count += 1
            if self.shield_count == 3:
                self.shield_count = 0
            self.thurst = 0
            return self.calc_pos(dest, t)
        if command == "SHIELD":
            self.shield_count = 1
            self.thurst = 0
            return self.calc_pos(dest, t)
        if command == "BOOST":
            if self.boost:
                self.thurst = 0
                return self.calc_pos(dest, t)
            self.boost = True
            self.thurst = self.boost_val
            return self.calc_pos(dest, t)
        self.thurst = command
        return self.calc_pos(dest, t)

    def calc_pos(self, dest, t=1):
        # acceleration = ((dest-self.position)/distance(dest,self.position))*(thurst)
        if self.angle == None:
            self.angle = points_angle(self.position, dest)
        self.rotate(dest)
        acceleration = np.array([cos(self.angle), sin(self.angle)])*self.thurst
        # print(np.round(self.position))
        self.speed += acceleration*t
        self.position += np.round(self.speed*t)
        self.speed = np.trunc(self.speed*0.85**t)

    def next_turn(self, dest, command):
        self.move_pod(dest, command, 1)
        dist = distance(
            self.checkpoints[self.checkpoint_counter], self.position)
        self.turn += 1
        if dist <= checkpoint_radius:
            self.turn = 0
            self.checkpoint_counter = (
                self.checkpoint_counter+1) % len(self.checkpoints)
            if self.checkpoint_counter == 0:
                self.laps += 1
        if self.turn > self.turns_limit:
            self.laps =-1
        return self.laps


class Simulation:
    def __init__(self, checkpoint=None, pods_location=None):
        self.map_size = 16000, 9000
        self.checkp_2_edge = 1000
        self.pods_radius = 400

        self.turns = 0
        if checkpoint == None:
            self.checkpoints = self.generate_checkpoints(randint(3, 5))
        else:
            self.checkpoints = [np.array(checkpoint[i:i+2])
                                for i in range(0, len(checkpoint), 2)]
        if pods_location == None:
            self.numb_pods = 1
            self.pods = self.gen_pods()
        else:
            self.numb_pods = len(pods_location)
            self.pods = [Pod(np.array(loc), self.checkpoints)
                         for loc in pods_location]

    def generate_checkpoints(self, numb):
        checkpoints = []
        for i in range(numb):
            x = randint(self.checkp_2_edge,
                        self.map_size[0]-self.checkp_2_edge)
            y = randint(self.checkp_2_edge,
                        self.map_size[1]-self.checkp_2_edge)
            checkpoints.append(np.array([x, y]))
        return checkpoints

    def gen_pods(self):
        # now only for 2
        if self.numb_pods == 1:
            return [Pod(self.checkpoints[-1], self.checkpoints)]

        tangent_vector = (
            self.checkpoints[0]-self.checkpoints[-1])*np.array([1, -1])
        pos_1 = (tangent_vector/distance([0, 0], tangent_vector))*500
        pos_2 = pos_1*-1
        return [Pod(pos_1, self.checkpoints), Pod(pos_2, self.checkpoints)]

    # @print_output
    def get_input(self, pod_id=0):
        pod = self.pods[pod_id]
        checkpoint = pod.checkpoints[pod.checkpoint_counter]
        dist = distance(pod.position, checkpoint)

        angle = points_angle(pod.position, checkpoint)
        return {"pos": pod.position, "checkpoint": checkpoint, "dist": dist, "angle": angle}

    # @print_input
    def set_output(self, x, y, thurst, pod_id=0):
        self.turns += 1
        self.pods[pod_id].next_turn(np.array([x, y]), thurst)
        return self

