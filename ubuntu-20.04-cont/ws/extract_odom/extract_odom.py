from bagpy import bagreader
import pandas as pd
import numpy as np
import math


def get_yaw_from_quaternion(x, y, z, w):
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)

bag = "curve_sequence_medium"

b = bagreader(f'../bags/{bag}.bag')

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
    ), axis=1)
})

print(result)
result.to_csv(f'{bag}.csv', index=False)
print(f"Exported {len(result)} messages to {bag}.csv")