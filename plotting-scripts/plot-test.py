from one_com_waypoint_static import *
import os
import re
import sys
sys.path.append("../optimization-scripts")
from task_optim.utils.files import *



test_dir = os.path.abspath("./test_data")


dirs = [d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))]

iter_dirs = [os.path.join(test_dir, d) for d in dirs if re.match('Iteration_.*', d)]
opt_dir = [os.path.join(test_dir, d) for d in dirs if re.match('Optimal_Solution', d)]

print("I found "+str(len(iter_dirs))+" iteration directories in the test directory: "+test_dir)

# rh = right hand
com_task_data, rh_task_data = getDataFromFiles(iter_dirs[0])

import matplotlib.pyplot as plt

com_tracking_cost = com_task_data.positionErrorSquaredNormTimeAveraged()
rh_tracking_cost = rh_task_data.positionErrorSquaredNormTimeAveraged()

com_goal_cost = com_task_data.goalPositionErrorSquaredNormPenalized()
rh_goal_cost = rh_task_data.goalPositionErrorSquaredNormPenalized()

energy_cost = com_task_data.torquesSquaredNormTimeAveragedScaled()

total_cost = com_tracking_cost + rh_tracking_cost + com_goal_cost + rh_goal_cost + energy_cost

total_cost = total_cost / max(total_cost)

fig, axarr = plt.subplots(4, sharex=True, num=None, figsize=(8, 10), facecolor='w', edgecolor='k')

axarr[0].set_ylabel(r'$j_{tracking}$')
axarr[0].plot(com_task_data.time, com_tracking_cost, 'r', lw=3)
axarr[0].plot(rh_task_data.time, rh_tracking_cost, 'b', lw=3)
axarr[1].set_ylabel(r'$j_{goal}$')
axarr[1].plot(com_task_data.time, com_goal_cost , 'r', lw=3)
axarr[1].plot(rh_task_data.time, rh_goal_cost, 'b', lw=3)
axarr[2].set_ylabel(r'$j_{energy}$')
axarr[2].plot(com_task_data.time, energy_cost, 'g', lw=3)
axarr[3].set_ylabel(r'$j_{total}$')
axarr[3].plot(com_task_data.time, total_cost, 'k', lw=3)







plt.show()
