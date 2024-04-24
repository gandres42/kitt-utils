import triad_openvr.triad_openvr as triad_openvr
import time
import sys
import numpy as np
import networktables

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
    
r_offset = None
t_offset = None

if interval:
    while r_offset == None:
        for device in v.devices.items():
            if device[0] != 'tracker_1':
                continue

            pose = device[1].get_pose_matrix()
            r = np.array([
                [pose[0][0], pose[0][1], pose[0][2]],
                [pose[1][0], pose[1][1], pose[1][2]],
                [pose[2][0], pose[2][1], pose[2][2]],
            ])
            t = np.array([
                [pose[0][3]],
                [pose[1][3]],
                [pose[2][3]],
            ])

            print(t)
            
            if r_offset is None:
                r_offset = np.linalg.inv(r)

            