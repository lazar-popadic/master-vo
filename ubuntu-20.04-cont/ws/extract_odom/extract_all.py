from bagpy import bagreader
import pandas as pd
import math
import os
from pathlib import Path


def get_yaw_from_quaternion(x, y, z, w):
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


rootdir = '../bags'
extensions = ('.bag')
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))
            b = bagreader(f'../bags/{file}')

            csvfiles = []
            odom_msgs = b.message_by_topic("/ros381/odom")
            csvfiles.append(odom_msgs)

            data = pd.read_csv(csvfiles[0])
            print(data)

            result = pd.DataFrame({
                'timestamp': data['Time'],
                'x': data['pose.pose.position.x'],
                'y': data['pose.pose.position.y'],
                'phi': data.apply(lambda row: get_yaw_from_quaternion(
                    row['pose.pose.orientation.x'],
                    row['pose.pose.orientation.y'],
                    row['pose.pose.orientation.z'],
                    row['pose.pose.orientation.w']
                ), axis=1),
                'v': data['twist.twist.linear.x'],
                'w': data['twist.twist.angular.z'],
            })

            print(result)
            bag = Path(file).stem
            result.to_csv(f'{bag}.csv', index=False)
            print(f"Exported {len(result)} messages to {bag}.csv")