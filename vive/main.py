import triad_openvr.triad_openvr as triad_openvr
import time
import sys
import numpy as np
from networktables import NetworkTables

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

NetworkTables.initialize(server='192.168.1.109')
nt = NetworkTables.getTable("localization")

station_t = np.array([
    [-.67],
    [1.01],
    [3.26]
])

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False

if interval:
    while True:
        start = time.time()
        txt = ""
        for device in v.devices.items():
            if device[0] != 'tracker_1':
                continue

            pose = device[1].get_pose_matrix()
            
            if pose is None:
                continue
            
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

            real_pos = t # + station_t

            print(real_pos)
            nt.putNumber('vive_x', real_pos[2])
            nt.putNumber('vive_y', real_pos[0])
            nt.putNumber('vive_z', real_pos[1])

        time.sleep(1/60)
            