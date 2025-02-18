import launch
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gnome-terminal', '--', 'ros2', 'run', 'swarm_com', 'bottom_slave.py'],
            output='screen'
        ),
        ExecuteProcess(
            cmd=['gnome-terminal', '--', 'ros2', 'run', 'swarm_com', 'master.py'],
            output='screen'
        ),
        # Add more processes if needed
    ])
