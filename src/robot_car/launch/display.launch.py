from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get URDF file path
    urdf_file = os.path.join(
        get_package_share_directory("robot_car"),
        'urdf',
        'robot_car.urdf.xacro'  # Make sure this matches your actual file name
    )
    
    # Verify the file exists
    if not os.path.exists(urdf_file):
        raise RuntimeError(f"URDF file not found at {urdf_file}")
    
    # Read URDF contents
    with open(urdf_file, 'r') as infp:
        robot_description_content = infp.read()

    # Get RViz config path
    rviz_config_file = os.path.join(
        get_package_share_directory('robot_car'),
        'rviz',
        'robot_model.rviz'
    )

    # Get DiffDrive controller config path
    diff_drive_controller_config = os.path.join(
        get_package_share_directory('robot_car'),
        'config',
        'diff_drive_controller.yaml'  # Ensure this YAML file is correctly configured
    )

    return LaunchDescription([        
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description_content}]
        ),
        
        # Joint State Publisher
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen'
        ),
        
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            output='screen'
        ),
        
        # RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_file]  # No parameters needed for RViz
        ),
        
        # Start diff_drive_controller
        Node(
            package='controller_manager',
            executable='spawner',
            name='diff_drive_controller_spawner',
            output='screen',
            arguments=['diff_drive_controller']  # Start the controller
        ),
        
        # Robot control via teleop (keyboard)
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            output='screen',
            parameters=[{'use_sim_time': 'true'}],  # Enable simulation time if needed
        ),
    ])
