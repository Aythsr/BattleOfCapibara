cmake_minimum_required(VERSION 3.20)

# 设置项目名称和版本
project(Nome VERSION 0.1.0 LANGUAGES CXX)

# 设置C++标准
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 设置警告选项
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")

# 添加一个
add_library(NomeFlag INTERFACE)
target_include_directories(NomeFlag INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)

enable_testing()
# 添加三方库
# add_subdirectory(thirdparty) 

add_subdirectory(src)

# add_subdirectory(test)

# add_subdirectory(examples)

