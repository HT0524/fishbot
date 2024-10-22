import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 定位到功能包的地址
    pkg_share = FindPackageShare(package='fishbot_cartographer').find('fishbot_cartographer')

    #=====================运行节点需要的配置=======================================================================
    # 是否使用仿真时间
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    # 配置文件夹路径
    configuration_directory = LaunchConfiguration('configuration_directory', default=os.path.join(pkg_share, 'config'))
    # 纯定位的配置文件
    configuration_basename = LaunchConfiguration('configuration_basename', default='pure_localization.lua')
    # 地图文件位置
    map_file = '/home/ht/fishbot/src/fishbot_cartographer/map/fishbot_map.yaml'
    rviz_config_dir = os.path.join(pkg_share, 'config') + "/cartographer.rviz"

    #=====================声明两个节点，cartographer/rviz_node=================================
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-configuration_directory', configuration_directory,
                   '-configuration_basename', configuration_basename]
    )

    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='nav2_map_server',
        output='screen',
        parameters=[{
            'yaml_filename': map_file,
            'use_sim_time': use_sim_time
        }]
    )

    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     arguments=['-d', rviz_config_dir],
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     output='screen'
    # )

    #===============================================定义启动文件========================================================
    ld = LaunchDescription()
    ld.add_action(cartographer_node)
    ld.add_action(map_server_node)
    # ld.add_action(rviz_node)

    return ld
