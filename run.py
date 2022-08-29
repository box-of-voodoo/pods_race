import datetime
import numpy as np

from simulation.simulation import Simulation
import simulation.log_sim as log_sim

if __name__ == "__main__":

    checkpoints = "7230 6662 5443 2816 10340 3380 11222 5398"
    checkpoints = [int(i) for i in checkpoints.split(" ")]
    checkpoints = checkpoints[2:] + checkpoints[:2]
    pod_l = [[6777, 6873]]

    sim = Simulation(checkpoints, pod_l)
    log = log_sim.LogSim(sim)
    print()
    file_name = "game_data/" + datetime.datetime.now().isoformat(sep="_",timespec="seconds") + ".json"
    print(file_name)
    
    turns = 0
    x, y = 0, 0
    while True:
        turns += 1
        inpt = sim.get_input()
        if turns == 1:
            x, y = inpt["pos"][0], inpt["pos"][1]
        thurst = 50
        pos1, pos2 = x, 0
        if turns > 4:
            pos1, pos2 = x+100, 9000
        if turns > 15:
            thurst = 0

        out = sim.set_output(pos1, pos2, thurst)
        log.add_turn(sim)

        print(sim.pods[0].position, end="\t")
        print(np.round(sim.pods[0].speed), round(np.degrees(sim.pods[0].angle),1), end="\t")
        print(pos1, pos2)
        # print(inpt["checkpoint"])
        print(sim.turns-1, end="\t")
        laps = [pod.laps for pod in sim.pods]
        print(laps)
        
        if max(laps) >= 1:
            break
        if min(laps) == -1:
            print("GAME OVER")
            break
    log.save(file_name)
