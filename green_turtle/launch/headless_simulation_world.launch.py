import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

MODEL_CONSTANT = "waffle"
WORLD_CONSTANT = 'maze'


def generate_launch_description():
    # Because we simulate the world, this should always be true 
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # String reference the world file
    # Note: The world file loads the gazebo robot model, make sure the urdf matches
    world = os.path.join(get_package_share_directory('green_turtle'), 'worlds', WORLD_CONSTANT + ".model")
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    
    # We use the turtlebots so we reference the description
    robot_urdf_name = "turtlebot3_" + MODEL_CONSTANT + ".urdf"
    robot_urdf = os.path.join(get_package_share_directory('turtlebot3_description'), 'urdf', robot_urdf_name)

    
    # Define what to launch
    gz_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource( os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        launch_arguments={'world': world, "verbose": "true"}.items()
    )

    # gz_client = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py'))
    # )

    robot_state = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=[robot_urdf]
    )

    # Build and return
    ld = LaunchDescription()
    ld.add_action(gz_server)
    # ld.add_action(gz_client)
    ld.add_action(robot_state)
    return ld