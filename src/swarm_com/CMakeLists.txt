cmake_minimum_required(VERSION 3.8)
project(swarm_com)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  PROGRAMS
    src/bottom_slave_lvl1.py
    src/front_slave_lvl1.py
    src/left_slave_lvl1.py
    src/master_lvl1.py
    src/right_slave_lvl1.py
    src/bottom_slave_lvl2.py
    src/front_slave_lvl2.py
    src/left_slave_lvl2.py
    src/master_lvl2.py
    src/right_slave_lvl2.py
    src/bottom_slave_lvl3.py
    src/front_slave_lvl3.py
    src/left_slave_lvl3.py
    src/master_lvl3.py
    src/right_slave_lvl3.py
    src/door_detector.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)


ament_package()
