project(MainWidget VERSION 1.0.0)

include_directories(./include)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


find_package(Qt6 COMPONENTS
        Core
        REQUIRED)

aux_source_directory(./ SRC_LIST)

add_executable(${PROJECT_NAME} ${SRC_LIST})


target_link_libraries(${PROJECT_NAME} PUBLIC
        Qt::Core
        )

