import subprocess
import time
import shlex
import os

rootPath = os.path.expanduser("~")

def simulate(pathToRightHandWptFile, pathToComWptFile, savePath=None, verbose=False, visual=False):

    # Gazebo world file
    pathToIcubGazeboWorlds = rootPath + "/icub-gazebo/world"
    icubWorldPath = pathToIcubGazeboWorlds + "/icub.world"

    # Task set path
    allTaskSets = rootPath + "/bayesian-task-optimization/reaching-task-sets/icubGazeboSim"
    taskSetPath = allTaskSets + "/TaskOptimizationTaskSet.xml"


    if verbose:
        print('Starting script...')
    if verbose:
        print('-- Launching yarpserver')
    yarp = subprocess.Popen(["yarpserver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)

    if visual:
        if verbose:
            print('-- Launching gazebo with icub.world @', icubWorldPath)
        gazebo = subprocess.Popen(["gazebo", icubWorldPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        if verbose:
            print('-- Launching gzserver with icub.world @', icubWorldPath)
        gazebo = subprocess.Popen(["gzserver", icubWorldPath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)


    args1 = "ocra-icub-server --floatingBase --controllerType HOCRA --solver QPOASES --taskSet " + taskSetPath + " --absolutePath"
    args = shlex.split(args1)
    if verbose:
        print('-- Launching ocra-icub-server with args: ', args)
    controller = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(5)

    if savePath != None:
        save_args = " --savePath " + savePath
    else:
        save_args = ""

    args1 = "reach-client --rightHandWptFile "+pathToRightHandWptFile+" --comWptFile " + pathToComWptFile + save_args
    args = shlex.split(args1)
    if verbose:
        print('-- Launching reach-client with args: ', args)
    client = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    timeout = 40.0
    try:
        client.wait(timeout)
    except: 
        client.kill()


    timeout = 20.0
    if verbose:
        print('-- Terminating controller')
    controller.terminate()
    try:
        controller.wait(timeout)
    except: 
        controller.kill()
    if verbose:
        print('-- Terminating gzserver')
    gazebo.terminate()
    try:
        gazebo.wait(timeout)
    except: 
        gazebo.kill()
    if verbose:
        print('-- Cleaning up ports')
    args1 = "yarp clean"
    args = shlex.split(args1)
    cleanYarp = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        cleanYarp.wait(timeout)
    except: 
        cleanYarp.kill()
    if verbose:
        print('-- Terminating yarpserver')
    yarp.terminate()